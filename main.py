#!/usr/bin/python3

from heapq import *

import numpy as np

import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt

from global_params import *
from reader import *
from tag import *
counter = 15
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
        self.tag_state = []
        self.counter = -1
        # event of the reader, current event time, previous event time
        heappush(self.pq, (reader, 0.0, -1.0))
        self.timestamp_prev.append(-1.0)
        self.timestamp_cur.append(0.0)
        self.reader_state.append(0)
        self.tag_state.append(0)
        #self.temp1 = tags_list

    def identify_selected_tags(self):
        # Initialize an empty list to store the selected tags
        selected_tags_list = []
        for cur_tag in self.tags_list:
            #print("curr_tag inventeroid:",cur_tag.flag_inventorized)                              #Add range parameter
            if cur_tag.flag_inventorized==0 and cur_tag.flag_SL==0:
               selected_tags_list.append(cur_tag)
        return selected_tags_list
    def process_event(self,temp2):
        # pop the current reader event that has already finished
        # with the format (reader state, current event time, previous event time)
        (reader, cur_time, prev_time) = heappop(self.pq)
        #cur_selected_tags_list = self.identify_selected_tags()
        print("counter",self.counter)

        # update global timestamp
        prev_time = cur_time
        if reader.state == ReaderState.SLEEP_SAMPLE:
            self.counter = self.counter+1       
        # if reader.state == ReaderState.TAG_ID:
        #     tags_list[0].state = TagState.REPLY
        for cur_tag in tags_list:
            if reader.state == ReaderState.TAG_ID:
                cur_tag.next_state()
        for cur_tag in tags_list:
            if reader.state == ReaderState.TAG_ID_RX:
                cur_tag.next_state()
        for cur_tag in tags_list:
            if reader.state == ReaderState.SELECT or (reader.state == ReaderState.SLEEP_SAMPLE and cur_tag.state == TagState.ACKNOWLEDGED):
                cur_tag.next_state()
        
        
        new_time = cur_time + reader.next_state(self.counter,tags_list,temp2)
        
        print("timer",new_time)
        heappush(self.pq, (reader, new_time, cur_time))
        
        # print("cur_time: " + "{:.6f}".format(cur_time) + ", Reader State: " + str(reader.state))

        self.timestamp_prev.append(prev_time)
        self.timestamp_cur.append(new_time)
        self.reader_state.append(reader.state)
        for cur_tag in tags_list:
            self.tag_state.append(cur_tag.state) 


        return cur_time



#####
#####
RUN_TIME = 100
NUM_TAG = 1

reader = Reader(1, (0, 0), ReaderState.SAMPLE_DATA)
temp2 = []
tags_list = []

for tag_id in range(NUM_TAG):
    tags_list.append(Tag(tag_id, (0,0), TagState.READY))
    #temp2.append(Tag(tag_id, (0,0), TagState.READY))
for tag_id in range(NUM_TAG):
    temp2.append(Tag(tag_id, (0,0), TagState.READY))
te = TimedEvents(reader, tags_list)
print(RUN_TIME)
while te.process_event(temp2) < RUN_TIME:
    #print(reader.state)
    pass

plt.figure()
for idx in range(len(te.reader_state)):
    plt.plot([te.timestamp_prev[idx],te.timestamp_cur[idx]],
             [te.reader_state[idx],te.reader_state[idx]],
             linewidth=2.0)

plt.title("Reader Schedule")

plt.xlim(0.0, RUN_TIME)


plt.ylim(0.0, 50)
plt.yticks([ReaderState.IDLE, ReaderState.SLEEP_SAMPLE,ReaderState.SAMPLE_DATA,ReaderState.SLEEP_QUERY, ReaderState.QUERY, ReaderState.QUERY_RX, ReaderState.QUERY_REP, ReaderState.QUERY_ACK, ReaderState.QUERY_ACK_RX, ReaderState.QUERY_REQ_RN16, ReaderState.TAG_ID,ReaderState.SLEEP_SENSOR_DATA, ReaderState.SELECT, ReaderState.SELECT_RX,ReaderState.SENSOR_DATA,
            ReaderState.SENSOR_DATA_RX ,ReaderState.SENSOR_DATA_ACK,ReaderState.SENSOR_DATA_ACK_RX, ReaderState.SENSOR_DATA_REQ_RN16, ReaderState.DATA],
           ['IDLE','SLEEP_SAMPLE','SAMPLE_DATA','SLEEP_QUERY', 'QUERY', 'QUERY_RX', 'QUERY_REP', 'QUERY_ACK', 'QUERY_ACK_RX','QUERY_REQ_RN16','TAG_ID','SLEEP_SENSOR_DATA', 'SELECT', 'SELECT_RX','SENSOR_DATA','SENSOR_DATA_RX','SENSOR_DATA_ACK','SENSOR_DATA_ACK_RX','SENSOR_DATA_REQ_RN16', 'DATA'],
           rotation=45)
# plt.yticks([TagState.READY,TagState.ARBITRATE,TagState.REPLY,TagState.ACKNOWLEDGED],
#            ['READY','ARBITRATE','REPLY','ACKNOWLEDGED'],
#            rotation=45)
plt.ylabel("Reader State")

plt.show()
print(len(te.tag_state))
print(len(te.timestamp_prev))
for idx in range(len(te.tag_state)):
    plt.plot([te.timestamp_prev[idx],te.timestamp_cur[idx]],
             [te.tag_state[idx],te.tag_state[idx]],
             linewidth=2.0)

plt.title("Tag Schedule")

plt.xlim(0.0, RUN_TIME)


plt.ylim(0.0, 50)
# plt.yticks([ReaderState.IDLE, ReaderState.SLEEP_SAMPLE,ReaderState.SAMPLE_DATA,ReaderState.SLEEP_QUERY, ReaderState.QUERY, ReaderState.QUERY_RX, ReaderState.QUERY_REP, ReaderState.QUERY_ACK, ReaderState.QUERY_ACK_RX, ReaderState.QUERY_REQ_RN16, ReaderState.TAG_ID,ReaderState.SLEEP_SENSOR_DATA, ReaderState.SELECT, ReaderState.SELECT_RX,ReaderState.SENSOR_DATA,
#             ReaderState.SENSOR_DATA_RX ,ReaderState.SENSOR_DATA_ACK,ReaderState.SENSOR_DATA_ACK_RX, ReaderState.SENSOR_DATA_REQ_RN16, ReaderState.DATA],
#            ['IDLE','SLEEP_SAMPLE','SAMPLE_DATA','SLEEP_QUERY', 'QUERY', 'QUERY_RX', 'QUERY_REP', 'QUERY_ACK', 'QUERY_ACK_RX','QUERY_REQ_RN16','TAG_ID','SLEEP_SENSOR_DATA', 'SELECT', 'SELECT_RX','SENSOR_DATA','SENSOR_DATA_RX','SENSOR_DATA_ACK','SENSOR_DATA_ACK_RX','SENSOR_DATA_REQ_RN16', 'DATA'],
#            rotation=45)
plt.yticks([TagState.READY,TagState.REPLY,TagState.ACKNOWLEDGED],
            ['READY','REPLY','ACKNOWLEDGED'],
            rotation=45)
plt.ylabel("Tag State")

plt.show()
