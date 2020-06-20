#Modules
import time
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import sys, time, threading

print("\t\t==> Youtube Video Downloader <==")

def animated_loading():
    """
    Creates an animation when there is work in progress
    
    """
    chars = "|/-\\"
    for char in chars:
        sys.stdout.write(f'\rLoading...Please Wait! {char}')
        # sys.stdout.write('\r'+'loading...'+char)
        time.sleep(.1)
        sys.stdout.flush()

def enter_link():
    """
    Prompts the user to enter the URL of the video
    
    """
    global url
    url = input("Enter the URL to the video: ")
    load_link()
    load_animation_url()

def load_link():
    """
    Reads and loads in the URL
    
    """
    global vid
    vid = YouTube(url)

def load_animation_url():
    """
    Loading animation When Reading and Loading the URL
    
    """
    the_process = threading.Thread(name='process', target=load_link)
    the_process.start()
    while the_process.is_alive():
        animated_loading()

def valid_link():
    """
    Checks if the URL is valid and proceeds to the next stage
    
    """
    print('\n- URL Okay!...')
    time.sleep(2)
    vid_details()

#Disapproves the link
def invalid_link():
    """
    Checks if the URL is Invalid and exits the app
    
    """
    
    print('Link invalid...Enter a valid link: ')
    exit()

def vid_details():
    """
    Prints out the Video Details in this format:
        __ __ __ __ __ __ __ __ __ __ __ __
    - Channel:
    - Title:
    - Description:
    - Length:
    
    """
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

def resolution():
    """
    This function gets a list of Resolutions available for Downloads.
    It also takes a user input for their preffered Download Resolution
    
    """
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

def download_video():
    """
    This Function downloads the Video
    
    """
    global vid
    chosen_video = vid.streams.filter(file_extension = 'mp4', resolution = resolution_[int(res)])
    chosen_video[0].download()

def load_animation_download():
    """
    Loading animation when download is in progress
    
    """
    the_process = threading.Thread(name='process', target=download_video)
    the_process.start()
    while the_process.is_alive():
        animated_loading()
    print('\n\aDownload Complete!')

def initialize():
    """
    Initialize the Program with an exception to catch invalid URLs
    
    """
    try:
        enter_link()
    except RegexMatchError as e:
        invalid_link()
    else:
        valid_link()

initialize()