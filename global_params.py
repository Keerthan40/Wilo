#!/usr/bin/python3

# Parameters from Section 5 of
# https://cdn.sparkfun.com/assets/learn_tutorials/6/1/3/Gen2_Protocol_Standard.pdf

# https://www.gs1.org/sites/default/files/docs/epc/Gen2_Protocol_Standard.pdf

# Divide ratio (Table 6.9)
DR = 8.0
# Tag-to-Interrogator calibration symbol
TRCAL = 25e-6 # (sec)

# Interrogator-to-Tag calibration symbol
# 1.1 * TRcal <= RTcal <= 3.0 * TRcal
RTCAL = 2.0 * TRCAL

# Backscatter-link frequency (BLF = 1/Tpri = DR/TRcal)
BLF = DR/TRCAL # (Hz)
TPRI = 1.0/BLF

# Table 6.16
# Time from Interrogator transmission to Tag response for an immediate Tag reply
T1 = max(TRCAL, 10.0 * TPRI)

# Time from Tag response to Interrogator transmission
# 3.0 * Tpri <= T2 <= 20.0 * Tpri
T2 = 5.0 * TPRI

# Time an Interrogator waits, after T1, before it issues another command
T3 = 0.0 * TPRI

# Minimum time between Interrogator commands
T4 = 2.0 * RTCAL

# Time from Interrogator transmission to Tag response for a delayed Tag reply
T5 = 0.0

# Time from Interrogator transmission to first Tag response for an in-process Tag reply
T6 = 0.0


QUERY_BITS = 22
RN16_BITS = 16
