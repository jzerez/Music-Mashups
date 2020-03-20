from pytube import *
import sys

link = sys.argv[1]
yt = YouTube(link).streams.filter(only_audio=True)

yt[0].download()
