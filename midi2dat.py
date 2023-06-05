# Convert MIDI files to frequency and duration data for a PWM library.
# Uses the mido library: https://mido.readthedocs.io/en/latest/

from mido import MidiFile
import mido
import argparse
from pathlib import Path
import time
import math
import subprocess


tempo = 500000  # microseconds per beat

# MIDI note 69 is A4, which is 440 Hz.



def midiNoteToFreq(midiNote):
    return round(440 * 2 ** ((midiNote - 69) / 12))

def midiTimeToMillis(midiFile, midiTime):
    return round(mido.tick2second(midiTime, tempo=tempo, ticks_per_beat=midiFile.ticks_per_beat) * 1000)

def main():
    parser = argparse.ArgumentParser(description='Convert MIDI files to frequency and duration data for a PWM library.')
    parser.add_argument('midi_file', type=str, help='MIDI file to convert')
    parser.add_argument('-o', '--output', type=str, help='Output file name')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-p', '--play', action='store_true', help='Play output using the PC speaker')
    args = parser.parse_args()
    
    if args.output is None:
        args.output = Path(args.midi_file).stem + '.dat'
    
    outFile = open(args.output, 'w')
    
    if not Path(args.midi_file).is_file():
        print(f'Error: {args.midi_file} does not exist.')
        return
    
    if args.verbose:
        print('Converting {} to {}'.format(args.midi_file, args.output))
        
    mid = MidiFile(args.midi_file)
                                
    output = []
    currentTime = 0
    for tnum, track in enumerate(mid.tracks):
        if args.verbose:
            print('Track {}: {}'.format(tnum, track.name))
        trackStart = True
        currentFreq = 0
        for msg in track:
            if args.verbose:
                print(msg)
            
            # Process all note_on and note_off messages in the track.
            # Record the equivalent frequency and duration for each note.
            # A note_on message with a velocity of 0 is equivalent to a note_off message.
            if msg.type == 'note_on' and msg.velocity > 0:
                noteTime = msg.time
                if trackStart:
                    trackStart = False
                    if noteTime > 0:
                        output.append([0,  noteTime - currentTime])
                if currentFreq != 0:
                    output.append([0, midiTimeToMillis(mid, noteTime)])
                currentFreq = midiNoteToFreq(msg.note)
                currentTime += noteTime

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                noteTime = msg.time
                output.append([currentFreq, midiTimeToMillis(mid, noteTime)])
                currentTime += noteTime
    outFile.write(',\n'.join(map(str, output)))
    if args.play:
        for note in output:
            if note[0] == 0:
                time.sleep(note[1] / 1000)
            else:
                subprocess.run(['beep', '-f', str(note[0]), '-l', str(note[1])])
     
if __name__ == '__main__':
    main()