#!/usr/bin/python3

import random
from global_params import *

''' Class of tag states'''
class TagState(object):
    READY = 0
    ARBITRATE = 1
    REPLY = 2
    ACKNOWLEDGED = 3
    OPEN = 4
    SECURED = 5
    KILLED = 6


''' Class of tag radio states'''
class TagRadioState(object):
    SLEEP = 0
    LISTEN = 1
    RECEIVE = 2
    TRANSMIT = 3


''' Class of Tag params'''
class TagParam(object):

    # power consumptino in nW
    power = {TagRadioState.SLEEP: 0.0,
             TagRadioState.LISTEN: 0.01,
             TagRadioState.RECEIVE: 0.01,
             TagRadioState.TRANSMIT: 0.02}

    # RF characteristics
    rf = {'RSSI': -999.9}


''' Tag object'''
class Tag(object):
    def __init__(self, ID, loc, state):
        self.ID = ID
        self.loc = loc
        self.state = state
        self.slot_counter = 0

        self.flag_SL = 0
        self.flag_inventorized = 0

    # following the state transitions in Annex B and C:
    # https://cdn.sparkfun.com/assets/learn_tutorials/6/1/3/Gen2_Protocol_Standard.pdf
    def next_state(self, next_state):

        # READY (Sec. 6.3.2.6.1)
        if self.state == TagState.READY:
            if self.slot_counter == 0:
                self.state = TagState.REPLY
            else:
                self.state = TagState.ARBITRATE
        # ARBITRATE (Sec. 6.3.2.6.2)
        elif self.state == TagState.ARBITRATE:
            if self.slot_counter == 0:
                self.state = TagState.REPLY
            elif self.slot_counter != 0:
                self.slot_counter = self.slot_counter - 1
        # REPLY (Sec. 6.3.2.6.3)
        elif self.state == TagState.REPLY:
            # TODO: if receving an ack from the reader
            # now assume that the acking is always successful
            if true:
                self.state = TagState.ACKNOWLEDGED
            else:
                self.state = TagState.ARBITRATE
        # ACKNOWLEDGED (Sec. 6.3.2.6.4)
        elif self.state == TagState.ACKNOWLEDGED:
            # TODO:
            if ture:
                self.state = TagState.READY
            else:
                self.state = TagState.ARBITRATE
        else:
            pass

    # (pseudo-) random number generator
    def rng(self, query_q):
        self.slot_counter = random.randint(0, 2**query_q-1)
        pass
