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
    loading_animation()

def load_link():
    """
    Reads and loads in the URL
    
    """
    global target
    target = load_link
    global vid
    vid = YouTube(url)

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
    - Length:
    
    """
    print("\t\t==> Video Details <==")
    print(f"- Channel: {vid.author}")
    print(f"- Title: {vid.title}")
    # print(f"- Description: {vid.description}")
    length = vid.length
    if length < 60:
        print(f"- Video Length: {length}s")
    else:
        print(f'- Video Length: {length/60}m')
    # time.sleep(2)
    audio_or_video()

def audio_or_video():
    """
    Prompts user to choose their preferred file type for download (video/audio).

    """
    print("\t\t==> File Type <==")
    global a_or_v
    a_or_v = input(
'''What file type would you like to download: 
0. mp4 
1. mp3
>''')
    if a_or_v == '0':
        resolution_and_size()
    elif a_or_v == '1':
        download_path()
    else:
        audio_or_video()

def resolution_and_size():
    """
    This function gets a list of Resolutions available for Downloads.
    It also takes a user input for their preferred Download Resolution
    
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
    res = input('>')
    if int(res) not in range(0,len(resolution_)):
            resolution_and_size()
    
    download_path()

def download_path():
    """ 
    Prompts user to specify the download path or downloads to the current directory by default

    Path must be in form 'C:\\Users\\Emmanuel\\Desktop\\v1.1'

    Specifying your download path is the most preferrable option
    
    """
    global path
    path = input("Enter download path: (press 'enter' to Download file to your current working directory) >> ")
    if path == '':
        print(f"...Downloading to current directory {os.getcwd()}...")
    else:
        print(f"...Downloading to {path}...")

    if a_or_v == '0':
        download_video()
        loading_animation()
    elif a_or_v == '1':
        download_audio()
        loading_animation()

def download_video():
    """
    This Function downloads the file in mp4 format
    
    """
    target = download_video

    chosen_video = vid.streams.filter(file_extension = 'mp4', resolution = resolution_[int(res)])
    chosen_video[0].download(filename = (f"{vid.author}-{vid.title}"), output_path = path)

def download_audio():
    """
    This Function downloads the the file in mp3 format

    """
    target = download_audio

    audio_ = vid.streams.filter(only_audio=True)
    audio_file = audio_[0].download(filename = (f"{vid.author}-{vid.title}"), output_path = path)
    

    """ 
    By default, pytube saves the download file with the '.mp4' extension even if it's an audio file;
    so, i have to convert the downloaded file from '.mp4' to '.mp3' manually

    """
    if a_or_v == "1":
        base, ext = os.path.splitext(audio_file)
        new_file = base + '.mp3'
        os.rename(audio_file, new_file)

def loading_animation():
    """
    Loading animation when there is any delaying process
    
    """
    the_process = threading.Thread(name='process', target=target)
    the_process.start()
    while the_process.is_alive():
        animated_loading()
    print('\nDone!')

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

#Quit
input('\nPress enter to exit > ')