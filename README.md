# commandlinemediahelper
A Python project to edit video, photo and audio using various system calls mostly to FFmpeg.

] HELP [

                    Examples : Videos | Audio | Photos

     Slicing Videos To Time :  ./ffmpegHelper.py -s1 v.mov 0:34 0:39 out.mov
    Slicing Videos To Range :  ./ffmpegHelper.py -s2 v.mov 0:34 0:39 out.mov
    Instagram Without Resize :  ./ffmpegHelper.py -i1 v.mov 0:34 0:39 720:720:300:0 out.mp4
      Instagram With Resize :  ./ffmpegHelper.py -i2 v.mov 0:34 0:39 720:720:300:0 out.mp4
      Almost Lossless With Resize :  ./ffmpegHelper.py -i3 v.mov 0:34 0:39 720:720:300:0 out.mp4
      YouTube Audio Removed :  ./ffmpegHelper.py -y1 v.mov 0:34 0:39 out.mp4
                    YouTube :  ./ffmpegHelper.py -y2 v.mov 0:34 0:39 out.mp4
              Concat Videos :  ./ffmpegHelper.py -c1 out.mp4
              Concat Videos Youtube BRND :  ./ffmpegHelper.py -c2 out.mp4
    Combine Video and Audio :  ./ffmpegHelper.py -c3 v.mov out.mp3 out.mkv
    Overlay Text/Image 2 Video :  ./ffmpegHelper.py -t1 out.mov "Overlayed Text" /pathto/font.ttf out.mp4
      Overlay Text To Video :  ./ffmpegHelper.py -t2 text.mov "Overlayed Text" /pathto/font.ttf out.mp4
              Preview Video :  ./ffmpegHelper.py -p v.mov 0:34 0:39 720:720:300:0
                Slow Motion :  ./ffmpegHelper.py -e1 v.mov 4 out.mp4
       Slow Motion No Audio :  ./ffmpegHelper.py -e2 v.mov 0:34 0:39 2.5 out.mp4
            Black And White :  ./ffmpegHelper.py -e3 v.mov 0:34 0:39 out.mp4
            Black And White No Audio :  ./ffmpegHelper.py -e4 v.mov 0:34 0:39 out.mp4
       Extract Single Frame :  ./ffmpegHelper.py -e5 v.mov 0:34 image.png
          Scale Ratio Width :  ./ffmpegHelper.py -e6 v.mov 0:34 0:39 out.mp4
          Scale Ratio Width No Audio :  ./ffmpegHelper.py -e7 v.mov 0:34 0:39 out.mp4
         Scale Ratio Height :  ./ffmpegHelper.py -e8 v.mov 0:34 0:39 416 out.mp4
         Scale Ratio Height No Audio :  ./ffmpegHelper.py -e9 v.mov 0:34 0:39 416 out.mp4
           Resize Arbitrary :  ./ffmpegHelper.py -e10 v.mov 0:34 0:39 416 416 out.mp4
           Resize Arbitrary No Audio :  ./ffmpegHelper.py -e11 v.mov 0:34 0:39 416 416 out.mp4
           Combine Audio With Image :  ./ffmpegHelper.py -e12 i.png a.mp3 out.mp4
      Turn Image Into Video :  ./ffmpegHelper.py -e13 i.png 5 out.mp4
               Audio Volume :  ./ffmpegHelper.py -a1 a.mp3 2 b.mp3
         Caption To A Photo :  ./ffmpegHelper.py -p1 i.png /pathto/font.ttf "Hello World" out.png
      Caption From temp.txt :  ./ffmpegHelper.py -p2 #123456 "#344567" /home/lex/share/Mo_De_Studio/audio_blog/Bookerly/Bookerly-Bold.ttf "1280x720" "#123456" 10 out.png
             Resize A Photo :  ./ffmpegHelper.py -p3 i.png 150X700! out.png
                       Hint :  Use 0 to choose media length example : ./ffmpegHelper.py -p v.mov 0:34 0 720:720:300:0
                       Hint :  To use c1 and c2 the filenames must be sequenced like this you can mix and match suffixes c1.xxx, c2.xxx ... c400.xxx 
                       Help :  ./ffmpegHelper.py -h

] Install These [

apt-get install ffmpeg imagemagick mplayer python3-pip

Install the following helper class for python 3.X.

pip3 install ffmpy

] Connect [

https://motiondesigntechnology.wordpress.com/
https://www.facebook.com/motiondesignstudio/
https://www.instagram.com/motiondesignstudio

#motiondesignstudio
 
