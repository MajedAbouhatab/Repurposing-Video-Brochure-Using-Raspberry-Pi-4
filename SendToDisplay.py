from time import sleep
from os import system, listdir, popen
from moviepy.editor import VideoFileClip
from os.path import join, expanduser, isfile, getsize

while True:
    try:
        TotalSize = 0
        CopyList=[]
        MasterList = [[ff, getsize(ff), VideoFileClip(ff).duration] for ff in [join(expanduser('~'), 'Downloads', f) for f in sorted(listdir(join(expanduser('~'), 'Downloads'))) if f.endswith('.mp4') and not f.startswith('_') and not isfile(join(expanduser('~'), 'Downloads', '_' + f))]]
        print('MasterList', MasterList)
        
        def SaveCopyList():
            print('CopyList', CopyList)
            system('sudo uhubctl -l 1-1 -a 2 > /dev/null 2>&1')
            while len(popen('lsblk -r | grep sda').read().strip().split(' ')) < 7:
                sleep(1)
            USBDrive = popen('lsblk -r | grep sda').read().strip().split(' ')[-1] + '/video/'
            print(USBDrive)
            system(f'rm {USBDrive}*')
            for c in CopyList: 
                system(f'cp {c[0]} {USBDrive}')
            system('sudo uhubctl -l 1-1 -p 3 -a 0 > /dev/null 2>&1')
            print(sum([c[2] for c in CopyList]), 'seconds')
            sleep(sum([c[2] for c in CopyList]))
            
        for i, l in enumerate(MasterList):
            if TotalSize + l[1] < 80000000:
                TotalSize += l[1]
                CopyList.append(l)
                if i == len(MasterList) - 1:
                    SaveCopyList()
            else:
                SaveCopyList()
                TotalSize = l[1]
                CopyList = [l]
                
    except Exception as e:
        print(e)
        
        

        #system('lsblk -r | grep sda'):
#popen('lsblk -r | grep sda').read().strip().split(' ')[-1] #'/media/pi/2A4B-2567' #popen('lsblk | grep sda').read().strip().split(' ')[-1]
        
        
# popen('lsblk -r | grep sda').read().strip().split(' ')[-1] == '':
        
        
        
        
        
        
        
        # import cv2
# import ffmpeg
        
#     CurrentVideoNumber = l[0]
# #     print(CurrentVideoNumber)
#     if TotalSize > 100000000:
#         print(CopyList)
#         TotalSize = 0
#         CopyList = [l]
#         print(TotalSize)
#         print(CopyList) 
#         if l[0] > 15:
#             break
#         
#     else:
#         TotalSize += l[2]
#         CopyList.append(l)
#     
#     print(l, TotalSize)
    
    
# print(L)
    
# for f in listdir(join(expanduser('~'), 'Downloads')):
#     if VideoFileClip(join(expanduser('~'), 'Downloads', f)).duration > 10:
#         continue
#     system('sudo uhubctl -l 1-1 -a 2')
#     while system('ls /media/pi/2A4B-2567/video/'):
#         sleep(1)
#     system('rm /media/pi/2A4B-2567/video/*')
#     system('cp ' + join(expanduser('~'), 'Downloads', f) + ' /media/pi/2A4B-2567/video/')
#     system('sudo uhubctl -l 1-1 -p 3 -a 0')
#     sleep(VideoFileClip('/home/pi/Downloads/' + f).duration)
#     break

#     print(ffmpeg.probe('/home/pi/Downloads/' + f)['format']['duration'] + 1)
    
#     print(VideoFileClip('/home/pi/Downloads/' + f).duration)    
#     print(cv2.VideoCapture('/home/pi/Downloads/' + f).get(cv2.CAP_PROP_POS_MSEC))

# L = [[f, getsize(join(expanduser('~'), 'Downloads', f)), 0, 0] for f in listdir(join(expanduser('~'), 'Downloads'))]
# 
# print(L)


# print(l)
    

# exit()
# 
# while True:
#     try:
#         for VideoFile in listdir(join(expanduser('~'), 'Downloads')):
#             if VideoFile[0] == '_':
#                 VideoFileClip(join(expanduser('~'), 'Downloads', VideoFile)).rotate(90).write_videofile(join(expanduser('~'), 'Downloads', VideoFile[1:]))
#                 remove(join(expanduser('~'), 'Downloads', VideoFile))
#     except Exception as e:
#         print(e)