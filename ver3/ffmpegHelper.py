#!/usr/bin/env python3.7

import ffmpy 
import sys
import subprocess
from subprocess import PIPE, run
import re
import os
from random import *
import json

print ( "Numer arguments : ", len(sys.argv), " arguments.")

print ( "Argument List : " , str (sys.argv) )

video_file = ""
ffmpeg_command=""
crop_value=""
media_duration =""
out_file=""

def getMediaLengthFloatingNumber( the_file ):
	print ( "CALCULATING %s LENGTH" % ( the_file ) )

	getMediaLengthValue = run('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 %s' % ( the_file ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	return  getMediaLengthValue.stdout 


def getMediaInfo( the_file, main_json_node, sub_json_node, info ):
	print ( "Retreiving info for %s " % ( the_file ) )
	getMediaLengthValue = run('ffprobe -v quiet -print_format json -show_format -show_streams %s' % ( the_file ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	
	#print ( " XXXXX : getMediaLengthValue : %s" % ( getMediaLengthValue )  )
	#print ( "FORMAT TYPE : %s" % ( json.loads (  getMediaLengthValue.stdout )[ "format" ][ "format_name" ] ) ) 
	#print ( "FORMAT TYPE : %s" % ( json.loads (  getMediaLengthValue.stdout )[ "format" ][ "format_name" ].find ("matroska,webm")  ) ) 
	# Check if file is a .MKV ( Matroska Multimedia Container  )
	if json.loads (  getMediaLengthValue.stdout )[ "format" ][ "format_name" ] == "matroska,webm" :
		print ("%s is a Matroska Multimedia file." % ( the_file )  )
		return json.loads (  getMediaLengthValue.stdout )[ "format" ][ "duration" ] 
	else :
		return json.loads (  getMediaLengthValue.stdout )[ main_json_node ][ sub_json_node ][ info ]

# I need to use this for the 'format' node to check if file has an audio stream
# it also contain info on the play duration of the file.
def getMediaAudioInfo( the_file, main_json_node, sub_json_node ):
	print ( "Retreiving info for : %s " % ( the_file ) )
	getMediaLengthValue = run('ffprobe -v quiet -print_format json -show_format -show_streams %s' % ( the_file ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	#requestedInfo = json.loads (  getMediaLengthValue.stdout )['format']['nb_streams']
	
	returnMe = json.loads (  getMediaLengthValue.stdout )[ main_json_node ][ sub_json_node ]

	print ( "info : %s | returned : %s" % ( sub_json_node, returnMe ) )
	return returnMe

# If no help set values
#if ( not re.search('-(h|c1)', sys.argv[1] ) ):
if ( not re.search('-(h)', sys.argv[1] ) ):
	print ( "Setting values for video_file and out_file"  )
	video_file=sys.argv[2]
	out_file=sys.argv[ len(sys.argv) - 1 ] # The last value passed to the code
	#if ( not re.search('^-(c1$|c2$|c4$|c5$|c6$|c7$|e1$|lex1$)', sys.argv[1] ) ): 
	#if ( not re.search('^-(c1$|c2$|c4$|c5$|c6$|c7$|c8$|e1$|lex1$)', sys.argv[1] ) ): 
	if ( not re.search('^-(c1$|c2$|c4$|c5$|c6$|c7$|c8$|e1$|e22$|lex1$)', sys.argv[1] ) ): 
		# If the user specifies the length of zero aka 0 as the file length give them back the true length of the video
		media_duration = getMediaAudioInfo( video_file, 'format', 'duration' ) if sys.argv[4] == "0" else sys.argv[4]

def useFFmpegClass():
	ff = ffmpy.FFmpeg(
		inputs={ video_file : None},
		outputs={ out_file : ffmpeg_command }
	)
	print ( ff.cmd )
	ff.run()
	# Run a preview of the video
	subprocess.call( 'mplayer %s -loop 0'  % ( out_file ) , shell=True )

# Search for cx.x movies and place them in the file l.txt example : file 'c36'.mov

def searchForConcatFiles():
	print ("*** Searching For cx.x Videos To Concat ***")

	# Open or create the file l.txt for storing the files that need to be concated
	fo = open ( "l.txt", "w")
	print ( fo.name )

	listOfFilesToAlphabetize = []
	#for name in glob.glob('./c\d+.*'):
	for filename in os.listdir ("./"):
		if ( re.match (r"c\d+.*" , filename ) and  os.path.splitext(filename)[1] != ".ts"):
			# Display file name without extension
			#print ( os.path.splitext(filename)[1] )
			# Convert file to .ts
			run('ffmpeg -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts %s.ts' % ( filename, os.path.splitext(filename)[0] ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
			listOfFilesToAlphabetize.append( '%s.ts' % ( os.path.splitext(filename)[0] ) )
	for i in sorted ( listOfFilesToAlphabetize ) :
		fo.write ( "file " + "'" + i + "' \n")

	# Close the file
	fo.close ()
	
	
	
	
def searchForConcatFilesToTs():
	print ("*** Searching For cx.x Videos To Concat to cx.ts***")
	
	stringOfTsFiles="concat:"
	listOfFilesToAlphabetize = []
	#for name in glob.glob('./c\d+.*'):
	for filename in os.listdir ("./"):
		if ( re.match (r"c\d+.*" , filename ) and  os.path.splitext(filename)[1] != ".ts"):
			# Convert file to .ts
			print ("Converting %s to %s.ts" % (filename, os.path.splitext(filename)[0] ) )
			run('ffmpeg -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts -y %s.ts' % ( filename, os.path.splitext(filename)[0] ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
			listOfFilesToAlphabetize.append( '%s.ts' % ( os.path.splitext(filename)[0] ) )
	
	stringOfTsFiles += "|".join( sorted ( listOfFilesToAlphabetize ) )
	return stringOfTsFiles, listOfFilesToAlphabetize
	

def searchForConcatFilesAndRemove():
	#print ("*** Searching For cx.ts Videos To Remove ***")

	for filename in os.listdir ("./"):
		if ( re.match (r"c\d+.ts" , filename ) ):
			# Remove cX.ts file
			run('rm %s' % ( filename ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)


# This method is used for sorting
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def searchForConcatFilesAddAudioIfSilent():
	print ("*** Searching For cx.x Videos To Concat ***")

	listOfFilesToAlphabetize = []
	tmpNoAudioFilename=""
	sorttedFilesList = []
	filesToDelete = []
 
	for filename in os.listdir ("./"):
		if ( re.match (r"c\d+.*" , filename ) and  os.path.splitext(filename)[1] != ".ts"):
			# Display file name without extension
			#ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i c9.mp4 -shortest -c:v copy -c:a aac c9a.mov

			if ( getMediaAudioInfo ( filename, 'format', 'nb_streams' )	== 2 ):
				listOfFilesToAlphabetize.append( '%s' % ( filename ) )
			elif ( getMediaAudioInfo ( filename, 'format', 'nb_streams' ) == 1 ):
				tmpNoAudioFilename = os.path.splitext(filename)[0]+"_.mkv"
				print ("Adding Empty Audio To %s , tmpNoAudioFilename : %s" % (filename, tmpNoAudioFilename ) )
				run('ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i %s -shortest -c:v copy -c:a aac -y %s' % ( filename, tmpNoAudioFilename ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)	
				listOfFilesToAlphabetize.append( '%s' % ( tmpNoAudioFilename ) )
				filesToDelete.append ( tmpNoAudioFilename )

	for infile in sorted(listOfFilesToAlphabetize, key=numericalSort):
   		sorttedFilesList.append(infile)

	print ("sorttedFilesList ::  %s" % sorttedFilesList)

	return sorttedFilesList , filesToDelete


def removeTheseFiles( *removeList):
	absolutePath = os.path.dirname(os.path.realpath(__file__)) 

	for filename in removeList[0] :
			# Remove file
			print ( "Removing %s " % ( filename ) )
			run('rm %s/%s' % ( absolutePath, filename ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
			

def createStringForConcat ( *filesToConcat ) :
	inputFilesString = ""
	filterComplexInternalString = "" 
	vidPositionInList = ""
	filterComplexInternalStringNoAudio=""

	for i in filesToConcat[0] : 
		inputFilesString = inputFilesString + "-i "+ i+ " "
		vidPositionInList = filesToConcat[0].index( i )
		filterComplexInternalString = filterComplexInternalString + "[%s:v:0] [%s:a:0] " % ( vidPositionInList , vidPositionInList )
		filterComplexInternalStringNoAudio = filterComplexInternalStringNoAudio + "[%s:v:0] " % ( vidPositionInList )

	#print ( "inputFilesString : %s" % ( inputFilesString ) ) 
	#print ( "filterComplexInternalString : %s" % ( filterComplexInternalString ) ) 
	return inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio









def createStringForConcatFancyTransitions ( *filesToConcat ) :
	inputFilesString = ""
	filterComplexInternalString = "" 
	vidPositionInList = ""
	filterComplexInternalStringNoAudio=""
	filterComplexInternalStringNoAudioTrim=""
	filterComplexInternalStringNoAudioTrans=""
	filterComplexInternalStringNoAudioConcat=""
	
	filterComplexlastLine=""
	
	middleConcat=""
	endConcat=""
	counterA=0
	counterB=0
	
	# Choose type of transition for all the videos
	transSource = sys.argv[3]
	
	audioString=""
	audioString2=""
	audioConcat=""
	
	# This variable will store the length of the fancy transition
	#transDuration = 1
	transDuration = float( sys.argv[4] )
	
	myDuration = 0
	
	for i in filesToConcat[0] : 
		inputFilesString = inputFilesString + "-i "+ i+ " "
		vidPositionInList = filesToConcat[0].index( i )
		counterA=vidPositionInList*20
		counterB=counterA+10
		counterCTrim=counterA+1
		counterDTrim=counterA+10
		counterETrim=counterCTrim+10
		
		counterFTrans=counterETrim+10
		
		vidDuration=0

		
		#filterComplexInternalString = filterComplexInternalString + "[%s:v:0] [%s:a:0] " % ( vidPositionInList , vidPositionInList )
		#tmp = getMediaInfo ( i , 'streams', 1, 'duration' ) 
		#tmp = i
		#print ( "XXXXX vidDuration %s" % (  tmp ) )
		
		#print ( "Calling find_values " )
		#find_values ( "duration", i )
		#print ( "After Calling find_values " )
		
		vidDuration = float ( getMediaInfo ( i , 'streams', 1, 'duration' ) ) 
		myDuration = vidDuration - transDuration
	
		#audioString2 = audioString2 + "[%s:a]atrim=0:%s[a%s]; " % ( vidPositionInList, myDuration, vidPositionInList )
		
		audioConcat = audioConcat + "[a%s]" %  ( vidPositionInList )
		
		
		filterComplexInternalStringNoAudio = filterComplexInternalStringNoAudio + "[%s:v]split[v%s][v%s]; " % ( vidPositionInList, counterA, counterB  )
		
		filterComplexInternalStringNoAudioTrim = filterComplexInternalStringNoAudioTrim + "[v%s]trim=0:%s[v%s]; [v%s]trim=%s:%s,setpts=PTS-STARTPTS[v%s]; " % ( counterA, myDuration, counterCTrim, counterDTrim, myDuration, vidDuration, counterETrim )
		
		# Must limit this loop to one less than the length of this array
		if vidPositionInList < len (filesToConcat[0]) - 1 :
			filterComplexInternalStringNoAudioTrans = filterComplexInternalStringNoAudioTrans + "[v%s][v%s]gltransition=duration=1:source=%s[vt%s]; " % ( counterETrim, counterFTrans, transSource, vidPositionInList )
			middleConcat=middleConcat + "[vt%s]" % ( vidPositionInList )
			audioString2 = audioString2 + "[%s:a]atrim=0:%s[a%s]; " % ( vidPositionInList, myDuration, vidPositionInList )

		# This gets the final audio length of the last clip.  This is necessary because there is no transition.
		if vidPositionInList == len (filesToConcat[0]) - 1 :
			audioString2 = audioString2 + "[%s:a]atrim=0:%s[a%s]; " % ( vidPositionInList, vidDuration, vidPositionInList )
		
		#print (  "YYYYY vidPositionInList :  %s  len (filesToConcat[0]) : %s" % ( vidPositionInList, len (filesToConcat[0]) ) )
		
		endConcat = "[v%s]" % ( counterETrim  )

	filterComplexlastLine = '[v1]%s%sconcat=n=%s [v]' % ( middleConcat, endConcat, len (filesToConcat[0]) + 1 )
			
	#print ( "inputFilesString : %s" % ( inputFilesString ) ) 
	#print ( "filterComplexInternalStringNoAudioTrim : %s" % ( filterComplexInternalStringNoAudioTrim ) ) 
	#print ( "filterComplexInternalStringNoAudioTrans : %s" % ( filterComplexInternalStringNoAudioTrans ) ) 
	

	audioString = "%sconcat=n=%s:v=0:a=1[audio]" %  ( audioConcat ,len (filesToConcat[0]) )
	

	
	#print ( "filterComplexlastLine : %s" % ( filterComplexlastLine ) )
	#print ( "audioString : %s" % ( audioString ) )
	#print ( "audioString2 : %s" % ( audioString2 ) )
	#print ( "audioConcat : %s" % ( audioConcat ) )
	
	# Making a final longer string
	filterComplexInternalStringNoAudio = filterComplexInternalStringNoAudio + " %s %s %s" % ( filterComplexInternalStringNoAudioTrim, filterComplexInternalStringNoAudioTrans, filterComplexlastLine  )
	
	# Add audio
	filterComplexInternalString = "%s %s; %s" % ( audioString2, filterComplexInternalStringNoAudio, audioString )
	
	#print ( "filterComplexInternalStringNoAudio : %s" % ( filterComplexInternalStringNoAudio ) ) 
	#print ( "filterComplexInternalString : %s" % ( filterComplexInternalString ) ) 
	
	return inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio






# Help 

def displayHelp ():

	print ( '{:>30} {:<0}'. format ( "Examples :", "Videos | Audio | Photos\n" ) )
	print ( '{:>30} {:<0}'. format ( "Slice Vid 2 Time No Compr. : ", "./ffmpegHelper.py -s1 v.mov 0:34 0:39 out.mov" ) )
	print ( '{:>30} {:<0}'. format ( "Slice Vid 2 Rnge No Compr. : ", "./ffmpegHelper.py -s2 v.mov 0:34 0:39 out.mov" ) )
	print ( '{:>30} {:<0}'. format ( "IG Without Resize No Aud : ", "./ffmpegHelper.py -i1 v.mov 0:34 0:39 720:720:300:0 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "IG -W- Resize No Aud : ", "./ffmpegHelper.py -i2 v.mov 0:34 0:39 720:720:300:0 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Almost Lossless -W- Resize : ", "./ffmpegHelper.py -i3 v.mov 0:34 0:39 720:720:300:0 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "IG Without Resize : ", "./ffmpegHelper.py -i4 v.mov 0:34 0:39 720:720:300:0 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "YouTube Audio Removed : ", "./ffmpegHelper.py -y1 v.mov 0:34 0:39 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "YouTube : ", "./ffmpegHelper.py -y2 v.mov 0:34 0:39 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Concat Vids IG Brand : ", "./ffmpegHelper.py -c1 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Concat Vids Youtube BRND : ", "./ffmpegHelper.py -c2 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Combine Vids and Audio : ", "./ffmpegHelper.py -c3 v.mov out.mp3 out.mkv" ) )
	print ( '{:>30} {:<0}'. format ( "Concat Vids No Branding : ", "./ffmpegHelper.py -c4 out.mkv" ) )
	print ( '{:>30} {:<0}'. format ( "Concat Vids YT Brnd No A : ", "./ffmpegHelper.py -c5 out.mkv" ) )
	print ( '{:>30} {:<0}'. format ( "Concat Vids IG Brnd No A : ", "./ffmpegHelper.py -c6 out.mkv" ) )
	print ( '{:>30} {:<0}'. format ( "Concat MP4s No Transcoding : ", "./ffmpegHelper.py -c7 out.mp4" ) )	
	print ( '{:>30} {:<0}'. format ( "Concat Vids Fncy Trans No A : ", "./ffmpegHelper.py -c8 ./ffmpeg ./FilmBurn.glsl 1 N out.mp4" ) )	
	print ( '{:>30} {:<0}'. format ( "Concat Vids Fncy Trans W A : ", "./ffmpegHelper.py -c8 ./ffmpeg ./FilmBurn.glsl 1 Y out.mp4" ) )	
	print ( '{:>30} {:<0}'. format ( "Overlay Text/Image 2 Video : ", './ffmpegHelper.py -t1 out.mov "Overlayed Text" /pathto/font.ttf out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Overlay Text To Video : ", './ffmpegHelper.py -t2 text.mov "Overlayed Text" fontName 20 d90000 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Preview Video : ", './ffmpegHelper.py -p v.mov 0:34 0:39 720:720:300:0' ) )
	print ( '{:>30} {:<0}'. format ( "Slow Motion : ", './ffmpegHelper.py -e1 v.mov 4 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Slow Motion No Audio : ", './ffmpegHelper.py -e2 v.mov 0:34 0:39 2.5 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Black And White : ", './ffmpegHelper.py -e3 v.mov 0:34 0:39 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Black And White No Audio : ", './ffmpegHelper.py -e4 v.mov 0:34 0:39 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Extract Single Frame : ", './ffmpegHelper.py -e5 v.mov 0:34 image.png' ) )
	print ( '{:>30} {:<0}'. format ( "Scale Ratio Width : ", './ffmpegHelper.py -e6 v.mov 0:34 0:39 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Scale Ratio Width No Audio : ", './ffmpegHelper.py -e7 v.mov 0:34 0:39 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Scale Ratio Height : ", './ffmpegHelper.py -e8 v.mov 0:34 0:39 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Scale Ratio Height No Audio : ", './ffmpegHelper.py -e9 v.mov 0:34 0:39 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Resize Arbitrary : ", './ffmpegHelper.py -e10 v.mov 0:34 0:39 416 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Resize Arbitrary No Audio : ", './ffmpegHelper.py -e11 v.mov 0:34 0:39 416 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Combine Audio With Image : ", './ffmpegHelper.py -e12 i.png a.mp3 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Turn Image Into Video : ", './ffmpegHelper.py -e13 i.png 5 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Overlay Vid or Img On Video : ", './ffmpegHelper.py -e14 main.mov overlay.mp4 40 40 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Crossfade Video : ", './ffmpegHelper.py -e15 vid1.mov vid2.mov 2 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Side By Side Video : ", './ffmpegHelper.py -e16 left.mov right.mov out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Cut Out Portion Of Video : ", './ffmpegHelper.py -e17 s.mov 0:06 0 1280:50:0:400 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Slice Vid Compressed : ", './ffmpegHelper.py -e18 v.mov 0:34 0:39 out.mov' ) )
	print ( '{:>30} {:<0}'. format ( "Side By Side Video W Border : ", './ffmpegHelper.py -e19 c2.mov c1.mov 1 1 black out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Motion Design Audio BLog Design : ", './ffmpegHelper.py -e21 a.wav white out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Multiple Speed Up/Slowmo : ", './ffmpegHelper.py -e22 "2:10:2.5:2, 16:19:1.9:.4" out.mp4' ) )

	print ( '{:>30} {:<0}'. format ( "Audio Volume : ", './ffmpegHelper.py -a1 a.mp3 2 b.mp3' ) )
	print ( '{:>30} {:<0}'. format ( "Caption To A Photo : ", './ffmpegHelper.py -p1 i.png /pathto/font.ttf "Hello World" out.png' ) )
	print ( '{:>30} {:<0}'. format ( "Caption From temp.txt : ", './ffmpegHelper.py -p2 #123456 "#344567" /home/lex/share/Mo_De_Studio/audio_blog/Bookerly/Bookerly-Bold.ttf "1280x720" "#123456" 10 out.png' ) )
	print ( '{:>30} {:<0}'. format ( "Resize A Photo : ", './ffmpegHelper.py -p3 i.png 150X700! out.png' ) )

	print ( '{:>30} {:<0}'. format ( "Hint : ", "Use 0 to choose media length example : ./ffmpegHelper.py -p v.mov 0:34 0 720:720:300:0" ) )
	print ( '{:>30} {:<0}'. format ( "Hint : ", "To use c1 and c2 the filenames must be sequenced like this you can mix and match suffixes c1.xxx, c2.xxx ... c400.xxx " ) )
	print ( '{:>30} {:<0}'. format ( "Hint : ", "IG Means Instagram" ) )
	print ( '{:>30} {:<0}'. format ( "Help : ", "./ffmpegHelper.py -h" ) )

if ( sys.argv[1] == "-h"):
	displayHelp()

# ] Slicing A Video [

if ( sys.argv[1] == "-s1"):
	print ("*** Slice Video To Time No Compression***")
	ffmpeg_command = "-ss %s -to %s -c copy -y" % ( sys.argv[3],  media_duration )
	useFFmpegClass()

if ( sys.argv[1] == "-s2"):
	print ("*** Slice Video Range No Compression***")
	ffmpeg_command = "-ss " + sys.argv[3] + " -c copy -t " + media_duration + " -y"
	useFFmpegClass()

if ( sys.argv[1] == "-s3"):
	crop_value= sys.argv[5]
	print ("*** Slice Almost Lossless ***")
	ffmpeg_command = "-ss " + sys.argv[3] +" -t " + media_duration + " -codec:v libx264  -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -an -y"
	useFFmpegClass()

# ] For Instagram I [
# ffmpeg -i MVI_9579.MOV -i brandVideos.png -ss 00:00:14.0 -t 00:00:02.0 -codec:v libx264 -filter_complex "crop=640:640:440:50,overlay=x=10:y=10" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y 4.mp4

if ( sys.argv[1] == "-i1"):
	crop_value= sys.argv[5]
	print ("*** For Instagram Without Resize No Audio ***")
	ffmpeg_command = "-i brandVideos.png -ss " + sys.argv[3] +" -to " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +',overlay=x=10:y=10" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y"
	useFFmpegClass()

# ] For Instagram II [

if ( sys.argv[1] == "-i2"):
	crop_value= sys.argv[5]
	print ("*** For Instagram With Resize ***")
	ffmpeg_command = "-i brandVideos.png -ss " + sys.argv[3] +" -to " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +',scale=-1:640,overlay=x=10:y=10" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y"
	useFFmpegClass()

if ( sys.argv[1] == "-i3"):
	crop_value= sys.argv[5]
	print ("*** For Instagram Without Resize ***")
	ffmpeg_command = "-i brandVideos.png -ss " + sys.argv[3] +" -t " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +',overlay=x=10:y=10" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -y"
	useFFmpegClass()

# ] Almost Lossless [

# ffmpeg -i MVI_9632.MOV -i brandVideos.png -ss 00:00:12.0 -t 00:00:21.0 -codec:v libx264 -filter_complex "crop=720:720:220:0,scale=-1:640,overlay=x=10:y=10" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -an -y s1.mp4

if ( sys.argv[1] == "-i4"):
	crop_value= sys.argv[5]
	print ("*** Almost Lossless With Resize ***")
	ffmpeg_command = "-i brandVideos.png -ss " + sys.argv[3] +" -to " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +',overlay=x=10:y=10" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -y"
	useFFmpegClass()


##### Changing Brand Location

if ( sys.argv[1] == "-i42"):
	crop_value= sys.argv[5]
	print ("*** Almost Lossless With Resize ***")
	ffmpeg_command = "-i brandVideos.png -ss " + sys.argv[3] +" -to " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +',overlay=x=770:y=680" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -y"
	useFFmpegClass()



if ( sys.argv[1] == "-lex1"):
	print ("*** Concat Videos IG Brand Bottom Right ***")
	filesToConcat, filesToDelete = searchForConcatFilesAddAudioIfSilent ()

	inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio = createStringForConcat ( filesToConcat )

	#subprocess.call( 'ffmpeg -f concat -i l.txt -i brandVideos.png -filter_complex overlay=x=770:y=680 -c:v libx264 -c:a aac -preset slow -crf 18 -pix_fmt yuv420p -y ' + out_file , shell=True )

	print (  'RUNNING :: ffmpeg %s -filter_complex -i brandVideos.png " %s concat=n=%s:v=1:a=1 [v] [a]; [v]overlay=x=770:y=680 [out]" -map "[out]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file )  )

	# Branding Below 
	#run('ffmpeg %s -i brandVideos.png -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]; [v]overlay=x=770:y=680 [out]" -map "[out]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

	subprocess.call ('ffmpeg %s -i brandVideos.png -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]; [v]overlay=x=770:y=680 [out]" -map "[out]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ), shell=True)

	removeTheseFiles ( filesToDelete )
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )

########


# ] YouTube [

if ( sys.argv[1] == "-y1"):
	print ("*** YouTube and Other Video Sharing Sites Audio Removed ***")
	ffmpeg_command = "-i cornerFinalBlack.png -ss " + sys.argv[3] +" -to " + media_duration + ' -filter_complex "overlay=x=0:y=0" ' + " -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -an -movflags +faststart -y"
	useFFmpegClass()

# ] Audio Intact [

if ( sys.argv[1] == "-y2"):
	print ("*** YouTube and Other Video Sharing Sites ***")
	ffmpeg_command = "-i cornerFinalBlack.png -ss " + sys.argv[3] +" -to " + media_duration + ' -filter_complex "overlay=x=0:y=0" ' + " -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -movflags +faststart -y"
	useFFmpegClass()


# ] Overlay Text and Image To Video [

#ffmpeg -i c2.mov -i brand.png -filter_complex \
#"[0] [1] overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2 [b]; [b] drawtext=fontfile=/home/share/content/aiar/MyriadPro-Bold.ttf:text='WWW.MO-DE.NET/ACROBATICYOGA':fontcolor=0xFFFFFFFF:fontsize=36:x=20:y=10: \
#shadowcolor=0x000000EE:shadowx=2:shadowy=2" \
#-y c4.mov

if ( sys.argv[1] == "-t1"):
	print ("*** Overlay Text and Image To Video ***")
	ffmpeg_command = '-i brandVideos.png -filter_complex "[0] [1] overlay=x=10:y=10 [b]; [b] drawtext=fontfile=%s:text=%s:fontcolor=0xFFFFFFFF:fontsize=36:x=20:y=10: #shadowcolor=0x000000EE:shadowx=2:shadowy=2" -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -y' % ( media_duration, sys.argv[3] )

	useFFmpegClass()

if ( sys.argv[1] == "-t2"):
	print ("*** Overlay Text To Video ***")
	#ffmpeg_command = '-filter_complex "drawtext=fontfile=%s:text=%s:fontcolor=0xFFFFFFFF:fontsize=%s:x=20:y=10: #shadowcolor=0x000000EE:shadowx=2:shadowy=2" -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -y' % ( sys.argv[4], sys.argv[3], sys.argv[5] )
	#ffmpeg_command = '-filter_complex "drawtext=font=%s:text=%s:fontcolor=0x000000FF:fontsize=%s:x=20:y=10: #shadowcolor=0x000000EE:shadowx=2:shadowy=2" -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -y' % ( sys.argv[4], sys.argv[3], sys.argv[5] )
	ffmpeg_command = '-filter_complex "drawtext=font=%s:text=%s:fontcolor=0x%sFF:fontsize=%s:x=20:y=10: #shadowcolor=0x%sEE:shadowx=2:shadowy=2" -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -y' % ( sys.argv[4], sys.argv[3], sys.argv[6], sys.argv[5], sys.argv[6] )
	useFFmpegClass()

# Previewing A File

if ( sys.argv[1] == "-p"):
	print ("*** Preview Video ***")
	subprocess.call( 'ffplay -i %s -vf "crop=%s" -ss %s -t %s -loop 0' % ( video_file, sys.argv[5], sys.argv[3], media_duration ) , shell=True )


# ] Concat Videos Remove Audio [

if ( sys.argv[1] == "-c1"):
	print ("*** Concat Videos IG Brand  ***")

	filesToConcat, filesToDelete = searchForConcatFilesAddAudioIfSilent ()
	inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio = createStringForConcat ( filesToConcat )

	print ( 'RUNNING :: ffmpeg %s -i brandVideos.png -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]; [v]overlay=x=10:y=10 [out]" -map "[out]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ) )

	# Branding Below 
	subprocess.call ('ffmpeg %s -i brandVideos.png -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]; [v]overlay=x=10:y=10 [out]" -map "[out]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ), shell=True)

	removeTheseFiles ( filesToDelete )
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )


if ( sys.argv[1] == "-c2"):
	print ("*** Concat Videos Youtube Branding Remove Audio ***")

	filesToConcat, filesToDelete = searchForConcatFilesAddAudioIfSilent ()
	inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio = createStringForConcat ( filesToConcat )

	print ( 'RUNNING :: ffmpeg %s -i cornerFinalBlack.png -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]; [v]overlay=x=10:y=10 [out]" -map "[out]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ) )

	# Branding Below
	subprocess.call ('ffmpeg %s -i cornerFinalBlack.png -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]; [v]overlay=x=0:y=0 [out]" -map "[out]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ), shell=True)

	removeTheseFiles ( filesToDelete )
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )


#] Combine Video and Audio [
#ffmpeg -i v2.mkv -i a.mp3 -acodec copy -vcodec copy -map 0:v -map 1:a Output.mkv

if ( sys.argv[1] == "-c3"):
	print ("*** Combine Video and Audio ***")
	ffmpeg_command = '-i %s -acodec copy -vcodec copy -map 0:v -map 1:a -y' % ( sys.argv[3] )
	useFFmpegClass()


# Must Update To The Following
# ffmpeg -i c1.mov -i c2.mp4 -i c3.mp4 -i c4.mp4 -i c5.mp4 -i c6.mp4 -i c7.mkv -i c8.mp4 -filter_complex "[0:v:0] [1:v:0] [2:v:0] [3:v:0] [4:v:0] [5:v:0] [6:v:0] [7:v:0] concat=n=8:v=1 [v] " -map "[v]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y saraR_YT_20171025.mp4

if ( sys.argv[1] == "-c4"):
	print ("*** Concat Videos No Branding ***")

	filesToConcat, filesToDelete = searchForConcatFilesAddAudioIfSilent ()
	inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio = createStringForConcat ( filesToConcat )

	print ( 'RUNNING :: ffmpeg %s -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ) )

	# NO Branding Below
	subprocess.call ('ffmpeg %s -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ), shell=True)

	removeTheseFiles ( filesToDelete )
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )

# ] Slow Motion [
# ffmpeg -i s1.MOV -c copy -filter:v "setpts=2.5*PTS" -y s1s.MOV

if ( sys.argv[1] == "-c5"):
	print ("*** Concat Videos Youtube Branding Remove Audio ***")

	# ffmpeg -i c2.mov -i c3.mov -i c17_.mkv  -i cornerFinalBlack.png -filter_complex " [0:v:0] [1:v:0] [2:v:0]  concat=n=3:v=1 [v] ; [v]overlay=x=0:y=0 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -an -y saraR_YT_20180110.mp4

	filesToConcat, filesToDelete = searchForConcatFilesAddAudioIfSilent ()
	inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio = createStringForConcat ( filesToConcat )

	print (  'RUNNING :: ffmpeg %s -i cornerFinalBlack.png -filter_complex " %s concat=n=%s:v=1 [v] ; [v]overlay=x=0:y=0 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -an -y %s' % ( inputFilesString, filterComplexInternalStringNoAudio,  len ( filesToConcat ), out_file )  )

	# Branding Below
	#subprocess.call ('ffmpeg %s -i cornerFinalBlack.png -filter_complex " %s concat=n=%s:v=1:a=1 [v] [a]; [v]overlay=x=0:y=0 [out]" -map "[out]" -map "[a]" -vcodec libx264 -crf 23 -preset medium -strict experimental -ab 128k -an -y %s' % ( inputFilesString, filterComplexInternalString,  len ( filesToConcat ), out_file ), shell=True)

	subprocess.call ('ffmpeg %s -i cornerFinalBlack.png -filter_complex " %s concat=n=%s:v=1 [v] ; [v]overlay=x=0:y=0 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -an -y %s' % ( inputFilesString, filterComplexInternalStringNoAudio,  len ( filesToConcat ), out_file ), shell=True)

	removeTheseFiles ( filesToDelete )
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )

if ( sys.argv[1] == "-c6"):
	print ("*** Concat Videos IG Branding Remove Audio ***")

	filesToConcat, filesToDelete = searchForConcatFilesAddAudioIfSilent ()
	inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio = createStringForConcat ( filesToConcat )

	print (  'RUNNING :: ffmpeg %s -i brandVideos.png -filter_complex " %s concat=n=%s:v=1 [v] ; [v]overlay=x=10:y=10 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -an -y %s' % ( inputFilesString, filterComplexInternalStringNoAudio,  len ( filesToConcat ), out_file )  )


	subprocess.call ('ffmpeg %s -i brandVideos.png -filter_complex " %s concat=n=%s:v=1 [v] ; [v]overlay=x=10:y=10 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -an -y %s' % ( inputFilesString, filterComplexInternalStringNoAudio,  len ( filesToConcat ), out_file ), shell=True)

	removeTheseFiles ( filesToDelete )
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )

if ( sys.argv[1] == "-c7"):
	print ("*** Concat MP4 Videos No Transcoding, might work with other media formats \nIf videos they must all have auido or none. \nIt fails if mixed.***")
	filesToConcat, filesToDelete = searchForConcatFilesToTs ()
	print (  'RUNNING :: ffmpeg -i "%s" -c copy -bsf:a aac_adtstoasc -y %s' % ( filesToConcat, out_file  ) )
	subprocess.call ('ffmpeg -i "%s" -c copy -bsf:a aac_adtstoasc -y %s' % ( filesToConcat, out_file ), shell=True)	
	removeTheseFiles (filesToDelete)
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )

	
	
	
	#./ffmpegHelper.py -c8 ./ffmpeg ./FilmBurn.glsl 1 Y o.mp4

	
	
	# ] Concat Videos Remove Audio Nice Transitions [

if ( sys.argv[1] == "-c8"):
	print ("*** C8 Concat Videos IG Brand Nice Transition  ***")

	filesToConcat, filesToDelete = searchForConcatFilesAddAudioIfSilent ()
	inputFilesString, filterComplexInternalString, filterComplexInternalStringNoAudio = createStringForConcatFancyTransitions ( filesToConcat )
	
	#path2SpecialFFpeg="/home/lex/share/python/ffmpegHelper/ffmpeg/ffmpeg"
	#path2SpecialFFpeg="./ffmpeg"
	# Set path for the specially compile ffmpeg with gl-transitions
	path2SpecialFFpeg=sys.argv[2]
	
	# Add or remove audio variable
	addRemoveAudio = sys.argv[5]
	
	# Temporarily removing branding because of a bug in ffmpeg that I can not resolve easily. 
	
	if addRemoveAudio == "Y" :
		print ( "ADDING AUDIO" )
		#print ( 'RUNNING :: %s %s -i brandVideos.png -filter_complex " %s [v]overlay=x=10:y=10 [out]" -map "[out]" -map "[audio]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalString, out_file ) )
		
		print ( 'RUNNING :: %s %s -filter_complex " %s" -map "[v]" -map "[audio]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalString, out_file ) )
		
		# Branding Below 
		#subprocess.call ('%s %s -i brandVideos.png -filter_complex " %s [v]overlay=x=10:y=10 [out]" -map "[out]" -map "[audio]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalString, out_file  ), shell=True)
				
		subprocess.call ('%s %s -filter_complex " %s" -map "[v]" -map "[audio]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalString, out_file  ), shell=True)
				
	elif addRemoveAudio == "N" :
		print ( "REMOVING AUDIO" )
		print ( 'RUNNING :: %s %s -i brandVideos.png -filter_complex " %s; [v]overlay=x=10:y=10 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalStringNoAudio, out_file ) )
		
		# Branding Below 
		#subprocess.call ('%s %s -i brandVideos.png -filter_complex " %s; [v]overlay=x=10:y=10 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalStringNoAudio, out_file ), shell=True)
		
		subprocess.call ('%s %s -filter_complex " %s" -map "[v]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalStringNoAudio, out_file ), shell=True)
			
			
	
	#print ( "inputFilesString : " + inputFilesString )
	#print ( "filterComplexInternalString : " + filterComplexInternalString )
	#print ( "filterComplexInternalStringNoAudio : " + filterComplexInternalStringNoAudio )
	
	#print ( 'RUNNING :: %s %s -i brandVideos.png -filter_complex " %s; [v]overlay=x=10:y=10 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalStringNoAudio, out_file ) )

		# Branding Below 
	#subprocess.call ('%s %s -i brandVideos.png -filter_complex " %s; [v]overlay=x=10:y=10 [out]" -map "[out]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( path2SpecialFFpeg, inputFilesString, filterComplexInternalStringNoAudio, out_file ), shell=True)
	
	removeTheseFiles ( filesToDelete )
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
if ( sys.argv[1] == "-e1"):
	print ("*** Slow Motion ***")
	ffmpeg_command = '-c:v libx264 -preset slow -filter_complex "setpts=%s*PTS" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -y' % ( sys.argv[3]  )
	useFFmpegClass()

if ( sys.argv[1] == "-e2"):
	print ("*** Slow Motion No Audio ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -filter_complex "setpts=%s*PTS" -crf 0 -preset ultrafast -an -y' % ( sys.argv[3], media_duration, sys.argv[5]  )
	useFFmpegClass()

# ] Black and White with No Audio [
#ffmpeg -i MVI_5487.MOV -ss 00:00:14.0 -t 00:00:6.0 -an -vf format=gray,format=yuv422p c.MOV

if ( sys.argv[1] == "-e3"):
	print ("*** Black And White ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -vf "format=gray,format=yuv422p" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -y' % ( sys.argv[3], media_duration )
	useFFmpegClass()

if ( sys.argv[1] == "-e4"):
	print ("*** Black And White No Audio ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -vf "format=gray,format=yuv422p" -crf 0 -preset ultrafast -an -y' % ( sys.argv[3], media_duration )
	useFFmpegClass()

# ] Extract Single Frame [

# ffmpeg -i MVI_5486.MOV -vframes 1 -ss 00:00:40 $(date +%Y%m%d-%H%M%S).png
if ( sys.argv[1] == "-e5"):
	print ("*** Extract Single Frame ***")
	ffmpeg_command = '-vframes 1 -ss %s -y' % ( sys.argv[3] )
	useFFmpegClass()

# ] Resive A Video [

#ffmpeg -i l1.MOV -filter:v scale=-1:640 -c:a copy l2.mov

if ( sys.argv[1] == "-e6"):
	print ("*** Scale 2 Ratio Width ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -filter_complex "scale=%s:-1" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -y' % ( sys.argv[3], media_duration, sys.argv[5] )
	useFFmpegClass()

if ( sys.argv[1] == "-e7"):
	print ("*** Scale 2 Ratio Width No Audio ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -filter_complex "scale=%s:-1" -crf 0 -preset ultrafast -an -y' % ( sys.argv[3], media_duration, sys.argv[5] )
	useFFmpegClass()

if ( sys.argv[1] == "-e8"):
	print ("*** Scale 2 Ratio Height ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -filter_complex "scale=-1:%s" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -y' % ( sys.argv[3], media_duration, sys.argv[5] )
	useFFmpegClass()

if ( sys.argv[1] == "-e9"):
	print ("*** Scale 2 Ratio Height No Audio ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -filter_complex "scale=-1:%s" -crf 0 -preset ultrafast -an -y' % ( sys.argv[3], media_duration, sys.argv[5] )
	useFFmpegClass()

if ( sys.argv[1] == "-e10"):
	print ("*** Resize Arbitrary ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -filter_complex "scale=%s:%s" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -y' % ( sys.argv[3], media_duration, sys.argv[5], sys.argv[6] )
	useFFmpegClass()

if ( sys.argv[1] == "-e11"):
	print ("*** Resize Arbitrary No Audio ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -filter_complex "scale=%s:%s" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -an -y' % ( sys.argv[3], media_duration, sys.argv[5], sys.argv[6] )
	useFFmpegClass()

if ( sys.argv[1] == "-e12"):
	print ("*** Combine Audio With Image ***")
	subprocess.call( 'ffmpeg -loop 1 -i %s -i %s -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -movflags +faststart -y -shortest %s' % ( video_file, sys.argv[3], out_file ) , shell=True )

if ( sys.argv[1] == "-e13"):
	print ("*** Turn Image Into Video ***")
	run('ffmpeg -loop 1 -framerate 30000/1001 -i %s -c:v libx264 -profile:v baseline -t %s -pix_fmt yuvj420p -y %s' % ( video_file, sys.argv[3], out_file ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	subprocess.call( 'mplayer %s -loop 0'  % ( out_file ) , shell=True )


if ( sys.argv[1] == "-e14"):
	print ("*** Overlay Vid or Img On Video  ***")
	vid1hasAudio = getMediaAudioInfo ( video_file, 'format', 'nb_streams' )
	vid2hasAudio = getMediaAudioInfo ( sys.argv[3], 'format', 'nb_streams' )

	if ( vid1hasAudio >1 and vid2hasAudio >1):
		ffmpeg_command = '-i %s -filter_complex "[0:v][1:v]overlay=x=%s:y=%s:eof_action=pass; [0:a][1:a]amix" -c:v libx264 -preset slow -crf 0 -preset ultrafast -y' % ( sys.argv[3], sys.argv[4], sys.argv[5] )
	else :
		ffmpeg_command = '-i %s -filter_complex "[0:v][1:v]overlay=x=%s:y=%s:eof_action=pass" -c:v libx264 -preset slow -crf 0 -preset ultrafast -y' % ( sys.argv[3], sys.argv[4], sys.argv[5] )
	useFFmpegClass()


if ( sys.argv[1] == "-e15"):
	print ("*** Crossfade Video  ***")
	W = getMediaInfo ( video_file, 'streams', 0, 'width' )
	H = getMediaInfo ( video_file, 'streams', 0, 'height' )
	v1Length = float ( getMediaInfo ( video_file, 'streams', 1, 'duration' ))
	sumOfSpecialAffect = v1Length  + float ( getMediaInfo ( sys.argv[3], 'streams', 1, 'duration' ) ) - float ( sys.argv[4] )
	FadeDuration = sys.argv[4]
	ffmpeg_command = '-i %s -filter_complex "color=black:%sx%s:d=%s[base]; [0:v]setpts=PTS-STARTPTS[v0]; [1:v]format=yuva420p,fade=in:st=0:d=%s:alpha=1, setpts=PTS-STARTPTS+((%s-%s)/TB)[v1]; [base][v0]overlay[tmp]; [tmp][v1]overlay,format=yuv420p[fv]; [0:a][1:a]acrossfade=d=%s[fa] " -map [fv] -map [fa] -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart -y' % ( sys.argv[3], W, H, sumOfSpecialAffect, FadeDuration, v1Length, FadeDuration, FadeDuration )
	useFFmpegClass()


if ( sys.argv[1] == "-e16"):
	print ("*** Side By Side Video  ***")
	# Check that both streams have audio if not remove the mix audio from the ffmpeg command
	vid1hasAudio = getMediaAudioInfo ( video_file, 'format', 'nb_streams' )
	vid2hasAudio = getMediaAudioInfo ( sys.argv[3], 'format', 'nb_streams' )

	if ( vid1hasAudio >1 and vid2hasAudio >1):
		ffmpeg_command = '-i %s -filter_complex "[0:v]setpts=PTS-STARTPTS, pad=iw*2:ih[bg]; [1:v]setpts=PTS-STARTPTS[fg]; [bg][fg]overlay=w; [0:a][1:a]amix" -y' % ( sys.argv[3] )
	else:
		ffmpeg_command = '-i %s -filter_complex "[0:v]setpts=PTS-STARTPTS, pad=iw*2:ih[bg]; [1:v]setpts=PTS-STARTPTS[fg]; [bg][fg]overlay=w" -y' % ( sys.argv[3] )
	useFFmpegClass()


if ( sys.argv[1] == "-e17"):
	crop_value= sys.argv[5]
	print ("*** Cut Out Portion Of Video ***")
	#ffmpeg_command = "-ss " + sys.argv[3] +" -t " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +'" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -y"
	ffmpeg_command = '-ss %s -t %s -codec:v libx264 -filter_complex "crop=%s" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y ' % ( sys.argv[3], media_duration, sys.argv[5] )
	useFFmpegClass()

if ( sys.argv[1] == "-e18"):
	crop_value= sys.argv[5]
	print ("*** Croping Video ***")
	print  ( "media_duration :: " + media_duration )
	ffmpeg_command = "-ss " + sys.argv[3] +" -to " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +'" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -y"
	useFFmpegClass()


if ( sys.argv[1] == "-e19"):
	print ("*** Side By Side Video With Border ***")
	# Check that both streams have audio if not remove the mix audio from the ffmpeg command
	vid1hasAudio = getMediaAudioInfo ( video_file, 'format', 'nb_streams' )
	vid2hasAudio = getMediaAudioInfo ( sys.argv[3], 'format', 'nb_streams' )
	w_Left = getMediaInfo ( video_file, 'streams', 0, 'width' )
	w_Right = getMediaInfo ( sys.argv[3] , 'streams', 0, 'width' )
	h_Left = getMediaInfo ( video_file, 'streams', 0, 'height' )
	h_Right = getMediaInfo ( sys.argv[3] , 'streams', 0, 'height' )
	leftNewWidth = w_Left - int ( sys.argv[4] )
	rigthNewWidth = w_Right - int ( sys.argv[5] )
	borderColor =  sys.argv[6]

	if ( vid1hasAudio >1 and vid2hasAudio >1):
		ffmpeg_command = '-i %s -filter_complex "[0:v]crop=%s:%s, pad=%s:%s:0:0:%s[tmp0]; [1:v]crop=%s:%s, pad=%s:%s:%s:0:%s[tmp1]; [tmp0][tmp1]hstack[v];[0:a][1:a]amerge=inputs=2[a]" -map "[v]" -map "[a]" -ac 2 -y' % ( sys.argv[3], leftNewWidth, h_Left, w_Left, h_Left, borderColor, rigthNewWidth, h_Right, w_Right, h_Right, sys.argv[5], borderColor )
	else:
		ffmpeg_command = '-i %s -filter_complex "[0:v]crop=%s:%s, pad=%s:%s:0:0:%s[tmp0]; [1:v]crop=%s:%s, pad=%s:%s:%s:0:%s[tmp1]; [tmp0][tmp1]hstack[v] " -map "[v]" -y' % ( sys.argv[3], leftNewWidth, h_Left, w_Left, h_Left, borderColor, rigthNewWidth, h_Right, w_Right, h_Right, sys.argv[5], borderColor )
	useFFmpegClass()


if ( sys.argv[1] == "-e20"):
	crop_value= sys.argv[5]
	print ("*** Cut Out Portion Of Video And Brand ***")
	#ffmpeg_command = "-ss " + sys.argv[3] +" -t " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +'" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -y"
	ffmpeg_command = '-i brandVideos.png -ss %s -t %s -codec:v libx264 -filter_complex "crop=%s, overlay=x=10:y=10" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y ' % ( sys.argv[3], media_duration, sys.argv[5] )
	useFFmpegClass()


# ffmpeg -i tmp2.wav -i brandVideos.png -filter_complex "[0:a]showwaves=s=1280x720:mode=point:colors=white, overlay=x=10:y=10, drawtext=font=Open Sans Extrabold:textfile=temp.txt:fontcolor=0xFFFFFFFF:fontsize=30:x=10:y=60: #shadowcolor=0xFFFFFFEE:shadowx=2:shadowy=2,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -c:a copy -y tS2017101.mkv 

if ( sys.argv[1] == "-e21"):
	print ("*** Motion Design Audio BLog Design ***")
	ffmpeg_command = '-i brandVideos.png -filter_complex "[0:a]showwaves=s=1280x720:mode=point:colors=%s, overlay=x=10:y=10, drawtext=font=Open Sans Extrabold:textfile=temp.txt:fontcolor=0xFFFFFFFF:fontsize=30:x=10:y=60: #shadowcolor=0xFFFFFFEE:shadowx=2:shadowy=2,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -c:a copy -y ' % ( sys.argv[3] )
	useFFmpegClass()


	
	
	
# ./ffmpegHelper.py -e22 s2.mov  "2:10:.5, 16:19:.5" o.mp4	

# ./ffmpegHelper.py -e22 s2.mov  "2:10:.5:2.5, 16:20:.3:1.9" o.mp4	
	
	
	
	
if ( sys.argv[1] == "-e22"):
	print ("*** Multiple Speed Up ***")
	
	vidDuration = float ( getMediaInfo ( sys.argv[2] , 'streams', 1, 'duration' ) )
	
	videoString=""
	audioString=""
	concatString=""
	
	ts=""
	
	# This stores the volume of each cut from the commandline
	cutVolume = ""
		
	# List Of Cuts
	cutList = []
	# Build list from commandline parameter
	tmpList=list ( sys.argv[3].replace(" ","").split(",") )
	
	# Adding to list so code outputs beginning and end.
	addToEnd = "%s:%s" % ( vidDuration, vidDuration )
	addToBeginning  = "0:0"
	
	tmpList.append( addToEnd )
	tmpList.insert( 0, addToBeginning )
	
	length = len ( tmpList )

	i=0	
	while i < length-1:
		
		# Get all the values after the colons
		matchLast = tmpList[i].split(":")
		matchFirst = tmpList[i+1].split(":")

		# Build list containing cut points
		#cutList.append( "%s:%s" % ( matchLast[0], matchLast[1]  ) )
		
		#tt =  str ( matchLast[0] ).zfill(2)
		#print ( "XX %s" % ( tt ) )
		#print ( "matchLast[2] %s" % ( matchLast[1] ) )
		#print ( "matchLast %s" % ( matchLast ) )
		#print ( "Length matchLast %s" % ( len ( matchLast ) ) )
		
		# The zfill's are to padd single digits so they do not break things such as 03
		# This feel potentially buggy if it encounters a character that is not numeric then what?
		
		if  len ( matchLast ) == 2 :
			cutList.append( "%s:%s" % (  str ( matchLast[0] ).zfill(2) , str ( matchLast[1] ).zfill(2)  ) )
		elif len ( matchLast ) > 2 :
			#cutList.append( "%s:%s:%s" % (  str ( matchLast[0] ).zfill(2) , str ( matchLast[1] ).zfill(2),  str ( matchLast[2] ).zfill(2)  ) )
			
			# loop over this list because its length can be anything to build cutlist
			for searchingVolume in  matchLast :
				#print ( " matchLast  %s" %  ( str ( searchingVolume ).zfill(2)   )  ) 
				ts+=  "%s:" %  ( str ( searchingVolume ).zfill(2)   ) 
		
		#print ( "ts = %s" % ( ts[:-1] ))
			cutList.append( "%s" % (   ts[:-1]  ) )
			ts=""
		
		# This adds the in between time intervals for the transitions. 
		cutList.append( "%s:%s" % ( str ( matchLast[1] ).zfill(2) , str ( matchFirst[0] ).zfill(2)  ) )
		print ( "  str ( matchLast[1] ).zfill(2) ::::: %s  str ( matchFirst[0] ).zfill(2)  ) :::  " %  (   str ( matchLast[1] ).zfill(2) ) ,     str ( matchFirst[0] ).zfill(2)      ) 
		
		i+=1
		
	#print ( "cutList = %s " % ( cutList ))
	
	ii=0
	lengthOfCutList = len ( cutList[1:]  ) 
	while ii < lengthOfCutList:
		if len (  cutList[1:][ii].split(":")  ) == 2 : 
			#print ( "[0:v]trim=%s:%s,setpts=PTS-STARTPTS[v%s]; " % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , ii  )   ) 
			#print ( "[0:a]atrim=%s:%s,asetpts=PTS-STARTPTS[a%s]; " % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , ii  )   ) 
			videoString += "[0:v]trim=%s:%s,setpts=PTS-STARTPTS[v%s]; " % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , ii  )
			
			audioString += "[0:a]atrim=%s:%s,asetpts=PTS-STARTPTS[a%s]; " % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , ii  )
		elif len (  cutList[1:][ii].split(":")  ) > 2 :
			
			# Get volume value if passed.  If not set it to one.
			
			try:
				#print ( "cutList[1:][ii].split(':')[3] %s" % ( cutList[1:][ii].split(":")[3] )   )
				cutVolume =  cutList[1:][ii].split(":")[3]
			except IndexError:
				cutVolume = 1
				print ( "cutVolume %s", ( cutVolume ) )
			
			
			
			#print ( "[0:v]trim=%s:%s,setpts=PTS-STARTPTS,setpts=%s*PTS[v%s];" % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , cutList[1:][ii].split(":")[2] , ii  )   ) 
			#print ( "[0:a]atrim=%s:%s,asetpts=PTS-STARTPTS,atempo=1/%s[a%s];" % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , cutList[1:][ii].split(":")[2] , ii  )   )			
			
			videoString += "[0:v]trim=%s:%s,setpts=PTS-STARTPTS,setpts=%s*PTS[v%s]; " % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , cutList[1:][ii].split(":")[2] , ii  )
			#audioString += "[0:a]atrim=%s:%s,asetpts=PTS-STARTPTS,atempo=1/%s[a%s];" % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , cutList[1:][ii].split(":")[2] , ii  ) 
			
			audioString += "[0:a]atrim=%s:%s,asetpts=PTS-STARTPTS,atempo=1/%s,volume=%s[a%s]; " % (  cutList[1:][ii].split(":")[0] , cutList[1:][ii].split(":")[1] , cutList[1:][ii].split(":")[2] , cutVolume ,ii  )
			
			#print ( "volume = %s", (  cutList[1:][ii].split(":") )  )
			#print ( "cutList[1:][ii].split(':')[3] %s" % ( cutList[1:][ii].split(":")[3] )   )
			
		ii+=1
	
	iii=0
	while iii < ii:
		concatString+= "[v%s][a%s]" % ( iii, iii ) 
		iii+=1
	
	concatString+= "concat=n=%s:v=1:a=1[v][audio]" % ( iii )
	
	print ( 'RUNNING :: ffmpeg -i %s -filter_complex " %s %s %s" -map "[v]" -map "[audio]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( video_file, videoString, audioString, concatString, out_file  ) )
	
	
	subprocess.call ('ffmpeg -i %s -filter_complex " %s %s %s" -map "[v]" -map "[audio]" -vcodec libx264 -crf 23 -preset medium -acodec aac -strict experimental -ac 2 -ar 44100 -ab 128k -y %s' % ( video_file, videoString, audioString, concatString, out_file  ), shell=True)
	
	subprocess.call( 'mplayer -loop 0 %s'  % ( out_file ) , shell=True )

	
	
	
	
	

if ( sys.argv[1] == "-a1"):
	print ("*** Audio Volume ***")
	ffmpeg_command = '-af "volume=%s" -y' % ( sys.argv[3] )
	useFFmpegClass()

#[ Add caption to a photo ]

if ( sys.argv[1] == "-p1"):
	print ("*** Caption To A Photo ***")
	subprocess.call( "convert %s -fill white -stroke none -font %s  -pointsize 30 -gravity NorthWest -annotate 0 '%s' %s" % ( video_file, sys.argv[3], sys.argv[4], out_file ) , shell=True )
	run('display %s' % ( out_file), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

if ( sys.argv[1] == "-p2"):
	print ("*** Caption From temp.txt ***")
	#print ( 'convert -background %s -fill %s -font %s -size %s caption:"$(cat ./temp.txt)" -bordercolor %s -border %s %s' % ( sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], out_file ) )

	# Generate random number to store the file as that name
	# I must do this because convert does not generate a file with the text in it
	# that matches the users request

	randomFileName =  '%s.png' % ( randint (9000, 22000 ) )
	print ( randomFileName ) 
	subprocess.call( 'convert -background %s -fill %s -font %s -size %s caption:"$(cat ./temp.txt)" -bordercolor %s -border %s %s' % ( "'"+sys.argv[2]+"'", "'"+sys.argv[3]+"'", sys.argv[4], sys.argv[5], "'"+sys.argv[6]+"'", sys.argv[7], randomFileName ) , shell=True )

	# resize to match the size passed
	run('convert %s -resize %s %s' % ( randomFileName, sys.argv[5]+"!", out_file), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	# Delete temp file
	run('rm %s' % ( randomFileName ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	# Preview caption
	run('display %s' % ( out_file), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

if ( sys.argv[1] == "-p3"):
	print ("*** Resize Image ***")
	subprocess.call( "convert %s -resize %s %s" % ( video_file, sys.argv[3], out_file ) , shell=True )
	run('display %s' % ( out_file), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
