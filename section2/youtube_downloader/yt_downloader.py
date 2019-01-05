# coding: utf-8
# 181215
import argparse
import os
import subprocess
import pytube

cwd = os.getcwd() # 현재 경로

'''
옵션들
--yt_url : 다운로드 받고 싶은 youtube 영상 url
--savePath : 파일을 저장하고 싶은 경로
--filename : 저장할 영상 name
--mp3_filename : 저장할 mp3파일 이름
--only_video : 영상만 다운로드 하고 싶으면 True 입력

조건
1. yt_downloader.py와 같은 경로에 ffmpeg.exe 실행파일이 함께 있어야함
2. 위에 import한 라이브러리들이 깔려 있어야함

ex)
python yt_downloader.py --yt_url www.url.com
python yt_downloader.py --yt_url www.url.com --filename test
'''


parser = argparse.ArgumentParser()
parser.add_argument('--yt_url', dest = 'yt_url', help ='youtube url')
parser.add_argument('--savePath', dest = 'savePath', default = cwd + '/download_file/', help ='save path')
parser.add_argument('--filename', dest = 'filename', help ='write filename')
parser.add_argument('--mp3_filename', dest = 'mp3_filename', help ='write mp3_filename')
parser.add_argument('--only_video', dest = 'only_video',default = False, help ='Only video : True', type = bool)

args = parser.parse_args()


yt = pytube.YouTube(args.yt_url)
videos= yt.streams.all()
default_filename = videos[0].default_filename # 가장 화질이 좋은 첫 번째 파일 선택
ext = os.path.splitext(default_filename)[1] # 확장자명만 가져옴

# 다운로드 받을 경로 설정
savePath = args.savePath # 다운로드 받을 경로
if not os.path.exists(savePath): # 만약 입력한 경로가 없다면 만든 후 저장
    os.makedirs(savePath)

# 해당 url 다운로드
videos[0].download(savePath)

# 만약 영상의 filename 설정
if args.filename: # 만약 추가적으로 다른 이름을 입력했다면
	new_filename = args.filename + ext
	os.rename(savePath + default_filename, savePath + new_filename)
	default_filename = new_filename

# mp3 파일로 변환
if not(args.only_video): # only video만 아닌 mp3 파일도 받고 싶다면

	if args.mp3_filename: # mp3_filename을 따로 설정한다면
		new_mp3_filename = args.mp3_filename + '.mp3'
	else:
		new_mp3_filename = os.path.splitext(default_filename)[0] + '.mp3'

	# cmd창에서 시키는 것과 동일
	subprocess.call(['ffmpeg', '-i',
		os.path.join(savePath, default_filename),
		os.path.join(savePath, new_mp3_filename)
	])
