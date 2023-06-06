# MIDI to Frequency Converter
A tool to convert MIDI files to a list of frequencies and durations.
Useful for converting sound from your MIDI instruments to a format that can be used in your microcontroller projects.
Uses the Mido library to parse MIDI files.

Current only supports unix-like systems.

# Usage
midi2dat.py *input_file.midi* -o *output_file.dat* 
## Flags
-v --verbose: Print out the notes as they are being processed.  
-p --play: Play the notes after finishing.