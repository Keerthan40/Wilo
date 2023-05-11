#!/usr/bin/python3

from global_params import *
import time
import datetime
from tag import *
''' Class of Reader states'''
class ReaderState(object):
    IDLE = 0
    
    
    SLEEP_SAMPLE = 5
    SAMPLE_DATA = 10
    # SELECT command: variable length
    # 1010 (4) | Target (3) | Action (3) | MemBank (2) | Pointer (EBV) |
    # Length (8) | Mask (variable) | Truncate (1) | CRC (16) |

    # QUERY command: 22 bits
    # 1000 (4) | DR (1) | M (2) | TRext (1) | Sel (2) | Session (2) | Target (1) | Q (4) | CRC (5) |
    SLEEP_QUERY = 15
    QUERY = 20
    # Tag Reply command: 16 bits
    # RN16 (16)
    QUERY_RX = 25

    QUERY_REP = 30
    QUERY_REP_RX = 35
    QUERY_ACK = 40
    QUERY_ACK_RX = 45
    QUERY_RN16 = 50 # fix?
    QUERY_REQ_RN16 = 55
    TAG_ID = 60
    TAG_ID_RX = 65   
    
    SLEEP_SENSOR_DATA = 70
    SELECT = 75
    SELECT_RX = 80
    SENSOR_DATA = 85
    SENSOR_DATA_RX = 90
    SENSOR_DATA_ACK = 95
    SENSOR_DATA_ACK_RX = 100
    SENSOR_DATA_RN16 = 105
    SENSOR_DATA_REQ_RN16 = 110
    DATA = 115
    SAMPLE_DATA_RX = 120
    SELECT_QUERY = 125
    SELECT_RX_QUERY = 130
''' Class of Reader params'''
class ReaderParam(object):

    # timing
    timing = {ReaderState.SELECT: 1,
              ReaderState.QUERY: QUERY_BITS/BLF,
              ReaderState.QUERY_RN16: RN16_BITS/BLF,
              ReaderState.SENSOR_DATA_RN16: RN16_BITS/BLF,
              ReaderState.QUERY_REQ_RN16:RN16_BITS/BLF,
              ReaderState.SENSOR_DATA_REQ_RN16:RN16_BITS/BLF,
              ReaderState.QUERY_REP: 1,
              ReaderState.QUERY_ACK: 1,
              ReaderState.SENSOR_DATA_ACK:1,
              ReaderState.SAMPLE_DATA: 1,
              ReaderState.SENSOR_DATA:1,
              ReaderState.SLEEP_SAMPLE:1,
              ReaderState.SLEEP_QUERY: 6,
              ReaderState.SLEEP_SENSOR_DATA: 12}

    rf = {'TX_POWER': 0.0}


''' Reader object'''
class Reader(object):
    def __init__(self, ID, loc, state):
        self.ID = ID
        self.loc = loc
        self.state = state

    ''' Reader state transition
    '''
    def next_state(self,counter,tag_list,temp2):
        
        if self.state == ReaderState.SLEEP_SAMPLE:
            print(self.state)
            
            self.state = ReaderState.SAMPLE_DATA
            return ReaderParam.timing[ReaderState.SLEEP_SAMPLE]
        elif self.state == ReaderState.SAMPLE_DATA:
            print(self.state)
            self.state = ReaderState.SLEEP_SAMPLE
            print(counter)
            if counter%4==0 and counter>0:
                self.state = ReaderState.SELECT_QUERY
            
            return T1 + ReaderParam.timing[ReaderState.SLEEP_SAMPLE]
        elif self.state == ReaderState.SAMPLE_DATA_RX:
            print(self.state)
            self.state = ReaderState.SLEEP_SAMPLE
            return ReaderParam.timing[ReaderState.SLEEP_SAMPLE]
        elif self.state == ReaderState.SELECT_QUERY:
             print(self.state)
            
             self.state = ReaderState.SELECT_RX_QUERY
             return ReaderParam.timing[ReaderState.SELECT]
        elif self.state == ReaderState.SELECT_RX_QUERY:
            print(self.state)
            self.state = ReaderState.QUERY
            return ReaderParam.timing[ReaderState.SELECT]
        elif self.state == ReaderState.QUERY:
            print(self.state)
            self.state = ReaderState.QUERY_RX
            return T1 + ReaderParam.timing[ReaderState.QUERY_ACK] + T2
        elif self.state == ReaderState.QUERY_RX:
            print(self.state)
            self.state = ReaderState.QUERY_ACK
            return T1 + ReaderParam.timing[ReaderState.QUERY_ACK] + T2
        elif self.state == ReaderState.QUERY_ACK:
            print(self.state)
            self.state = ReaderState.QUERY_ACK_RX
            return 1#T1 + T3
        elif self.state == ReaderState.QUERY_ACK_RX:
            print(self.state)
            self.state = ReaderState.QUERY_REQ_RN16
            return 1#ReaderParam.timing[ReaderState.QUERY_REQ_RN16]
        elif self.state == ReaderState.QUERY_REQ_RN16:
            print(self.state)
                
            # if counter%48 == 0:
            #         self.state = ReaderState.SELECT            
            
            self.state = ReaderState.TAG_ID
            return 1#T1 + ReaderParam.timing[ReaderState.QUERY_RN16] + T2
        elif self.state == ReaderState.TAG_ID:
            print(self.state)
            self.state = ReaderState.TAG_ID_RX
            return 1
        elif self.state == ReaderState.TAG_ID_RX:
            print(self.state)
            print("len of tag_list",len(tag_list))
            if len(temp2)!=0:
                self.state = ReaderState.SELECT_QUERY
                temp2.pop()
            if len(temp2)==0:
                for cur_tag in tag_list:
                    temp2.append(cur_tag)
                if counter%48 !=0:
                    self.state = ReaderState.SLEEP_SAMPLE
                elif counter%48 == 0 and counter>0:
                    self.state = ReaderState.SELECT 
            # if counter%48 == 0:
            #     self.state = ReaderState.SELECT
            return ReaderParam.timing[ReaderState.SLEEP_SAMPLE]
        elif self.state == ReaderState.SLEEP_QUERY:
            print(self.state)
            
            self.state = ReaderState.SELECT_QUERY
            return 1#ReaderParam.timing[ReaderState.QUERY]

        elif self.state == ReaderState.SELECT:
            print(self.state)
            self.state = ReaderState.SELECT_RX
            return ReaderParam.timing[ReaderState.SELECT]

        elif self.state == ReaderState.SELECT_RX:
            print(self.state)
            self.state = ReaderState.SENSOR_DATA
            return ReaderParam.timing[ReaderState.SENSOR_DATA]
        elif self.state == ReaderState.SENSOR_DATA:
            self.state = ReaderState.SENSOR_DATA_RX
            return 1#T1 + ReaderParam.timing[ReaderState.SENSOR_DATA_RN16] + T2
        elif self.state == ReaderState.SENSOR_DATA_RX:
            self.state = ReaderState.SENSOR_DATA_ACK
            return 1#T1 + ReaderParam.timing[ReaderState.SENSOR_DATA_RN16] + T2
        elif self.state == ReaderState.SENSOR_DATA_ACK:
            self.state = ReaderState.SENSOR_DATA_ACK_RX
            return 1#T1 + T3
        elif self.state == ReaderState.SENSOR_DATA_ACK_RX:
            self.state = ReaderState.SENSOR_DATA_REQ_RN16
            return 1#ReaderParam.timing[ReaderState.SENSOR_DATA_REQ_RN16]
        elif self.state == ReaderState.SENSOR_DATA_REQ_RN16:
            self.state = ReaderState.DATA
            return 1#T1 + ReaderParam.timing[ReaderState.SENSOR_DATA_RN16] + T2
        elif self.state == ReaderState.DATA:
            if len(temp2)!=0:
                self.state = ReaderState.SELECT
                temp2.pop()
            if len(temp2)==0:
                for cur_tag in tag_list:
                    temp2.append(cur_tag)
                self.state = ReaderState.SLEEP_SAMPLE          
            return ReaderParam.timing[ReaderState.SLEEP_SAMPLE]
        elif self.state == ReaderState.SLEEP_SENSOR_DATA:
            self.state = ReaderState.SLEEP_SAMPLE
            return ReaderParam.timing[ReaderState.SELECT]
        else:
            return 0.0

    ''' Reader operation
    '''

    def query(self, Q):
        return Q
