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
