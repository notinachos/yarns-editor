# -*- coding: utf-8 -*-

'''
The MIT License (MIT)

Copyright (c) 2015 Panagiotis Peppas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Notice:
Portions of this software may include text and/or graphics from Mutable Instruments, 
provided under the cc-by-sa 3.0 license. The author of this software is not 
endorsed by Mutable Instruments. Their company website, and the license, can be 
found at the following address: http://mutable-instruments.net/
'''

# cc map 
controllers = {
    # global
    'yarns_layout': 1,
    'yarns_tempo':  2,
    'yarns_swing':  3,

    # part 1
    'part1_midiChannel':     4,
    'part1_lowerNote':       5,
    'part1_upperNote':       6,
    'part1_midiOutMode':     7,
    'part1_voicing':         8,
    'part1_notePriority':    9,
    'part1_portamento':      10,
    'part1_legato':          11,
    'part1_pitchBendRange':  12,
    'part1_vibratoRange':    13,
    'part1_vibratoSpeed':    14,
    'part1_transpose':       15,
    'part1_fineTuning':      16,
    'part1_tuningRoot':      17,
    'part1_tuningSystem':    18,
    'part1_triggerDuration': 19,
    'part1_velocityScale':   20,
    'part1_triggerShape':    21,
    'part1_auxCVout':        22,
    'part1_oscillatorShape': 23,
    'part1_arpClockDiv':     24,
    'part1_arpGateLength':   25,
    'part1_arpRange':        26,
    'part1_arpDirection':    27,
    'part1_arpPattern':      28,
    'part1_euclideanLength': 29,
    'part1_euclideanFill':   30,
    'part1_euclideanRotate': 31,

    # part 2
    'part2_midiChannel':     36,
    'part2_lowerNote':       37,
    'part2_upperNote':       38,
    'part2_midiOutMode':     39,
    'part2_voicing':         40,
    'part2_notePriority':    41,
    'part2_portamento':      42,
    'part2_legato':          43,
    'part2_pitchBendRange':  44,
    'part2_vibratoRange':    45,
    'part2_vibratoSpeed':    46,
    'part2_transpose':       47,
    'part2_fineTuning':      48,
    'part2_tuningRoot':      49,
    'part2_tuningSystem':    50,
    'part2_triggerDuration': 51,
    'part2_velocityScale':   52,
    'part2_triggerShape':    53,
    'part2_auxCVout':        54,
    'part2_oscillatorShape': 55,
    'part2_arpClockDiv':     56,
    'part2_arpGateLength':   57,
    'part2_arpRange':        58,
    'part2_arpDirection':    59,
    'part2_arpPattern':      60,
    'part2_euclideanLength': 61,
    'part2_euclideanFill':   62,
    'part2_euclideanRotate': 63,

    # part 3
    'part3_midiChannel':     68,
    'part3_lowerNote':       69,
    'part3_upperNote':       70,
    'part3_midiOutMode':     71,
    'part3_voicing':         72,
    'part3_notePriority':    73,
    'part3_portamento':      74,
    'part3_legato':          75,
    'part3_pitchBendRange':  76,
    'part3_vibratoRange':    77,
    'part3_vibratoSpeed':    78,
    'part3_transpose':       79,
    'part3_fineTuning':      80,
    'part3_tuningRoot':      81,
    'part3_tuningSystem':    82,
    'part3_triggerDuration': 83,
    'part3_velocityScale':   84,
    'part3_triggerShape':    85,
    'part3_auxCVout':        86,
    'part3_oscillatorShape': 87,
    'part3_arpClockDiv':     88,
    'part3_arpGateLength':   89,
    'part3_arpRange':        90,
    'part3_arpDirection':    91,
    'part3_arpPattern':      92,
    'part3_euclideanLength': 93,
    'part3_euclideanFill':   94,
    'part3_euclideanRotate': 95,

    # part 4
    'part4_midiChannel':     100,
    'part4_lowerNote':       101,
    'part4_upperNote':       102,
    'part4_midiOutMode':     103,
    'part4_voicing':         104,
    'part4_notePriority':    105,
    'part4_portamento':      106,
    'part4_legato':          107,
    'part4_pitchBendRange':  108,
    'part4_vibratoRange':    109,
    'part4_vibratoSpeed':    110,
    'part4_transpose':       111,
    'part4_fineTuning':      112,
    'part4_tuningRoot':      113,
    'part4_tuningSystem':    114,
    'part4_triggerDuration': 115,
    'part4_velocityScale':   116,
    'part4_triggerShape':    117,
    'part4_auxCVout':        118,
    'part4_oscillatorShape': 119,
    'part4_arpClockDiv':     120,
    'part4_arpGateLength':   121,
    'part4_arpRange':        122,
    'part4_arpDirection':    123,
    'part4_arpPattern':      124,
    'part4_euclideanLength': 125,
    'part4_euclideanFill':   126,
    'part4_euclideanRotate': 127}

# layout/cc value map
layout = {
    '1M - Monophonic':                 1,
    '2M - Dual monophonic':           13, 
    '4M - Quad monophonic':           26,
    '2P - Duophonic':                 39,
    '4P - Quadraphonic':              52,
    '2> - Duophonic polychaining':    64,
    '4> - Quadraphonic polychaining': 77,
    '8> - Octophonic polychaining':   90,
    '4T - Quad trigger':              103,
    '3+ - Three plus one':            116}

# tempo/cc value map
tempo = {
    'External MIDI clock': 0,
    '40': 1, 
    '42': 2, 
    '44': 4, 
    '46': 5, 
    '48': 6, 
    '50': 7, 
    '52': 9, 
    '54': 10, 
    '56': 11, 
    '58': 13, 
    '60': 14, 
    '62': 15, 
    '64': 16, 
    '66': 18, 
    '68': 19, 
    '70': 20, 
    '72': 21, 
    '74': 23, 
    '76': 24, 
    '78': 25, 
    '80': 26, 
    '82': 28, 
    '84': 29, 
    '86': 30, 
    '88': 32, 
    '90': 33, 
    '92': 34, 
    '94': 35, 
    '96': 37, 
    '98': 38, 
    '100': 39, 
    '102': 40, 
    '104': 42, 
    '106': 43, 
    '108': 44, 
    '110': 45, 
    '112': 47, 
    '114': 48, 
    '116': 49, 
    '118': 51, 
    '120': 52, 
    '122': 53, 
    '124': 54, 
    '126': 56, 
    '128': 57,
    '130': 58, 
    '132': 59, 
    '134': 61, 
    '136': 62, 
    '138': 63, 
    '140': 64, 
    '142': 66, 
    '144': 67, 
    '146': 68, 
    '148': 70, 
    '150': 71, 
    '152': 72, 
    '154': 73, 
    '156': 75, 
    '158': 76, 
    '160': 77, 
    '162': 78, 
    '164': 80, 
    '166': 81, 
    '168': 82, 
    '170': 84, 
    '172': 85, 
    '174': 86, 
    '176': 87, 
    '178': 89, 
    '180': 90, 
    '182': 91, 
    '184': 92, 
    '186': 94, 
    '188': 95, 
    '190': 96, 
    '192': 97, 
    '194': 99, 
    '196': 100, 
    '198': 101, 
    '200': 103, 
    '202': 104, 
    '204': 105, 
    '206': 106, 
    '208': 108, 
    '210': 109, 
    '212': 110, 
    '214': 111, 
    '216': 113, 
    '218': 114, 
    '220': 115, 
    '222': 116, 
    '224': 118, 
    '226': 119, 
    '228': 120, 
    '230': 122, 
    '232': 123, 
    '234': 124, 
    '236': 125, 
    '238': 127}

# swing/cc value map
swing = {
    '0': 0, 
    '1': 2, 
    '2': 3, 
    '3': 4, 
    '4': 6, 
    '5': 7, 
    '6': 8, 
    '7': 9, 
    '8': 11, 
    '9': 12, 
    '10': 13, 
    '11': 15, 
    '12': 16, 
    '13': 17, 
    '14': 18, 
    '15': 20, 
    '16': 21, 
    '17': 22, 
    '18': 24, 
    '19': 25, 
    '20': 26, 
    '21': 27, 
    '22': 29, 
    '23': 30, 
    '24': 31, 
    '25': 32, 
    '26': 34, 
    '27': 35, 
    '28': 36, 
    '29': 38, 
    '30': 39, 
    '31': 40, 
    '32': 41, 
    '33': 43, 
    '34': 44, 
    '35': 45, 
    '36': 47, 
    '37': 48, 
    '38': 49, 
    '39': 50,
    '40': 52, 
    '41': 53, 
    '42': 54, 
    '43': 56, 
    '44': 57, 
    '45': 58, 
    '46': 59, 
    '47': 61, 
    '48': 62, 
    '49': 63, 
    '50': 64, 
    '51': 66, 
    '52': 67, 
    '53': 68, 
    '54': 70, 
    '55': 71, 
    '56': 72, 
    '57': 73, 
    '58': 75, 
    '59': 76, 
    '60': 77, 
    '61': 79, 
    '62': 80, 
    '63': 81, 
    '64': 82, 
    '65': 84, 
    '66': 85, 
    '67': 86, 
    '68': 88, 
    '69': 89, 
    '70': 90, 
    '71': 91, 
    '72': 93, 
    '73': 94, 
    '74': 95, 
    '75': 96, 
    '76': 98, 
    '77': 99, 
    '78': 100, 
    '79': 102, 
    '80': 103, 
    '81': 104, 
    '82': 105, 
    '83': 107, 
    '84': 108, 
    '85': 109, 
    '86': 111, 
    '87': 112, 
    '88': 113, 
    '89': 114, 
    '90': 116, 
    '91': 117, 
    '92': 118, 
    '93': 120, 
    '94': 121, 
    '95': 122, 
    '96': 123, 
    '97': 125, 
    '98': 126, 
    '99': 127}

# portamento/cc value map
portamento = {
    '0': 0, 
    '1': 2, 
    '2': 3, 
    '3': 4, 
    '4': 6, 
    '5': 7, 
    '6': 8, 
    '7': 9, 
    '8': 11, 
    '9': 12, 
    '10': 13, 
    '11': 15, 
    '12': 16, 
    '13': 17, 
    '14': 18, 
    '15': 20, 
    '16': 21, 
    '17': 22, 
    '18': 24, 
    '19': 25, 
    '20': 26, 
    '21': 27, 
    '22': 29, 
    '23': 30, 
    '24': 31, 
    '25': 32, 
    '26': 34, 
    '27': 35, 
    '28': 36, 
    '29': 38, 
    '30': 39, 
    '31': 40, 
    '32': 41, 
    '33': 43, 
    '34': 44, 
    '35': 45, 
    '36': 47, 
    '37': 48, 
    '38': 49, 
    '39': 50,
    '40': 52, 
    '41': 53, 
    '42': 54, 
    '43': 56, 
    '44': 57, 
    '45': 58, 
    '46': 59, 
    '47': 61, 
    '48': 62, 
    '49': 63, 
    '50': 64, 
    '51': 66, 
    '52': 67, 
    '53': 68, 
    '54': 70, 
    '55': 71, 
    '56': 72, 
    '57': 73, 
    '58': 75, 
    '59': 76, 
    '60': 77, 
    '61': 79, 
    '62': 80, 
    '63': 81, 
    '64': 82, 
    '65': 84, 
    '66': 85, 
    '67': 86, 
    '68': 88, 
    '69': 89, 
    '70': 90, 
    '71': 91, 
    '72': 93, 
    '73': 94, 
    '74': 95, 
    '75': 96, 
    '76': 98, 
    '77': 99, 
    '78': 100, 
    '79': 102, 
    '80': 103, 
    '81': 104, 
    '82': 105, 
    '83': 107, 
    '84': 108, 
    '85': 109, 
    '86': 111, 
    '87': 112, 
    '88': 113, 
    '89': 114, 
    '90': 116, 
    '91': 117, 
    '92': 118, 
    '93': 120, 
    '94': 121, 
    '95': 122, 
    '96': 123, 
    '97': 125, 
    '98': 126, 
    '99': 127}

# channel/cc value map
channel = {
    '1': 1,
    '2': 8,
    '3': 16,
    '4': 23,
    '5': 31,
    '6': 38,
    '7': 46,
    '8': 53,
    '9': 61,
    '10': 68,
    '11': 76,
    '12': 83,
    '13': 91,
    '14': 98,
    '15': 106,
    '16': 113}

# note/cc value map
note = {
    '0 - C_0':     0, 
    '1 - Db_0':    1, 
    '2 - D_0':     2, 
    '3 - Eb_0':    3, 
    '4 - E_0':     4, 
    '5 - F_0':     5, 
    '6 - Gb_0':    6, 
    '7 - G_0':     7, 
    '8 - Ab_0':    8, 
    '9 - A_0':     9, 
    '10 - B_0':    10, 
    '11 - Bb_0':   11,
    '12 - C_1':    12, 
    '13 - Db_1':   13, 
    '14 - D_1':    14, 
    '15 - Eb_1':   15, 
    '16 - E_1':    16,
    '17 - F_1':    17, 
    '18 - Gb_1':   18, 
    '19 - G_1':    19, 
    '20 - Ab_1':   20, 
    '21 - A_1':    21,
    '22 - B_1':    22, 
    '23 - Bb_1':   23, 
    '24 - C_2':    24, 
    '25 - Db_2':   25, 
    '26 - D_2':    26,
    '27 - Eb_2':   27, 
    '28 - E_2':    28, 
    '29 - F_2':    29, 
    '30 - Gb_2':   30, 
    '31 - G_2':    31,
    '32 - Ab_2':   32, 
    '33 - A_2':    33, 
    '34 - B_2':    34, 
    '35 - Bb_2':   35, 
    '36 - C_3':    36,
    '37 - Db_3':   37, 
    '38 - D_3':    38, 
    '39 - Eb_3':   39, 
    '40 - E_3':    40, 
    '41 - F_3':    41,
    '42 - Gb_3':   42, 
    '43 - G_3':    43, 
    '44 - Ab_3':   44, 
    '45 - A_3':    45, 
    '46 - B_3':    46,
    '47 - Bb_3':   47, 
    '48 - C_4':    48, 
    '49 - Db_4':   49, 
    '50 - D_4':    50, 
    '51 - Eb_4':   51,
    '52 - E_4':    52, 
    '53 - F_4':    53, 
    '54 - Gb_4':   54, 
    '55 - G_4':    55, 
    '56 - Ab_4':   56,
    '57 - A_4':    57, 
    '58 - B_4':    58, 
    '59 - Bb_4':   59, 
    '60 - C_5':    60, 
    '61 - Db_5':   61,
    '62 - D_5':    62, 
    '63 - Eb_5':   63, 
    '64 - E_5':    64, 
    '65 - F_5':    65, 
    '66 - Gb_5':   66,
    '67 - G_5':    67, 
    '68 - Ab_5':   68, 
    '69 - A_5':    69, 
    '70 - B_5':    70, 
    '71 - Bb_5':   71,
    '72 - C_6':    72, 
    '73 - Db_6':   73, 
    '74 - D_6':    74, 
    '75 - Eb_6':   75,
    '76 - E_6':    76,
    '77 - F_6':    77, 
    '78 - Gb_6':   78, 
    '79 - G_6':    79, 
    '80 - Ab_6':   80, 
    '81 - A_6':    81,
    '82 - B_6':    82, 
    '83 - Bb_6':   83, 
    '84 - C_7':    84, 
    '85 - Db_7':   85, 
    '86 - D_7':    86,
    '87 - Eb_7':   87, 
    '88 - E_7':    88, 
    '89 - F_7':    89, 
    '90 - Gb_7':   90, 
    '91 - G_7':    91,
    '92 - Ab_7':   92, 
    '93 - A_7':    93, 
    '94 - B_7':    94, 
    '95 - Bb_7':   95, 
    '96 - C_8':    96,
    '97 - Db_8':   97, 
    '98 - D_8':    98, 
    '99 - Eb_8':   99, 
    '100 - E_8':   100, 
    '101 - F_8':   101,
    '102 - Gb_8':  102, 
    '103 - G_8':   103, 
    '104 - Ab_8':  104, 
    '105 - A_8':   105, 
    '106 - B_8':   106, 
    '107 - Bb_8':  107, 
    '108 - C_9':   108, 
    '109 - Db_9':  109,
    '110 - D_9':   110, 
    '111 - Eb_9':  111, 
    '112 - E_9':   112, 
    '113 - F_9':   113,
    '114 - Gb_9':  114, 
    '115 - G_9':   115, 
    '116 - Ab_9':  116, 
    '117 - A_9':   117,
    '118 - B_9':   118, 
    '119 - Bb_9':  119, 
    '120 - C_10':  120, 
    '121 - Db_10': 121,
    '122 - D_10':  122, 
    '123 - Eb_10': 123, 
    '124 - E_10':  124,
    '125 - F_10':  125,
    '126 - Gb_10': 126, 
    '127 - G_10':  127}

# tuning root values
tuning_root = {
    'C':  0,
    'Db': 11,
    'D':  22,
    'Eb': 32,
    'E':  43,
    'F':  54,
    'Gb': 64,
    'G':  75,
    'Ab': 86,
    'A':  96,
    'Bb': 107,
    'B':  118}

# boolean/cc value map
boolean = {
    'Off': 0, 
    'On':  127}

# vibrato speed values
vibrato_speed = {
    '0': 0, 
    '1': 2, 
    '2': 3, 
    '3': 4, 
    '4': 5, 
    '5': 6, 
    '6': 7, 
    '7': 9, 
    '8': 10, 
    '9': 11, 
    '10': 12, 
    '11': 13, 
    '12': 14, 
    '13': 16, 
    '14': 17, 
    '15': 18, 
    '16': 19, 
    '17': 20, 
    '18': 21, 
    '19': 23, 
    '20': 24, 
    '21': 25, 
    '22': 26, 
    '23': 27, 
    '24': 28, 
    '25': 30, 
    '26': 31, 
    '27': 32, 
    '28': 33, 
    '29': 34,
    '30': 35, 
    '31': 37, 
    '32': 38, 
    '33': 39, 
    '34': 40, 
    '35': 41, 
    '36': 42, 
    '37': 44, 
    '38': 45, 
    '39': 46,
    '40': 47, 
    '41': 48, 
    '42': 49, 
    '43': 51, 
    '44': 52, 
    '45': 53, 
    '46': 54, 
    '47': 55, 
    '48': 56, 
    '49': 58,
    '50': 59, 
    '51': 60, 
    '52': 61, 
    '53': 62, 
    '54': 63, 
    '55': 64, 
    '56': 66, 
    '57': 67, 
    '58': 68, 
    '59': 69,
    '60': 70, 
    '61': 71, 
    '62': 73, 
    '63': 74, 
    '64': 75, 
    '65': 76, 
    '66': 77, 
    '67': 78, 
    '68': 80, 
    '69': 81,
    '70': 70, 
    '71': 83, 
    '72': 84, 
    '73': 85, 
    '74': 87, 
    '75': 88, 
    '76': 89, 
    '77': 90, 
    '78': 91, 
    '79': 92,
    '80': 94, 
    '81': 95, 
    '82': 96, 
    '83': 97, 
    '84': 98, 
    '85': 99, 
    '86': 101, 
    '87': 102, 
    '88': 103, 
    '89': 104,
    '90': 105, 
    '91': 106, 
    '92': 108, 
    '93': 109, 
    '94': 110, 
    '95': 111, 
    '96': 112, 
    '97': 113, 
    '98': 115, 
    '99': 116,
    '/1': 117, 
    '/2': 118, 
    '/3': 119, 
    '/4': 120, 
    '/6': 122, 
    '/8': 123, 
    '/12': 124, 
    '/16': 125, 
    '/24': 126, 
    '/32': 127}

# oscillator/cc value map
oscillator = {
    'Off':      0, 
    'Sawtooth': 19, 
    'Pulse':    37, 
    'Square':   55, 
    'Triangle': 74, 
    'Sine':     92,
    'Noise':    110}

# midi out modes/cc value map
midi_output = {
    'Off':     0, 
    'Thru':    43, 
    'Arp/Seq': 86}

# note priority/cc value map
note_priority = {
    'Last': 0,
    'Low':  43, 
    'High': 86}

# voicing values. these only effect polyphonic layouts
voicing = {
    'Poly':     0, 
    'Cyclic':   32, 
    'Random':   64, 
    'Velocity': 96}

# arpeggiator direction values
arp_direction = {
    'Up':      0, 
    'Down':    26, 
    'Up/Down': 52, 
    'Random':  77, 
    'Played':  103}

# arpeggiator clock divider/cc value map
arp_clock_division = {
    '/1':  0, 
    '/2':  11, 
    '/3':  22, 
    '/4':  32, 
    '/6':  43, 
    '/8':  54, 
    '/12': 64, 
    '/16': 75, 
    '/24': 86, 
    '/32': 96, 
    '/48': 107, 
    '/96': 118}

# tuning system values. the ragas are prefixed with numbers as they are on the module
tuning_system = {
    'Equal temperament': 0,
    'Just intonation':   4,
    'Pythagorean':       8,
    'EB 1/4':            12,
    'E 1/4':             16,
    'EA 1/4':            19,
    '01 Bhairav':        23,
    '02 Gunakri':        27,
    '03 Marwa':          31,
    '04 Shree':          34,
    '05 Purvi':          38,
    '06 Bilawal':        42,
    '07 Yaman':          46,
    '08 Kafi':           49,
    '09 Bhimpalasree':   53,
    '10 Darbari':        57,
    '11 Bageshree':      61,
    '12 Rageshree':      64,
    '13 Khamaj':         68,
    '14 Mi Mal':         72,
    '15 Parameshwari':   76,
    '16 Rangeshwari':    80,
    '17 Gangeshwari':    83,
    '18 Kameshwari':     87,
    '19 Pa Kafi':        91,
    '20 Natbhairav':     95,
    '21 M.Kauns':        98,
    '22 Bairagi':        102,
    '23 B.Todi':         106,
    '24 Chandradeep':    110,
    '25 Kaushik Todi':   113,
    '26 Jogeshwari':     117,
    '27 Rasia':          121,
    'Custom':            125}

# trigger shape/cc value map
trigger_shape = {
    'Square':      0, 
    'Linear':      22, 
    'Exponential': 43, 
    'Ring':        64, 
    'Step':        86, 
    'Burst':       107}

# aux cv output/cc value map
aux_cv = {
    'Aftertouch CC#2': 26, 
    'Pedal CC#4':      52, 
    'Vibrato LFO':     77, 
    'LFO':             103}

# pitch bend range/cc value map
pitch_bend = {
    '0': 0, 
    '1': 6, 
    '2': 11, 
    '3': 16,
    '4': 21, 
    '5': 26, 
    '6': 31, 
    '7': 36, 
    '8': 41,
    '9': 47, 
    '10': 52, 
    '11': 57, 
    '12': 62, 
    '13': 67, 
    '14': 72, 
    '15': 77, 
    '16': 82,
    '17': 88, 
    '18': 93, 
    '19': 98, 
    '20': 103, 
    '21': 108, 
    '22': 113, 
    '23': 118,
    '24': 123}

# vibrato range/cc value map
vibrato_range = {
    '0': 0, 
    '1': 10, 
    '2': 20, 
    '3': 30, 
    '4': 40, 
    '5': 50, 
    '6': 60,
    '7': 69, 
    '8': 79, 
    '9': 89, 
    '10': 99, 
    '11': 109, 
    '12': 119}

# transpose/cc value map
transpose = {
    '-36': 0, 
    '-35': 2, 
    '-34': 4, 
    '-33': 6, 
    '-32': 8, 
    '-31': 9, 
    '-30': 11,
    '-29': 13, 
    '-28': 15, 
    '-27': 16, 
    '-26': 18, 
    '-25': 20, 
    '-24': 22,
    '-23': 23, 
    '-22': 25, 
    '-21': 27, 
    '-20': 29, 
    '-19': 30, 
    '-18': 32,
    '-17': 34, 
    '-16': 36, 
    '-15': 37, 
    '-14': 39, 
    '-13': 41, 
    '-12': 43,
    '-11': 44, 
    '-10': 46, 
    '-9': 48, 
    '-8': 50, 
    '-7': 51, 
    '-6': 53,
    '-5': 55, 
    '-4': 57, 
    '-3': 58, 
    '-2': 60, 
    '-1': 62, 
    '0': 64, 
    '1': 65, 
    '2': 67, 
    '3': 69, 
    '4': 71,
    '5': 72, 
    '6': 74, 
    '7': 76, 
    '8': 78,
    '9': 79, 
    '10': 81, 
    '11': 83, 
    '12': 85, 
    '13': 86, 
    '14': 88, 
    '15': 90, 
    '16': 92, 
    '17': 93, 
    '18': 95, 
    '19': 97, 
    '20': 99, 
    '21': 100, 
    '22': 102,
    '23': 104, 
    '24': 106, 
    '25': 107, 
    '26': 109, 
    '27': 111, 
    '28': 113,
    '29': 114, 
    '30': 116, 
    '31': 118, 
    '32': 120, 
    '33': 121, 
    '34': 123,
    '35': 125, 
    '36': 127}

# fine tuning/cc value map
fine_tuning = {
    '-64': 0, 
    '-63': 1, 
    '-62': 2, 
    '-61': 3, 
    '-60': 4, 
    '-59': 5, 
    '-58': 6,
    '-57': 7, 
    '-56': 8, 
    '-55': 9, 
    '-54': 10, 
    '-53': 11, 
    '-52': 12, 
    '-51': 13,
    '-50': 14,
    '-49': 15, 
    '-48': 16, 
    '-47': 17, 
    '-46': 18, 
    '-45': 19, 
    '-44': 20, 
    '-43': 21, 
    '-42': 22, 
    '-41': 23, 
    '-40': 24, 
    '-39': 25, 
    '-38': 26, 
    '-37': 27,
    '-36': 28, 
    '-35': 29, 
    '-34': 30, 
    '-33': 31, 
    '-32': 32, 
    '-31': 33, 
    '-30': 34,
    '-29': 35, 
    '-28': 36, 
    '-27': 37, 
    '-26': 38, 
    '-25': 39, 
    '-24': 40, 
    '-23': 41,
    '-22': 42, 
    '-21': 43, 
    '-20': 44, 
    '-19': 45, 
    '-18': 46, 
    '-17': 47, 
    '-16': 48,
    '-15': 49, 
    '-14': 50, 
    '-13': 51, 
    '-12': 52, 
    '-11': 53, 
    '-10': 54, 
    '-9': 55,
    '-8': 56, 
    '-7': 57, 
    '-6': 58, 
    '-5': 59, 
    '-4': 60, 
    '-3': 61,
    '-2': 62, 
    '-1': 63,
    '0': 64, 
    '1': 65, 
    '2': 66, 
    '3': 67, 
    '4': 68, 
    '5': 69, 
    '6': 70, 
    '7': 71,
    '8': 72, 
    '9': 73, 
    '10': 74, 
    '11': 75, 
    '12': 76, 
    '13': 77, 
    '14': 78, 
    '15': 79,
    '16': 80, 
    '17': 81, 
    '18': 82, 
    '19': 83, 
    '20': 84, 
    '21': 85, 
    '22': 86, 
    '23': 87,
    '24': 88, 
    '25': 89, 
    '26': 90, 
    '27': 91, 
    '28': 92, 
    '29': 93, 
    '30': 94, 
    '31': 95,
    '32': 96, 
    '33': 97, 
    '34': 98, 
    '35': 99, 
    '36': 100, 
    '37': 101, 
    '38': 102,
    '39': 103, 
    '40': 104, 
    '41': 105, 
    '42': 106, 
    '43': 107, 
    '44': 108, 
    '45': 109,
    '46': 110, 
    '47': 111, 
    '48': 112, 
    '49': 113, 
    '50': 114, 
    '51': 115, 
    '52': 116,
    '53': 117, 
    '54': 118, 
    '55': 119, 
    '56': 120, 
    '57': 121, 
    '58': 122, 
    '59': 123,
    '60': 124, 
    '61': 125, 
    '62': 126, 
    '63': 127}

# euclidean/cc value map
euclidean = {
    '0': 0, 
    '1': 4, 
    '2': 8, 
    '3': 12, 
    '4': 16, 
    '5': 20, 
    '6': 24, 
    '7': 28, 
    '8': 32, 
    '9': 35, 
    '10': 39, 
    '11': 43, 
    '12': 47, 
    '13': 51, 
    '14': 55, 
    '15': 59, 
    '16': 63, 
    '17': 66, 
    '18': 70, 
    '19': 74, 
    '20': 78, 
    '21': 82, 
    '22': 86, 
    '23': 90, 
    '24': 94, 
    '25': 97, 
    '26': 101, 
    '27': 105, 
    '28': 109, 
    '29': 113, 
    '30': 117, 
    '31': 121, 
    '32': 125}

# trigger duration/cc value map
trigger_duration = {
    '1': 0, 
    '2': 2, 
    '3': 3, 
    '4': 4, 
    '5': 6, 
    '6': 7, 
    '7': 8, 
    '8': 10,
    '9': 11, 
    '10': 12, 
    '11': 13, 
    '12': 15, 
    '13': 16, 
    '14': 17, 
    '15': 19,
    '16': 20, 
    '17': 21, 
    '18': 22, 
    '19': 24, 
    '20': 25, 
    '21': 26, 
    '22': 28,
    '23': 29, 
    '24': 30, 
    '25': 32, 
    '26': 33, 
    '27': 34, 
    '28': 35, 
    '29': 37,
    '30': 38, 
    '31': 39, 
    '32': 41, 
    '33': 42, 
    '34': 43, 
    '35': 44, 
    '36': 46,
    '37': 47, 
    '38': 48, 
    '39': 50, 
    '40': 51, 
    '41': 52, 
    '42': 54, 
    '43': 55,
    '44': 56, 
    '45': 57, 
    '46': 59, 
    '47': 60, 
    '48': 61, 
    '49': 63, 
    '50': 64,
    '51': 65, 
    '52': 66, 
    '53': 68, 
    '54': 69, 
    '55': 70, 
    '56': 72, 
    '57': 73,
    '58': 74, 
    '59': 75, 
    '60': 77, 
    '61': 78, 
    '62': 79, 
    '63': 81, 
    '64': 82,
    '65': 83, 
    '66': 85, 
    '67': 86, 
    '68': 87, 
    '69': 88, 
    '70': 90, 
    '71': 91,
    '72': 92, 
    '73': 94, 
    '74': 95, 
    '75': 96, 
    '76': 97, 
    '77': 99, 
    '78': 100,
    '79': 101, 
    '80': 103, 
    '81': 104, 
    '82': 105, 
    '83': 107, 
    '84': 108,
    '85': 109, 
    '86': 110, 
    '87': 112, 
    '88': 113, 
    '89': 114, 
    '90': 116,
    '91': 117, 
    '92': 118, 
    '93': 119, 
    '94': 121, 
    '95': 122, 
    '96': 123,
    '97': 125, 
    '98': 126, 
    '99': 127}

# arpeggiator range/cc value map
arp_range = {
    '0': 0, 
    '1': 26, 
    '2': 52, 
    '3': 77, 
    '4': 103}

# arpeggiator pattern/cc value map
arp_pattern = {
    '1': 0, 
    '2': 6, 
    '3': 12, 
    '4': 18, 
    '5': 24, 
    '6': 30, 
    '7': 35, 
    '8': 41,
    '9': 47, 
    '10': 53, 
    '11': 59, 
    '12': 64, 
    '13': 70, 
    '14': 76, 
    '15': 82,
    '16': 88, 
    '17': 94, 
    '18': 99, 
    '19': 105, 
    '20': 111, 
    '21': 117, 
    '22': 123}

# arpeggiator gate length/cc value map
arp_gate_length = {
    '1': 0, 
    '2': 3, 
    '3': 6, 
    '4': 8, 
    '5': 11, 
    '6': 14, 
    '7': 16, 
    '8': 19,
    '9': 22, 
    '10': 24, 
    '11': 27, 
    '12': 30, 
    '13': 32,
    '14': 35, 
    '15': 38,
    '16': 40, 
    '17': 43, 
    '18': 46, 
    '19': 48, 
    '20': 51, 
    '21': 54, 
    '22': 56,
    '23': 59, 
    '24': 62, 
    '25': 64, 
    '26': 67, 
    '27': 70, 
    '28': 72, 
    '29': 75,
    '30': 78, 
    '31': 80, 
    '32': 83, 
    '33': 86, 
    '34': 88, 
    '35': 91, 
    '36': 94,
    '37': 96, 
    '38': 99, 
    '39': 102, 
    '40': 104, 
    '41': 107, 
    '42': 110, 
    '43': 112,
    '44': 115, 
    '45': 118, 
    '46': 120, 
    '47': 123, 
    '48': 126}
