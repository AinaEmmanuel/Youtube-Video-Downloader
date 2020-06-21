#Modules
import time
from pytube import YouTube, Stream
from pytube.exceptions import RegexMatchError
import sys, time, threading
import os

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

def invalid_try_or_quit():
    """
    Prompts User to Try again or Quit once the URL is invalid
    
    """
    print('\aLink invalid...')
    try_ = input("- Do you want to try again? (y /n): ")
    if try_ == 'y':
        initialize()
    else:
        quit()

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
    # time.sleep(2)
    resolution_and_size()

def resolution_and_size():
    """
    This function gets a list of Resolutions available for Downloads.
    It also takes a user input for their preffered Download Resolution
    
    Update: User can now get the size of the different resolutions 
    """
    global vid
    global resolution_
    global size_
    global res

    resolution_ = []
    size_ = []
    
    #Get the available Resolutions
    for value in vid.streams.filter(progressive=True):
        resolution_.append(value.resolution)
    
    #Gets their respective size
    for size in vid.streams.filter(progressive=True):
        size_ .append(size.filesize)
    
    print(f'\t\t==> Available Resolution <==')
    x = 0
    print('- Select download resolution: ')
    for r,s in zip(resolution_,size_):
        print(f"{x}. {r} - {round((s/1024000), 2)}mb")
        x+=1
    res = input()
    
    download_path()

def download_path():
    global path
    path = input("Enter download path: (press 'enter' to Download file to your current working directory) >> ")
    if path == '':
        print(f"...Downloading to current directory {os.getcwd()}...")
    else:
        print(f"...Downloading {path}...")
    download_video()
    load_animation_download()

def download_video():
    """
    This Function downloads the Video
    
    """
    global vid
    global path_
    chosen_video = vid.streams.filter(file_extension = 'mp4', resolution = resolution_[int(res)])
    chosen_video[0].download(filename = (f"{vid.author}-{vid.title}"), output_path = path)

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
        invalid_try_or_quit()
    else:
        valid_link()
initialize()