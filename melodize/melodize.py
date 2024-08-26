

from midiutil import MIDIFile
import argparse

BITS_PER_BYTE = 8

def bit_mask(bits):
    if bits > BITS_PER_BYTE:
        bits = BITS_PER_BYTE
    return (0xFF >> (BITS_PER_BYTE) - bits)


class ShortTokenReader:
    """
    Read groups of bits.
    It strictly requires that the group size (stepBits) is smaller than a byte.
    """



    def __init__(self,filename,stepBits=3):
        self.stepBits = stepBits

        self.currentByte = 0
        self.currentBit = 0
        self.chunk = None
        self.CHUNK_SIZE = 1024

        
        self.f_in = open(filename, "rb")
        #self.moreBytes = True
        self.chunk = self.f_in.read(self.CHUNK_SIZE)
        print("TR: ",len(self.chunk), " bytes")




    def remainingBits(self):
        return (len(self.chunk) - self.currentByte) * BITS_PER_BYTE - self.currentBit
    

    def getByteValue(self):
        if self.currentByte == len(self.chunk):
            self.readChunk()
        value = self.chunk[self.currentByte]
        self.currentByte+=1
        return value

    def readStepBitsLSBfirst(self):
        """
        Read bits, least significant bit first.
        """
        #bitIndex = self.currentBit

        bitShift = self.currentBit
        bitsToRead = self.stepBits + self.currentBit
        #print("  bitsToRead: ", bitsToRead)

        value = self.chunk[self.currentByte]
        #print("  value: ", value)

        if bitsToRead >= BITS_PER_BYTE:
            self.currentByte += 1
            self.currentBit -= BITS_PER_BYTE

            if bitsToRead > BITS_PER_BYTE:
            
                if self.currentByte == len(self.chunk):
                    #print("current byte:", self.currentByte)
                    self.readChunk()
                if len(self.chunk) > 0:
                    value += (self.chunk[self.currentByte] & bit_mask(bitsToRead - BITS_PER_BYTE)) << BITS_PER_BYTE
                

        value >>= bitShift
        self.currentBit += self.stepBits
        if self.currentBit > BITS_PER_BYTE:
            self.currentBit -= BITS_PER_BYTE
            self.currentByte += 1
        mask = bit_mask(self.stepBits)
        #print("  mask: %x" % mask)
        return value & mask


    def readChunk(self):
        data = self.f_in.read(self.CHUNK_SIZE)
        if self.currentByte == len(self.chunk):
            self.chunk = data
        else:
            self.chunk = self.chunk[self.currentByte:]+ data
        self.currentByte = 0


    def moreTokens(self):
        #print("moreTokens?")
        rb = self.remainingBits()
        #print("remaining bits:",rb)
        if rb > self.stepBits:
            return True
        else:
            self.readChunk()
            if self.remainingBits() > 0:
                return True
            return False
            

    def getNextToken(self):
        if self.moreTokens():
            return self.readStepBitsLSBfirst()
        #TODO: exception?
        return None



def test():
    tr = ShortTokenReader("test4.txt")
    tokens = []
    while tr.moreTokens():
        value = tr.getNextToken()
        tokens.append(value)
        print(value)
    print("Sequence:")
    print(tokens)
    print("num tokens:", len(tokens))


MIDI_C_SCALE = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI values

class Melodizer:

    def __init__(self):
        self.track = 0
        self.tempo = 60 # BPM
        self.melody_length = 8

        self.channel  = 0
        self.duration = 1   # In beats
        self.volume   = 100 # 0-127, as per the MIDI standard

    def convert(self, input_filename, output_prefix):

        melody_counter = 1

        tr = ShortTokenReader(input_filename)

        melody = []
        while tr.moreTokens():
            value = tr.getNextToken()
            melody.append(value)
            if len(melody) == self.melody_length:
                output_filename = f"{output_prefix}-{melody_counter}.mid"
                self.writeMelody(output_filename,melody)
                melody = []
                melody_counter += 1

        
        if len(melody) > 0:
            output_filename = f"{output_prefix}-{melody_counter}.mid"
            self.writeMelody(output_filename, melody)

            

    def writeMelody(self, filename, notes):
        output_file = open(filename, "wb")
        MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
        self.time = 0
        MyMIDI.addTempo(self.track,self.time, self.tempo)

        for value in notes:
            pitch = MIDI_C_SCALE[value]
            MyMIDI.addNote(self.track, self.channel, pitch, self.time, self.duration, self.volume)
            self.time = self.time + 1


        with open(filename, "wb") as output_file:
            MyMIDI.writeFile(output_file)




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', 
                        help='input file')
    parser.add_argument('-p', '--prefix', default="melody",
                        help='prefix for output files')

    args = parser.parse_args()


    #filename = args.filename



    mz = Melodizer()
    mz.convert(args.filename,args.prefix)
