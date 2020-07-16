#!/usr/bin/python


hoz = u'\u2500'  # horizontal line
vrt = u'\u2502'  # vertical line
h2d = u'\u2510'  # horizontal to down corner
d2h = u'\u2514'  # down to horizontal corner
h2u = u'\u2518'  # horizontal to up corner
u2h = u'\u250c'  # up to horizontal corner

def waveExtend(func):
    def inner():
        pass


class Waveform(object):
    """Build a wave that looks like this:
    [[  , /, -, \,  ,  ,  , /, -, -, -, -, -, \,  , /, -, \,  ]
     [ -, |,  , |,  ,  ,  , |,  ,  ,  ,  ,  , |,  , |,  , |, -]
     [  ,  ,  , \, _, _, _, /,  ,  ,  ,  ,  , \, _, /,  ,  ,  ]]
        s  1     0     0     1     1     1     0     1     e
    """

    def __init__(self, bytestring, use_terms=True, width=0, length=80):
        self.bytestring = bytestring
        self.width = width
        self.length = length
        self.use_terms = use_terms
        self.waveArray = [[], [], []]
        self.buildWaveArray(bytestring)

    def buildWaveArray(self, bytestring):
        """Encoding High == 1, Low == 0
        Transition when needed"""
        lastByte = len(bytestring) - 1
        if self.use_terms:
            self.term(self.waveArray)
        # Walk through the bytestring, tracking index
        for i, b in enumerate(bytestring):
            # If first bit, use proper 'start' function
            if i == 0:
                if b == '0':
                    self.ts_0(self.waveArray)
                else:
                    self.ts_1(self.waveArray)
            # Check previous and current bit to determine next function
            else:
                if bytestring[i-1] == '0':
                    if b == '0':
                        self.t0_0(self.waveArray)
                    else:
                        self.t0_1(self.waveArray)
                else:
                    if b == '0':
                        self.t1_0(self.waveArray)
                    else:
                        self.t1_1(self.waveArray)
        if bytestring[-1] == '0':
            self.t0_e(self.waveArray)
        else:
            self.t1_e(self.waveArray)
        if self.use_terms:
            self.term(self.waveArray)

    def printWave(self, waveArray=None):
        """print waveform to stdout"""
        if waveArray is None:
            waveArray = self.waveArray
        for i in xrange(0, len(waveArray[0]), self.length):
            print(''.join(waveArray[0][i:i+self.length]))
            print(''.join(waveArray[1][i:i+self.length]))
            print(''.join(waveArray[2][i:i+self.length]))

    def appendWaveArray(self, valTuple):
        """append values to all arrays in WaveArray"""
        for i, v in enumerate(valTuple):
            self.waveArray[i].append(v)

    def ts_1(self, arr):
        """transition from start to 1"""
        self.appendWaveArray([d2h, h2u, ' '])
        # return arr

    def ts_0(self, arr):
        """transition from start to 0"""
        self.appendWaveArray([' ', h2d, d2h])
        # return arr

    def t0_1(self, arr):
        """transition from 0 to 1"""
        for i in xrange(self.width):
            self.appendWaveArray([' ', ' ', hoz])
        self.appendWaveArray([u2h, vrt, h2u])
        # return arr
        
    def t0_0(self, arr):
        """transition from 0 to 0"""
        for i in xrange(self.width):
            self.appendWaveArray([' ', ' ', hoz])
        self.appendWaveArray([' ', ' ', hoz])
        # return arr

    def t1_0(self, arr):
        """transition from 1 to 0"""
        for i in xrange(self.width):
            self.appendWaveArray([hoz, ' ', ' '])
        self.appendWaveArray([h2d, vrt, d2h])
        # return arr

    def t1_1(self, arr):
        """transition from 1 to 1"""
        for i in xrange(self.width):
            self.appendWaveArray([hoz, ' ', ' '])
        self.appendWaveArray([hoz, ' ', ' '])
        # return arr

    def t0_e(self, arr):
        """transition from 0 to end"""
        for i in xrange(self.width):
            self.appendWaveArray([' ', ' ', hoz])
        self.appendWaveArray([' ', u2h, h2u])
        # return arr

    def t1_e(self, arr):
        """transition from 1 to end"""
        for i in xrange(self.width):
            self.appendWaveArray([hoz, ' ', ' '])
        self.appendWaveArray([h2d, d2h, ' '])
        # return arr

    def term(self, arr):
        """terminus of wave"""
        for i in xrange(self.width):
            self.appendWaveArray([' ', hoz, ' '])
        self.appendWaveArray([' ', hoz, ' '])
        # return arr


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('phrase')
    parser.add_argument('-t', '--terms', action='store_false', default=True)
    parser.add_argument('-w', '--width', type=int, default=0, help='Width of each bit')
    parser.add_argument('-l', '--length', type=int, default=80, help='Length of line before wrap')
    args = parser.parse_args()

    bytelist = [bin(ord(n)).lstrip('0b').zfill(8) for n in args.phrase]
    bytestring = ''.join(bytelist)
    wf = Waveform(bytestring, use_terms=args.terms, width=args.width, length=args.length)
    wf.printWave()
