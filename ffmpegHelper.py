#!/usr/bin/env python3.5

import ffmpy 
import sys
import subprocess
from subprocess import PIPE, run
import re

print ( "Numer arguments : ", len(sys.argv), " arguments.")

print ( "Argument List : " , str (sys.argv) )

video_file = ""
ffmpeg_command=""
crop_value=""
media_duration =""
out_file=""

#if ( not re.search('-(h|c1)', sys.argv[1] ) ):

def getMediaLength( the_file ):
	print ( "CALCULATING %s LENGTH" % ( the_file ) )

	getMediaLengthValue = run('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -sexagesimal %s' % ( the_file ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	return  getMediaLengthValue.stdout 

# If not help set values
if ( not re.search('-(h)', sys.argv[1] ) ):
	print ( "Setting values for video_file and out_file"  )
	video_file=sys.argv[2]
	out_file=sys.argv[ len(sys.argv) - 1 ] # The last value passed to the code
	media_duration = getMediaLength( video_file ) if sys.argv[4] == "0" else sys.argv[4] 

def useFFmpegClass():
	ff = ffmpy.FFmpeg( 
		inputs={ video_file : None},	
		outputs={ out_file : ffmpeg_command } 
	)
	print ( ff.cmd )
	ff.run()
	# Run a preview of the video
	subprocess.call( 'mplayer %s -loop 0'  % ( out_file ) , shell=True )

# Help 

def displayHelp ():

	print ( '{:>30} {:<0}'. format ( "Examples :", "Videos\n" ) )
	print ( '{:>30} {:<0}'. format ( "Slicing Videos To Time : ", "./ffmpegHelper.py -s1 v.mov 0:34 0:39 out.mov" ) )
	print ( '{:>30} {:<0}'. format ( "Slicing Videos To Range : ", "./ffmpegHelper.py -s2 v.mov 0:34 0:39 out.mov" ) )
	print ( '{:>30} {:<0}'. format ( "Instagram Without Resize : ", "./ffmpegHelper.py -i1 v.mov 0:34 0:39 720:720:300:0 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Instagram With Resize : ", "./ffmpegHelper.py -i2 v.mov 0:34 0:39 720:720:300:0 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Almost Lossless With Resize : ", "./ffmpegHelper.py -i3 v.mov 0:34 0:39 720:720:300:0 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "YouTube Audio Removed : ", "./ffmpegHelper.py -y1 v.mov 0:34 0:39 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "YouTube : ", "./ffmpegHelper.py -y2 v.mov 0:34 0:39 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Concat Videos : ", "./ffmpegHelper.py -c1 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Concat Videos Youtube BRND : ", "./ffmpegHelper.py -c2 out.mp4" ) )
	print ( '{:>30} {:<0}'. format ( "Combine Video and Audio : ", "./ffmpegHelper.py -c3 v.mov out.mp3 out.mkv" ) )
	print ( '{:>30} {:<0}'. format ( "Overlay Text and Image : ", './ffmpegHelper.py -t1 out.mov "Overlayed Text" /pathto/font.ttf out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Overlay Text : ", './ffmpegHelper.py -t2 text.mov "Overlayed Text" /pathto/font.ttf out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Preview Video : ", './ffmpegHelper.py -p v.mov 0:34 0:39 720:720:300:0' ) )
	print ( '{:>30} {:<0}'. format ( "Slow Motion : ", './ffmpegHelper.py -e1 v.mov 0:34 0:39 2.5 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Slow Motion No Audio : ", './ffmpegHelper.py -e2 v.mov 0:34 0:39 2.5 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Black And White : ", './ffmpegHelper.py -e3 v.mov 0:34 0:39 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Black And White No Audio : ", './ffmpegHelper.py -e4 v.mov 0:34 0:39 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Extract Single Frame : ", './ffmpegHelper.py -e5 v.mov 0:34 image.png' ) )
	print ( '{:>30} {:<0}'. format ( "Scale Ratio Width : ", './ffmpegHelper.py -e6 v.mov 0:34 0:39 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Scale Ratio Width No Audio : ", './ffmpegHelper.py -e7 v.mov 0:34 0:39 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Scale Ratio Height : ", './ffmpegHelper.py -e8 v.mov 0:34 0:39 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Scale Ratio Height No Audio : ", './ffmpegHelper.py -e9 v.mov 0:34 0:39 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Resize Arbitrary : ", './ffmpegHelper.py -e10 v.mov 0:34 0:39 416 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Resize Arbitrary No Audio : ", './ffmpegHelper.py -e11 v.mov 0:34 0:39 416 416 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Combine Audio With Image : ", './ffmpegHelper.py -e12 i.png a.mp3 out.mp4' ) )
	print ( '{:>30} {:<0}'. format ( "Audio Volume : ", './ffmpegHelper.py -a1 a.mp3 2 b.mp3' ) )
	print ( '{:>30} {:<0}'. format ( "Add Caption To A Photo : ", './ffmpegHelper.py -p1 i.png /pathto/font.ttf "Hello World" out.png
' ) )
	print ( '{:>30} {:<0}'. format ( "Resize A Photo : ", './ffmpegHelper.py -p2 i.png 150X700! out.png
' ) )

	print ( '{:>30} {:<0}'. format ( "Hint : ", "Use 0 to choose media length example : ./ffmpegHelper.py -p v.mov 0:34 0 720:720:300:0" ) )
	print ( '{:>30} {:<0}'. format ( "Help : ", "./ffmpegHelper.py -h" ) )

if ( sys.argv[1] == "-h"):
	displayHelp()

# ] Slicing A Video [

# ffmpeg -i MVI_5487.MOV -ss 00:00:14.0 -c copy -t 00:00:6.0 -an b.MOV

# ./ffmpegHelper.py -s v.mov 0:34 0:39 myout.mov


if ( sys.argv[1] == "-s1"):
	print ("*** Slicing Video To Time***")
	ffmpeg_command = "-ss %s -c copy -to %s -y" % ( sys.argv[3],  media_duration )

	useFFmpegClass()


if ( sys.argv[1] == "-s2"):
	print ("*** Slicing Video Range***")
	ffmpeg_command = "-ss " + sys.argv[3] + " -c copy -t " + media_duration + " -y"
	useFFmpegClass()

if ( sys.argv[1] == "-s3"):
	crop_value= sys.argv[5]
	print ("*** Slice Almost Lossless ***")
	ffmpeg_command = "-ss " + sys.argv[3] +" -t " + media_duration + " -codec:v libx264  -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -an -y"
	useFFmpegClass()

# ] For Instagram I [
# ffmpeg -i MVI_9579.MOV -i brandVideos.png -ss 00:00:14.0 -t 00:00:02.0 -codec:v libx264 -filter_complex "crop=640:640:440:50,overlay=x=10:y=10" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y 4.mp4

# ./ffmpegHelper.py -i1 v.mov 0:34 0:39 720:720:300:0 out.mov

if ( sys.argv[1] == "-i1"):
	crop_value= sys.argv[5]
	print ("*** For Instagram Without Resize ***")
	ffmpeg_command = "-i brandVideos.png -ss " + sys.argv[3] +" -t " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +',overlay=x=10:y=10" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y"
	useFFmpegClass()

# ] For Instagram II [

# ./ffmpegHelper.py -i2 v.mov 0:34 0:39 720:720:300:0 out.mov

if ( sys.argv[1] == "-i2"):
	crop_value= sys.argv[5]
	print ("*** For Instagram With Resize ***")
	ffmpeg_command = "-i brandVideos.png -ss " + sys.argv[3] +" -t " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +',scale=-1:640,overlay=x=10:y=10" ' +" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y"
	useFFmpegClass()

# ] Almost Lossless [

# ffmpeg -i MVI_9632.MOV -i brandVideos.png -ss 00:00:12.0 -t 00:00:21.0 -codec:v libx264 -filter_complex "crop=720:720:220:0,scale=-1:640,overlay=x=10:y=10" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -an -y s1.mp4

# ./ffmpegHelper.py -i3 v.mov 0:34 0:39 720:720:300:0 out.mov

if ( sys.argv[1] == "-i3"):
	crop_value= sys.argv[5]
	print ("*** Almost Lossless With Resize ***")
	ffmpeg_command = "-i brandVideos.png -ss " + sys.argv[3] +" -t " + media_duration + " -codec:v libx264 "+ ' -filter_complex "crop=' + crop_value +',scale=-1:640,overlay=x=10:y=10" ' +" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -an -y"
	useFFmpegClass()


# ] YouTube [

# ffmpeg -i input.avi -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p output.mkv

# ./ffmpegHelper.py -y1 v.mov 0:34 0:39 out2.mov

if ( sys.argv[1] == "-y1"):
	print ("*** YouTube and Other Video Sharing Sites Audio Removed ***")
	ffmpeg_command = "-i cornerFinal.png -ss " + sys.argv[3] +" -to " + media_duration + ' -filter_complex "overlay=x=0:y=0" ' + " -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -an -movflags +faststart -y"
	useFFmpegClass()

# ] Audio Intact [

# ./ffmpegHelper.py -y2 v.mov 0:34 0:39 out2.mov

if ( sys.argv[1] == "-y2"):
	print ("*** YouTube and Other Video Sharing Sites ***")
	ffmpeg_command = "-i cornerFinal.png -ss " + sys.argv[3] +" -to " + media_duration + ' -filter_complex "overlay=x=0:y=0" ' + " -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -movflags +faststart -y"
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

	ffmpeg_command = '-filter_complex "drawtext=fontfile=%s:text=%s:fontcolor=0xFFFFFFFF:fontsize=36:x=20:y=10: #shadowcolor=0x000000EE:shadowx=2:shadowy=2" -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -y' % ( media_duration, sys.argv[3] )

	useFFmpegClass()

# Previewing A File
# ffplay -i acrobaticyoga_Sara_R_2.mp4 -vf "crop=640:640:320:60" -ss 00:00:00.0 -t 00:01:03.0 
# ./ffmpegHelper.py -p v.mov 0:34 0:39 720:720:300:0 


if ( sys.argv[1] == "-p"):
	print ("*** Preview Video ***")
	subprocess.call( 'ffplay -i %s -vf "crop=%s" -ss %s -t %s -loop 0' % ( video_file, sys.argv[5], sys.argv[3], media_duration ) , shell=True )


# ] Concat Videos Remove Audio [

# ffmpeg -f concat -i l.txt -i brandVideos.png -codec:v libx264 -filter_complex "crop=720:720:250:0,scale=-1:640,overlay=x=10:y=10" -profile:v baseline -preset slow -pix_fmt yuv420p -b:v 3500k -threads 0 -an -y s1.mp4

if ( sys.argv[1] == "-c1"):
	print ("*** Concat Videos Remove Audio ***")
	subprocess.call( 'ffmpeg -f concat -i l.txt -i brandVideos.png -filter_complex overlay=x=10:y=10 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -y ' + out_file , shell=True )

	# Run a preview of the video
	subprocess.call( 'mplayer %s'  % ( out_file ) , shell=True )


if ( sys.argv[1] == "-c2"):
	print ("*** Concat Videos Youtube Branding Remove Audio ***")
	subprocess.call( 'ffmpeg -f concat -i l.txt -i cornerFinal.png -filter_complex overlay=x=0:y=0 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -an -y ' + out_file , shell=True )

	# Run a preview of the video
	subprocess.call( 'mplayer %s'  % ( out_file ) , shell=True )


#] Combine Video and Audio [
#ffmpeg -i v2.mkv -i a.mp3 -acodec copy -vcodec copy -map 0:v -map 1:a Output.mkv

if ( sys.argv[1] == "-c3"):
	print ("*** Combine Video and Audio ***")
	ffmpeg_command = '-i %s -acodec copy -vcodec copy -map 0:v -map 1:a -y' % ( sys.argv[3] )

	useFFmpegClass()

# ] Slow Motion [
# ffmpeg -i s1.MOV -c copy -filter:v "setpts=2.5*PTS" -y s1s.MOV

if ( sys.argv[1] == "-e1"):
	print ("*** Slow Motion ***")
	ffmpeg_command = '-ss %s -to %s -c:v libx264 -preset slow -filter_complex "setpts=%s*PTS" -crf 0 -preset ultrafast -c:a libmp3lame -b:a 320k -y' % ( sys.argv[3], media_duration, sys.argv[5]  )
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
	ffmpeg_command = '-vframes 1 -ss %s ' % ( sys.argv[3] )
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

# ffmpeg -loop 1 -i Lovelight.png -i a.mp3 -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -movflags +faststart -y -shortest out.mp4
if ( sys.argv[1] == "-e12"):
	print ("*** Combine Audio With Image ***")
	#run('ffmpeg -loop 1 -i %s -i %s -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -movflags +faststart -y -shortest %s' % ( video_file, sys.argv[3], out_file ), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	subprocess.call( 'ffmpeg -loop 1 -i %s -i %s -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -movflags +faststart -y -shortest %s' % ( video_file, sys.argv[3], out_file ) , shell=True )

if ( sys.argv[1] == "-a1"):
	print ("*** Audio Volume ***")
	ffmpeg_command = '-af "volume=%s" -y' % ( sys.argv[3] )
	useFFmpegClass()

#[ Add caption to a photo ]

if ( sys.argv[1] == "-p1"):
	print ("*** Add Caption To A Photo ***")
	subprocess.call( "convert %s -fill white -stroke none -font %s  -pointsize 30 -gravity NorthWest -annotate 0 '%s' %s" % ( video_file, sys.argv[3], sys.argv[4], out_file ) , shell=True )

if ( sys.argv[1] == "-p2"):
	print ("*** Resize Image ***")
	subprocess.call( "convert %s -resize %s %s" % ( video_file, sys.argv[3], out_file ) , shell=True )

# file 'c1.mov'
#for x in range (0, 50):
#	print ("file 'c" + str (x)+"'.mov")



