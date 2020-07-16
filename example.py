#!/usr/bin/python
import argparse
from binascii import a2b_qp
from wave import Waveform

def bytestring(n):
    return bin(n).lstrip('0b').zfill(8)


def getByteTuples(p1, p2):
    ba1 = bytearray(p1)
    ba2 = bytearray(p2)
    if len(p1) > len(p2):
        tupList = [
            (c1, b1, c2, b2, b1 ^ b2)
            for c1, b1, c2, b2 in zip(p1, ba1, cycle(p2), cycle(ba2))
        ]
    else:
        tupList = [
            (c1, b1, c2, b2, b1 ^ b2)
            for c1, b1, c2, b2 in zip(cycle(p1), cycle(ba1), p2, ba2)
        ]
    return tupList


parser = argparse.ArgumentParser()
parser.add_argument('phrases', nargs='+')
parser.add_argument('-t', '--table', action='store_true', help='Table output of XOR')
parser.add_argument('-w', '--wave', action='store_true', help='Show waveform of result')
parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
args = parser.parse_args()

# If only one word/phrase was entered...
if len(args.phrases) == 1:
    ba = bytearray(args.phrases[0])
    binstring = ''.join([bytestring(b) for b in ba])
    if args.table:
        # Print each byte on its own line if table arg is set
        for b in ba:
            if args.verbose:
                output = '{}  {}'.format(chr(b), bytestring(b))
            else:
                output = bytestring(b)
            print(output)
    else:
        # If not table, print out all bytes  in long string
        print(binstring)
    if args.wave:
        # If wave arg is set, print out waveform under the bytes
        wf = Waveform(binstring, use_terms=True, width=0, length=80)
        wf.printWave()
else:
    from itertools import cycle
    p1 = args.phrases[0]
    p2 = args.phrases[1]
    # Build list of tuples (char, byte, char, byte, xor'ed bytes)
    tupList = getByteTuples(p1, p2)
    binstring = ''.join([bytestring(t[-1]) for t in tupList])
    if args.table:
        for t in tupList:
            if args.verbose:
                output = '{}  {}  {}  {}  x  {}'.format(
                    t[0], bytestring(t[1]), t[2], bytestring(t[3]), bytestring(t[4]))
            else:
                output = bytestring(t[-1])
            print(output)
    else:
        print(binstring)
    if args.wave:
        wf = Waveform(binstring, use_terms=True, width=0, length=80)
        wf.printWave()
