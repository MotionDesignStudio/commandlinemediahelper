#!/usr/bin/env python

import sys
import cv2
import subprocess
from subprocess import call


import aalib
import Image

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import imghdr

import ImageOps

import numpy as np


sys.dont_write_bytecode = True
videofilename=str(sys.argv[1]).strip()

#These two variables control the resolution and font size.  They are interconnected.
#img_new_magnitude
#fontsize

try:
	img_new_magnitude= int (str(sys.argv[2]).strip() )
except :
	img_new_magnitude=4

try:
	fontsize= int (str(sys.argv[3]).strip())
except :
	fontsize= 15

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", fontsize, encoding="unic")

def create_ascii_video_2():
	#Extract the image size:
	image_width, image_height =calculate_image_size_from_video ()
	#Extract the number of rows and length of the string in pixels which is used for the image being 
	#created based on the width and height of the text.
	how_many_rows, new_img_width = calculate_image_size_from_video_2 ()

	vc = cv2.VideoCapture(videofilename)
	saved_file_name=""
	frame_rate=str (vc.get(cv2.cv.CV_CAP_PROP_FPS))

	#Png file name counter
	c=0

	if vc.isOpened():
    		rval , frame = vc.read()
	else:
    		rval = False

	while rval:
    		rval, frame = vc.read()
		
		#Check to see if file is a valid image.  I notice the last frame of the video is an empty file at times:
    		try:
			myimage= Image.fromarray(frame)
		except (TypeError, AttributeError):
            		print ("cannot identify image while loop in function create_ascii_video_2", myimage)
			continue		

	
		aalib_screen_width= int(image_width/25.28)*img_new_magnitude
		aalib_screen_height= int(image_height/41.39)*img_new_magnitude		

		screen = aalib.AsciiScreen(width=aalib_screen_width, height=aalib_screen_height )

		myimage= Image.fromarray(frame).convert("L").resize(screen.virtual_size)
		
		screen.put_image((0,0), myimage)

		img=Image.new("RGBA", (new_img_width, how_many_rows*fontsize),(120,20,20))
		draw = ImageDraw.Draw(img)
		y = 0
		for lines in screen.render().splitlines():
			draw.text( (0,y), lines, (255,255,0),font=font )
			y = y + fontsize
	

		imagefit = ImageOps.fit(img, (image_width, image_height), Image.ANTIALIAS)
		
		imagefit.save(str(c)+'.png', "PNG")

    		c = c + 1
    		cv2.waitKey(1)
		
	vc.release()
	cv2.destroyAllWindows()

	subprocess.call(["ffmpeg", "-r",  frame_rate, "-i", "%d.png",  "-y", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-c:a", "copy", "-pix_fmt", "yuv420p", "output.mkv" ])
	
	clean_up(c)


def create_ascii_image():

	myimage= Image.open(videofilename)
	image_width, image_height = myimage.size

	
	aalib_screen_width= int(image_width/24.9)*img_new_magnitude
	aalib_screen_height= int(image_height/41.39)*img_new_magnitude

	screen = aalib.AsciiScreen(width=aalib_screen_width, height=aalib_screen_height )

	myimage= Image.open(videofilename).convert("L").resize(screen.virtual_size)
	screen.put_image((0,0), myimage)
	
	y = 0

	how_many_rows = len ( screen.render().splitlines() ) 

	new_img_width, font_size = font.getsize (screen.render().splitlines()[0])
	

	img=Image.new("RGBA", (new_img_width, how_many_rows*fontsize),(120,20,20))
	draw = ImageDraw.Draw(img)

	for lines in screen.render().splitlines():
		draw.text( (0,y), lines, (255,255,0),font=font )
		y = y + fontsize
		

	imagefit = ImageOps.fit(img, (image_width, image_height), Image.ANTIALIAS)
	
	imagefit.save("ascii_photo.png", "PNG")


def clean_up(howmuchtodelete):
	i=0
	while i< howmuchtodelete :
		subprocess.call(["rm", str(i)+".png" ])
		i=i+1

def complete_alert_message(the_message):
	font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",40)
	img=Image.new("RGBA", (200,70),(120,20,20))
	draw = ImageDraw.Draw(img)
	draw.text((5, 0),the_message,(255,255,0),font=font)
	img.show()



def calculate_image_size_from_video ():

	vc = cv2.VideoCapture(videofilename)

	if vc.isOpened():
    		rval , frame = vc.read()

		#Extract the image size:
    		try:
			myimage= Image.fromarray(frame)
			return myimage.size			
        	except IOError:
            		print ("cannot identify image file", myimage)
		

	else:
    		print ("In fucntion calculate_image_size_from_video I could not find the video frame size." )


def calculate_image_size_from_video_2 ():
	#Extract the image size:
	image_width, image_height =calculate_image_size_from_video ()

	vc = cv2.VideoCapture(videofilename)

	if vc.isOpened():
    		rval , frame = vc.read()
	else:
    		rval = False

	while rval:
    		rval, frame = vc.read()
		
		#Check to see if file is a valid image.  I notice the last frame of the video is an empty file at times:
    		try:
			myimage= Image.fromarray(frame)
		except (TypeError, AttributeError):
            		print ("cannot identify image", myimage)
			continue		

	
		aalib_screen_width= int(image_width/25.28)*img_new_magnitude
		aalib_screen_height= int(image_height/41.39)*img_new_magnitude
		

		screen = aalib.AsciiScreen(width=aalib_screen_width, height=aalib_screen_height )

		myimage= Image.fromarray(frame).convert("L").resize(screen.virtual_size)
		
		screen.put_image((0,0), myimage)	

		how_many_rows = len ( screen.render().splitlines() ) 

		new_img_width, font_size = font.getsize (screen.render().splitlines()[0])
	
    		cv2.waitKey(1)	
		vc.release()
		return  (how_many_rows, new_img_width )
		

def test_if_image_or_video ():

	if imghdr.what(videofilename) != None :
		print ("This is a image file.")
		create_ascii_image()
	else: 
		print ("This is probably not a image.")
		create_ascii_video_2()


test_if_image_or_video ()









