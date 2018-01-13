#sonifyGrayscaleImage.py
# Author: Neha Bhagwat

from music import *
from image import *
from random import *
# from PIL import Image

soundscapeScore = Score("Grayscale Score", 60)
soundscapePart  = Part(PIANO, 0) 

scale = MIXOLYDIAN_SCALE

minPitch = 0        # MIDI pitch (0-127)
maxPitch = 127
 
minDuration = 0.8   # duration (1.0 is QN)
maxDuration = 6.0
 
minVolume = 0       # MIDI velocity (0-127)
maxVolume = 127

setVolume = 90 # pre defined volume for all notes

##### read in image (origin (0, 0) is at top left)
image = Image("Enter path to input image.")


width = image.getWidth()
height = image.getHeight()
analysisWidth = width/6

#pixelRows is a list that contains a list of row numbers for which pixel sonification will be carried out
pixelRows = []
currentWidth = 0
# pixelRows.append(currentWidth)

while currentWidth < width:
   pixelRows.append(currentWidth)
   currentWidth += analysisWidth
   
   
# print(pixelRows)

##### define function to sonify one pixel
# Returns a note from sonifying the RGB values of 'pixel'.
def sonifyPixel(pixel):
 
   # print(pixel)
   r, g, b = pixel
   luminosity = 0.299*r + 0.587*g + 0.114*b
   #luminosity = pixel   # calculate brightness
      
   # map luminosity to pitch (the brighter the pixel, the higher
   # the pitch) using specified scale
   pitch = mapScale(luminosity, 0, 255, minPitch, maxPitch, scale)
 
   # map red value to duration (the redder the pixel, the longer 
   # the note)
   duration = mapValue(1, 0, 255, minDuration, maxDuration)
 
   # map blue value to dynamic (the bluer the pixel, the louder 
   # the note)      
   dynamic = mapValue(setVolume, 0, 255, minVolume, maxVolume)
   
   # create note and return it to caller
   note = Note(pitch, 10, dynamic)   
   
   # done sonifying this pixel, so return result
   return note
   

# sonify image pixels
for row in pixelRows:   # iterate through selected rows
 
   for col in range(width):  # iterate through all pixels on this row
   
      # get pixel at current coordinates (col and row)
      pixel = image.getPixel(col, row)
      r, g, b = pixel
      luminosity = int(0.299*r + 0.587*g + 0.114*b)
      # print(luminosity)
      # sonify this pixel (we get a note)
      note = sonifyPixel(pixel)
 
      # wrap note in a phrase to give it a start time
      # (Phrases have start time, Notes do not)
 
      # use column value as note start time (e.g., 0.0, 1.0, and so on)
      startTime = float(col)   # phrase start time is a float
      
      # add some random displacement for variety
      startTime = startTime# + choice( timeDisplacement )
       
      phrase = Phrase(startTime)   # create phrase with given start time
      phrase.addNote(note)         # and put the note in it 
                         
      # put result in part
      soundscapePart.addPhrase(phrase)
      
##### combine musical material
soundscapeScore.addPart(soundscapePart)
 
##### view score and write it to an audio and MIDI files
Play.midi(soundscapeScore)
