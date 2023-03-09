#!/usr/bin/python3

from global_params import *
import time

''' Class of Reader states'''
class ReaderState(object):
    IDLE = 0
    SLEEP = 5
    # SELECT command: variable length
    # 1010 (4) | Target (3) | Action (3) | MemBank (2) | Pointer (EBV) |
    # Length (8) | Mask (variable) | Truncate (1) | CRC (16) |
    SELECT = 10

    SELECT_RX = 15

    # QUERY command: 22 bits
    # 1000 (4) | DR (1) | M (2) | TRext (1) | Sel (2) | Session (2) | Target (1) | Q (4) | CRC (5) |
    QUERY = 20

    # Tag Reply command: 16 bits
    # RN16 (16)
    QUERY_RX = 25

    QUERY_REP = 30
    QUERY_REP_RX = 35
    ACK = 40
    ACK_RX = 45
    RN16 = 50 # fix?
    SAMPLE_DATA = 55
    SENSOR_DATA = 60 
    SENSOR_DATA_RX = 65
    SENSOR_DATA_ACK = 70
    SENSOR_DATA_ACK_RX = 75
    Req_RN16 = 80
    Tag_ID = 85

''' Class of Reader params'''
class ReaderParam(object):

    # timing
    timing = {ReaderState.SELECT: 0.01,
              ReaderState.QUERY: QUERY_BITS/BLF,
              ReaderState.RN16: RN16_BITS/BLF,
              ReaderState.Req_RN16:RN16_BITS/BLF,
              ReaderState.QUERY_REP: 0.01,
              ReaderState.ACK: 0.01,
              ReaderState.SAMPLE_DATA: 0.01,
              ReaderState.SENSOR_DATA:0.01,
              ReaderState.SLEEP:0.00001}

    rf = {'TX_POWER': 0.0}


''' Reader object'''
class Reader(object):
    def __init__(self, ID, loc, state):
        self.ID = ID
        self.loc = loc
        self.state = state
        
        self.last_command_15min = 0
        self.last_command_1hour = 0
        self.last_command_12hour = 0

    ''' Reader state transition
    '''
    def next_state(self):
        current_time = time.time()
        if self.state == ReaderState.SLEEP:
            if current_time - self.last_command_15min >= 15 * 60:
                self.state == ReaderState.SAMPLE_DATA
                self.last_command_15min = current_time
                return ReaderParam.timing[ReaderState.SAMPLE_DATA]
            if current_time - self.last_command_1hour>= 60*60:
                self.state == ReaderState.QUERY
                self.last_command_1hour = current_time
                return ReaderParam.timing[ReaderState.QUERY]
            if current_time - self.last_command_12hour>=12*60*60:
                self.state == ReaderState.SELECT
                self.last_command_12hour = current_time
                return ReaderParam.timing[ReaderState.SELECT]
        elif self.state == ReaderState.SAMPLE_DATA:
            self.state = ReaderState.SLEEP
            return ReaderParam.timing[ReaderState.SLEEP]
        elif self.state == ReaderState.QUERY:
            self.state = ReaderState.QUERY_RX
            return T1 + ReaderParam.timing[ReaderState.RN16] + T2
        elif self.state == ReaderState.QUERY_RX:
            self.state = ReaderState.ACK
            return T1 + ReaderParam.timing[ReaderState.RN16] + T2
        elif self.state == ReaderState.ACK:
            self.state = ReaderState.ACK_RX
            return T1 + T3
        elif self.state == ReaderState.ACK_RX:
            self.state = ReaderState.Req_RN16
            return ReaderParam.timing[ReaderState.Req_RN16]
        elif self.state == ReaderState.Req_RN16:
            self.state = ReaderState.Tag_ID
            return T1 + ReaderParam.timing[ReaderState.RN16] + T2
        
        
        if self.state == ReaderState.SELECT:
            self.state = ReaderState.SELECT_RX
            return T4

        elif self.state == ReaderState.SELECT_RX:
            self.state = ReaderState.QUERY
            return ReaderParam.timing[ReaderState.QUERY]

        else:
            return 0.0

    ''' Reader operation
    '''

    def query(self, Q):
        return Q
