from time import sleep
from requests import get
from os import system, remove
from selenium import webdriver
from moviepy.editor import VideoFileClip
from selenium.webdriver.common.by import By
from os.path import join, expanduser, isfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# pip install --upgrade webdriver-manager ???
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import ChromeType
# from selenium.webdriver.chrome.service import Service as ChromiumService

# Get this from Chrome DevTools for https://tikcdn.io/ssstik/...
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'priority': 'u=0, i',
  'sec-ch-ua': '"Not?A_Brand";v="99", "Chromium";v="130"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

# Get this from chrome://version/ Command Line
options = Options()
options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-data-dir=/home/pi/.config/chromium')
options.add_argument('--profile-directory=Default')
options.add_argument('--force-renderer-accessibility')
options.add_argument('--enable-remote-extensions')
options.add_argument('--disable-pings')
options.add_argument('--enable-gpu-rasterization')
options.add_argument('--show-component-extension-options')
options.add_argument('--no-default-browser-check')
options.add_argument('--media-router=0')
options.add_argument('--enable-remote-extensions')
options.add_argument('--load-extension')
options.add_argument('--use-angle=gles')
options.add_argument('--flag-switches-begin')
options.add_argument('--flag-switches-end')
options.add_argument('--ozone-platform=x11')

def SetVideoFile(driver):
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME,'source')))
    sleep(3)
    if VideoFile.split('/')[-1][1:].replace('.mp4','') == driver.find_element(By.TAG_NAME,'video').find_element(By.XPATH, './..').get_attribute('id').split('-')[-1]:
        raise Exception('Duplicate')
    # Return file full name 
    return join(expanduser('~'), 'Downloads', '_' + driver.find_element(By.TAG_NAME,'video').find_element(By.XPATH, './..').get_attribute('id').split('-')[-1]).replace('playback_refactor','') + '.mp4'

def NextVideo(driver):
    body = driver.find_element(By.TAG_NAME,'body')
    body.send_keys(Keys.ESCAPE)
    body.click()
    body.send_keys(Keys.PAGE_DOWN)
    
while True:
    try:
        VideoFile = ''
        MaxFileSize = 8000000
        system('pkill chromium')
        with webdriver.Chrome(service=webdriver.ChromeService(executable_path='/usr/bin/chromedriver'),options=options) as driver:
            driver.get('https://www.tiktok.com/foryou/')
            VideoFile = SetVideoFile(driver)
            while True:
                # Make sure you don't have the video already
                while isfile(VideoFile) or isfile(VideoFile.replace('/_','/')):
                    print(isfile(VideoFile), isfile(VideoFile.replace('/_','/')), VideoFile)
                    NextVideo(driver)
                    VideoFile = SetVideoFile(driver)
                r = get('https://tikcdn.io/ssstik/' + VideoFile.split('/')[-1][1:].replace('.mp4',''), headers=headers)
                # Make sure video can be downloaded and it is not too big
                if r.status_code == 200 and int(r.headers['Content-Length']) < MaxFileSize:
                    with open(VideoFile, 'wb') as f:
                        f.write(r.content)
                    print('Downloaded', VideoFile)
                    # Rotate video from landscape to portrait for our display in a new file
                    VideoFileClip(VideoFile).rotate(90).write_videofile(VideoFile.replace('/_','/'))
                    # Delete old file
                    remove(VideoFile)
                else:
                    print(r.status_code, r.url)
                NextVideo(driver)
                VideoFile = SetVideoFile(driver)
    except Exception as e:
        print(e)

# def RotateVideo(f):
#     cap = VideoCapture(f)
#     fourcc = VideoWriter_fourcc(*'mp4v')
#     fps = cap.get(CAP_PROP_FPS)
#     height = int(cap.get(CAP_PROP_FRAME_HEIGHT))
#     width = int(cap.get(CAP_PROP_FRAME_WIDTH))
#     out = VideoWriter(f+'.mp4', fourcc, fps, (height, width)) 
# 
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         out.write(rotate(frame, ROTATE_90_CLOCKWISE))
# 
#     cap.release()
#     out.release()
# #     sleep(1)
#     remove(f)
#     rename(f+'.mp4',f)

#                     system('ffmpeg -i ' + VideoFile + ' -vf transpose=2 ' + VideoFile + '.mp4')
#                     remove(VideoFile)
#                     rename(VideoFile + '.mp4',VideoFile)
#                     RotateVideo(VideoFile)
#                     VideoFileClip(VideoFile).rotate(90).write_videofile(VideoFile + '.mp4')
                    #remove(f)
                    #rename(f+'.mp4',f)