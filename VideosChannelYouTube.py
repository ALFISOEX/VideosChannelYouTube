import requests
import os
from pytube import Channel

name_channel = input('URL Channel: ')

try:
    channel = Channel(name_channel)
    videos = channel.videos
    video_count = len(videos)

    if video_count > 0:
        print(f'Begin download video from channel: {channel.channel_name}.\nCount videos: {video_count}')
        path = channel.channel_name + '/'
        name_file = 1

        if os.path.exists(path):
            listdir = os.listdir(path)
            name_files = []
            for file in listdir:
                name_files.append(os.path.splitext(file)[0])
            if len(name_files) > 0:
                name_files.sort()
                name_file = int(name_files[len(name_files)-1]) + 1

        for video in videos:
            while (True):
                try: 
                    res = ''
                    if len(video.streams.filter(res='1080p')) > 0:
                        res = '1080p'
                    elif len(video.streams.filter(res='720p')) > 0:
                        res = '720p'
                    if res != '':
                        if len(video.streams.filter(res=res,progressive=True)) > 0:
                            progressive = True
                        else: progressive = False
                        video.streams.filter(file_extension='mp4', res=res, progressive=progressive).first().download(path, str(name_file) + '.mp4')
                    else:
                        video.streams.filter(file_extension='mp4').first().download(path, str(name_file) + '.mp4')
                    break
                except:
                    print(f'[{video.video_id}] Error download video. Restart download.')

            print(f'[{video.video_id}] Video saved to {path}{name_file}.mp4')
            thumbnail_url = f'https://i.ytimg.com/vi/{video.video_id}/maxresdefault.jpg'
            req = requests.get(thumbnail_url)
            with open(path + str(name_file) + '.jpg', 'wb') as preview:
                preview.write(req.content)

            if os.path.getsize(path + str(name_file) + '.jpg') < 2000:
                thumbnail_url = f'https://img.youtube.com/vi/{video.video_id}/hqdefault.jpg'
                req = requests.get(thumbnail_url)
                with open(path + str(name_file) + '.jpg', 'wb') as preview:
                    preview.write(req.content)
            print(f'[{video.video_id}] Preview saved to {path}{name_file}.jpg')
            name_file += 1
    else: print("Videos not found.")
except:
    print('Error link.')
