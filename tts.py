import pydub,os,PIL,ffmpeg,shutil,time,textwrap
from pathlib import Path
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
from moviepy.editor import *
import snatch
try:
    shutil.rmtree("out")
except:
    pass
os.mkdir("out")
def insert_newlines(string, every=100):
    #https://stackoverflow.com/questions/2657693/insert-a-newline-character-every-64-characters-using-python
    return textwrap.fill(string, width=every)
def tts(speak, n, post):
    tts = gTTS(speak, lang="en", tld="co.uk")
    tts.save(f'out/{n}.mp3')
    image = Image.new("RGB", (1920, 1080), "black")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("casual.ttf", size=42)
    text = insert_newlines(f"u/{post['User']}\n{post['Content']}").replace(f"u/{post['User']} ", f"u/{post['User']}\n")
    print(text)
    draw.text((10, 25), text, font=font)
    image.save(f'out/{n}.jpg')
posts = snatch.getRedditPosts('askreddit')
print(posts)
n=0
tts(posts[0] + ".; ", n, {'User': "", 'Content': posts[0]})
for i in posts[1:]:
    n+=1
    tts("u/slash/{}; {}.".format(i["User"], i["Content"]), n, i)
    print("Generated:" + str(n))
audios = []
n=0
#old PyDub based code
'''for file in os.listdir("out"): 
    print(file)
    if not file == "0.mp3" and file.endswith(".mp3"):
        audios += [AudioSegment.from_mp3("out/" + file), AudioSegment.from_mp3("beep.mp3")]
out = AudioSegment.from_mp3("out/0.mp3") + AudioSegment.from_mp3("beep.mp3")
for i in audios[:-1]:
    out = out + i
out.export("out.mp3", format="mp3")
'''
files = []
#n=0
pic = ffmpeg.input("beep.jpg")
vid = ffmpeg.input("beep.mp3")
#print(n, file)
(
    ffmpeg
    .concat(pic, vid, v=1, a=1)
    .output(f"beep.mp4")
    .run(overwrite_output=True)
)
for file in os.listdir("out"): 
    if file.endswith(".mp3"):
        n = file.replace(".mp3", "")
        pic = ffmpeg.input(f"out/{n}.jpg")
        vid = ffmpeg.input(f"out/{file}")
        #print(n, file)
        (
            ffmpeg
            .concat(pic, vid, v=1, a=1)
            .output(f"out/{n}-fixed.mp4")
            .run(overwrite_output=True)
        )
        files.append(f"out/{n}-fixed.mp4")
        #n+=1
files = sorted(files)
newfiles = []
for i in files:
    newfiles.append(VideoFileClip(i))
    newfiles.append(VideoFileClip("beep.mp4"))
files = newfiles
video = concatenate_videoclips(files)
video.write_videofile("out.mp4")
