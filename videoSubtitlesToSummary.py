# Imports
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound
import time
import imutils
from imutils.video import FileVideoStream,FPS
import transformers
from transformers import pipeline
# to speech conversion
from gtts import gTTS
from moviepy.editor import *
# This module is imported so that we can 
# play the converted audio
import os
import speech_recognition as sr

# Connects pytesseract(wrapper) to the trained tesseract module
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def videoSubtitlesToSummery():
    video = cv2.VideoCapture("C:\\Users\\liat\\ocr_realtime\\subtitles_trim.mp4")
    fvs = FileVideoStream("C:\\Users\\liat\\ocr_realtime\\subtitles_trim.mp4").start()
    file_fps = fvs.stream.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), file_fps, (1280,720))
    print(file_fps)
    # start the FPS timer
    fps = FPS().start()
    # Setting width and height for video feed
    video.set(3, 140)
    video.set(4, 180)

    textForFile = ""
    counterFPS = 0
    # Allows continuous frames
    while fvs.more():
        frames = fvs.read()
        if frames is not None:
            frames = imutils.resize(frames, width=1100)
            #cropped_frames = frames[500:730,100:1000]
            counterFPS = counterFPS +1
            if counterFPS == 100:
                counterFPS = 0

                # Capture each frame from the video feed
                data4 = pytesseract.image_to_data(frames)
                oldA = ""
                for z, a in enumerate(data4.splitlines()):
                        
                        a = a.split()
                        if len(a) == 12:
                            r = a[11].replace("===", "\n " ) 
                            r = r.replace("=", ' ' )
                            r = r.replace("text", ' ' )
                            r = r.replace("\\", '' )
                            r = r.replace("-", ' ' )
                            r = r.replace("—", ' ' )                       
                            r = r.replace("‘", ' ' )
                            r = r.replace("?", '' )
                            """r = r.replace("»", ' ' )
                            r = r.replace("~", ' ' )
                            r = r.replace(">", ' ' )
                            r = r.replace("¥", ' ' )
                            r = r.replace("©", ' ' )
                            r = r.replace("*", ' ' )"""

                            textForFile+=r.replace('_', ' ' )+" "
                            print(textForFile)
                            if(a[11] != 'text'):
                                x, y = int(a[6]), int(a[7])
                                w, h = int(a[8]), int(a[9])
                                # Display bounding box of each word
                                cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 0, 255), 2)
                                # Display detected word under each bounding box
                                cv2.putText(frames, r, (x, y ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                        # Output the bounding box with the image
                        cv2.imshow('Video output', frames)
                        out.write(frames)
                        cv2.waitKey(1)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            video.release()
                            cv2.destroyAllWindows()
                            out.release()
                            break

    
    with open("C:\\Users\\liat\\ocr_realtime\\textFromVideo.txt", "w", encoding="utf-8") as f:
        f.write(textForFile)
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    print(summarizer(textForFile))
    summery = summarizer(textForFile)[0]['summary_text']
    with open("C:\\Users\\liat\\ocr_realtime\\summarizeTextFromVideo.txt", "w", encoding="utf-8") as f:
        f.write(summery)
    video.release()
    cv2.destroyAllWindows()
    out.release()
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=summery, lang='en', slow=False)
    
    # Saving the converted audio in a mp3 file named
    myobj.save("summarizeTextFromVideoAudio.mp3")


videoSubtitlesToSummery()