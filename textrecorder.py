import sounddevice as sd
import wavio as wv
import speech_recognition as sr
from os.path import exists

# To run this code for the first time, do the following:
# Open the terminal... 
# Install the above libraries by copy pasting into the terminal:
#
# pip install sounddevice
# pip install wavio
# pip install SpeechRecognition


# Intro Screen
print("\nWelcome to my lecture converter.\n")
print("When prompted, input how long you want to record for.")
print("To record in MINUTES, input 1. To record in SECONDS, input 0.")
print("Lecture is 50 minutes long.\n")

# Define duration for recording. Ask minutes or seconds and return seconds
ask = True
while ask == True:
    ms = int(input("Minutes (1) or Seconds (0)?: "))
    print()
    # Check for minutes / seconds output
    if ms == 0:
        mult = 1
        ask = False
    elif ms == 1:
        mult = 60
        ask = False
    else:
        print("Please input a valid input")
        continue

    # Input for the length of recording
    d = int(mult*int(input("Enter duration of recording length: ")))

print("\nRecording for " + str(d) + " seconds...\n")

def recordForDuration(duration = d):
    # Sampling frequency ... 44100 or 48000 fps
    freq = 44100

    # Start recording with duration and frequency defined
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

    # Record audio for given duration
    sd.wait()

    # Check for files to prevent overwriting
    name = "lecture0.wav"
    # Check current folder for existing files to prevent overwriting
    file_exists = exists(name)
    # If the file exists, find a file name that doesn't
    count = 0
    while file_exists:
        count += 1
        # Separate and parse name to replace the figure number
        dotindex = name.index(".")
        namesep = [ii for ii in name]
        namesep[dotindex - 1] = str(count)
        # Fill new string with corrected string
        name = "" 
        for items in namesep:
            name += items
        # Determine if loop continues
        file_exists = exists(name)

    # Convert NumPy array to audio file
    wv.write(name, recording, freq, sampwidth=2)
    # Return corrected filename to find and parse recording 
    return name

filename = recordForDuration(d)

print("Recording Completed!\n")
print("Parsing file for text...\n")

# initialize the recognizer
r = sr.Recognizer()

# open the file
file = sr.AudioFile(filename)
with file as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
try:
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    # print("Text: " + text)
except Exception as e:
    print("Error thrown!:")
    print("Exception: " + str(e))

# Write contents of WAV file parsed into text file
writefile = filename.replace("wav", "txt")
with open(writefile, 'w') as f:
    f.write(text)

print("Done!\n")