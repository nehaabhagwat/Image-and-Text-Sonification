# csv_climate_data.py
# Author: Neha Bhagwat
# Purpose: To sonify monthly average temperature data

from music import *
import collections

# Enter the path to the file that contains temperature data to be sonified
filename = ""

dataset = open(filename, "r")

header_line = dataset.readline()
print(header_line)

data = dataset.readlines()
monthly_temp = {}
temperatures = []
for record in data:
    record = record.replace(",,,",",noise,noise,")
    record = record.replace(",,",",noise,")
    record = record.split(',')
    # print(record[11][1:len(record[11])-1])
    if record[6].find("noise") == -1 and record[11].find("noise") == -1:
        monthly_temp.update({record[6][1:len(record[6])-1]:float(record[11][1:len(record[11])-1])})
        temperatures.append(record[11][1:len(record[11])-1])
minTemperature = min(temperatures)
maxTemperature = max(temperatures)
print minTemperature
print maxTemperature

print monthly_temp

for key in sorted(monthly_temp.iterkeys()):
   print key + ": " + str(monthly_temp[key])

tempPitches = []
tempDurations = []
od = collections.OrderedDict(sorted(monthly_temp.items()))
print(od)
keyList = od.keys()
for key in keyList:
    pitch = mapScale(int(od[key]), 41, 71, C1, C6, CHROMATIC_SCALE)
    tempPitches.append( pitch )
    tempDurations.append( EN )

melody1 = Phrase(0.0)
melody1.addNoteList(tempPitches, tempDurations)

piano = Part("Eighth Notes", PIANO, 0)
piano.addPhrase(melody1)
score = Score("Temperatures")
score.addPart(piano)
View.sketch(score)
Play.midi(score)
print(monthly_temp)
