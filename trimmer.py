from pydub import AudioSegment
import re
import os
lines=[]
InputDir= []
for path in os.listdir():
    if ".mp3"in path or '.wav'in path: 
        InputDir= path
fileName = InputDir.split('.')[0]
fileName = " ".join((re.sub(r'[^A-Za-z0-9 ]+',' ',fileName)).split())
fileName= str(len(os.listdir("Ambience Playlists"))+1)+') '+fileName
if "ezmp3" in fileName: 
    fileName.replace('ezmp3','')
newpath = os.getcwd()+"\\Ambience Playlists\\"+  fileName
if not os.path.exists(newpath):
    os.makedirs(newpath)





def trim_audio(intervals, names):
    # load the audio file
    

    # iterate over the list of time intervals
    for i, (start_time, end_time) in enumerate(intervals):
        # extract the segment of the audio
        segment = audio[start_time*1000:end_time*1000]

        # construct the output file path
        output_file_path = newpath + "\\"+ names[i]

        # export the segment to a file
        segment.export(output_file_path, format='wav')

file= open('intervals.txt')
IntervalLines= [re.sub(r'[^A-Za-z0-9,:-]'," ",str(line.rstrip()))for line in file]
print(IntervalLines)
Intervals = [line.split(" ")[0] for line in IntervalLines]
names= [(line.split(' ',1))[1]for line in IntervalLines]

for i in range (len(names)): 
    SpacedName=re.sub(r'[^A-Za-z0-9 ]+',' ',names[i])
    names[i]= " ".join(SpacedName.split())+'.wav'
    print(names[i])

for n in names: 
     print(n)

milliIntervals=[]
for line in Intervals: 
    vals = line.split(":")
    vals.reverse()
    #print(vals)
    milliStamp=0
    for i in range(len(vals)):
        if i ==0: 
            milliStamp+=int(vals[i])
        if i==1: 
           milliStamp+= int(vals[i])*60
        if i ==2: 
            milliStamp+= int(vals[i])*60*60
    milliIntervals.append(milliStamp)
SongStamps= []
audio = AudioSegment.from_file(InputDir)
milliIntervals.append(audio.duration_seconds)
for i in range(len(milliIntervals)-1): 
     SongStamps.append([milliIntervals[i],milliIntervals[i+1]])
for n in SongStamps: 
        print(n)
# test it out
print("Trimming audio...")
trim_audio(SongStamps, names)
print("...done! <3")