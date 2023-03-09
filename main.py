#!/usr/bin/python3

from heapq import *

import numpy as np

import matplotlib as mpl
mpl.use('tkagg')

import matplotlib.pyplot as plt

from global_params import *
from reader import *
from tag import *

class TimedEvents(object):

    def __init__(self, reader, tags_list):
        self.reader = reader
        self.tags_list = tags_list
        self.pq = [] # priority queue

        print("Initialize reader... Reader ID: " + str(reader.ID))
        print("Initialize tags... ")
        for cur_tag in tags_list:
            print(" - Tag ID: " + str(cur_tag.ID) + ", location: " + str(cur_tag.loc) + ", state: " + str(cur_tag.state))

        self.timestamp_prev = []
        self.timestamp_cur = []
        self.reader_state = []

        # event of the reader, current event time, previous event time
        heappush(self.pq, (reader, 0.0, -1.0))
        self.timestamp_prev.append(-1.0)
        self.timestamp_cur.append(0.0)
        self.reader_state.append(0)

    def identify_selected_tags(self):
        # TODO: modify methods to select the tag population
        # tags whose inventoried parameter (for the session specified in the Query)
        # and sel parameter match its current flag values
        selected_tags_list = self.tags_list
        return selected_tags_list

    def process_event(self):
        # pop the current reader event that has already finished
        # with the format (reader state, current event time, previous event time)
        (reader, cur_time, prev_time) = heappop(self.pq)

        # update reader states
        if reader.state == ReaderState.SELECT_RX:
            # resolve tag operations
            pass

        elif reader.state == ReaderState.QUERY_RX:
            # resolve tag operations
            cur_reader_Q = reader.query(2)
            cur_selected_tags_list = self.identify_selected_tags()
            for cur_tag in cur_selected_tags_list:
                if cur_tag.state == TagState.READY:
                    cur_tag.rng(cur_reader_Q)
                    print("Tag " + str(cur_tag.ID) + "'s randomized slot counter: " + str(cur_tag.slot_counter))
                    cur_tag.next_state()

        elif reader.state == ReaderState.QUERY_REP_RX:
            # resolve tag operations
            for cur_tag in cur_selected_tags_list:
                if cur_tag.state == TagState.ARBITRATE:
                    if cur_tag.slot_counter == 0:
                        print("ERROR: Tag slot counter is 0 in the ARBITRATE state!")
                        pass
                    else:
                        cur_tag.slot_counter -= 1

        else:
            pass


        # update global timestamp
        prev_time = cur_time
        new_time = cur_time + reader.next_state()
        heappush(self.pq, (reader, new_time, cur_time))

        # print("cur_time: " + "{:.6f}".format(cur_time) + ", Reader State: " + str(reader.state))

        self.timestamp_prev.append(prev_time)
        self.timestamp_cur.append(new_time)
        self.reader_state.append(reader.state)

        return cur_time



#####
#####
RUN_TIME = 5.0e-3
NUM_TAG = 1

reader = Reader(1, (0, 0), ReaderState.SELECT)

tags_list = []
for tag_id in range(NUM_TAG):
    tags_list.append(Tag(tag_id, (0,0), TagState.ARBITRATE))

te = TimedEvents(reader, tags_list)

while te.process_event() < RUN_TIME:
    pass

plt.figure()
for idx in range(len(te.reader_state)):
    plt.plot([te.timestamp_prev[idx],te.timestamp_cur[idx]],
             [te.reader_state[idx],te.reader_state[idx]],
             linewidth=2.0)

plt.title("Reader Schedule")

plt.xlim(0.0, RUN_TIME)
plt.xlabel("Time (second)")

plt.ylim(0.0, 50)
plt.yticks([ReaderState.IDLE, ReaderState.SELECT, ReaderState.SELECT_RX, ReaderState.QUERY, ReaderState.QUERY_RX, ReaderState.QUERY_REP, ReaderState.ACK, ReaderState.ACK_RX],
           ['IDLE', 'SELECT', 'SELECT_RX', 'QUERY', 'QUERY_RX', 'QUERY_REP', 'ACK', 'ACK_RX'],
           rotation=45)
plt.ylabel("Reader State")

plt.show()
