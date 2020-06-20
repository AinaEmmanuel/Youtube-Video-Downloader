#Modules
import time
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import sys, time, threading

print("\t\t==> Youtube Video Downloader <==")

# Custom Loading-Screen Animation
def animated_loading():
    chars = "|/-\\" 
    for char in chars:
        sys.stdout.write(f'\rLoading...Please Wait! {char}') 
        # sys.stdout.write('\r'+'loading...'+char)
        time.sleep(.1)
        sys.stdout.flush()

#User enters the youtube link
def enter_link():
    global url
    url = input("Enter the URL to the video: ")
    load_link()
    load_animation_url()

#Reading and Loading the Link
def load_link():
    global vid
    vid = YouTube(url)

#Animation for when the link is being processed
def load_animation_url():
    the_process = threading.Thread(name='process', target=load_link)
    the_process.start()
    while the_process.is_alive():
        animated_loading()

#Approves the Link
def valid_link():
    print('\n- URL Okay!...')
    time.sleep(2)
    vid_details()

#Disapproves the link
def invalid_link():
    print('Link invalid...Enter a valid link: ')
    exit()

#Video Details
def vid_details():
    print("\t\t==> Video Details <==")
    print(f"- Channel: {vid.author}")
    print(f"- Title: {vid.title}")
    print(f"- Description: {vid.description}")
    length = vid.length
    if length < 60:
        print(f"- Video Length: {length}s")
    else:
        print(f'- Video Length {length/60}m')
    time.sleep(2)
    resolution()

#User selects their download resolution from the list of available resolutions
def resolution():
    global vid
    global resolution_
    global res
    resolution_ = []
    for value in vid.streams.filter(progressive=True):
        resolution_.append(value.resolution)
    print(f'\t\t==> Available Resolution <==')
    x = 0
    print('- Select download resolution: ')
    for r in resolution_:
        print(f"{x}. {r}")
        x+=1
    res = input()
    download_video()
    load_animation_download()

#Download the video
def download_video():
    global vid
    chosen_video = vid.streams.filter(file_extension = 'mp4', resolution = resolution_[int(res)])
    chosen_video[0].download()

#Animation for when the download is in progress
def load_animation_download():
    the_process = threading.Thread(name='process', target=download_video)
    the_process.start()
    while the_process.is_alive():
        animated_loading()
    print('\n\aDone!')

#Initializing the program
def initialize():
    try:
        enter_link()
    except RegexMatchError as e:
        invalid_link()
    else:
        valid_link()
initialize()