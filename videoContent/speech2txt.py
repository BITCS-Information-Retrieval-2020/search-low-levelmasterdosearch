from pydub import AudioSegment
import os
from optparse import OptionParser
from pydub.silence import detect_nonsilent
import itertools
from aip import AipSpeech
import fnmatch
import http.client
import random
import json
import shutil
import hashlib
import urllib
from tqdm import tqdm


class Subtitle(object):
    def __init__(self, path):
        self.path = path
        self.startTime = []
        self.endTime = []
        self.allTextEnglish = ""
        self.videoTextEnglish = []

    # 返回起始时间，结束时间，英文字幕
    def return_subtitle(self):

        # 将视频转化为音频
        video_path = self.path
        audio_path = self.convert2wav(video_path)

        # 切分音频
        sound = AudioSegment.from_file(audio_path, format='wav')
        chunks, starts, ends = self.split_audio(sound, min_silence_len=500, silence_thresh=-30, keep_silence=100)
        os.remove(audio_path)

        # 将切分的音频保存
        (filepath, tempfilename) = os.path.split(audio_path)
        (filename, extension) = os.path.splitext(tempfilename)
        chunks_folder_name = filename + '-chunks'
        chunks_path = filepath + '/' + chunks_folder_name + '/'
        if not os.path.exists(chunks_path):
            os.mkdir(chunks_path)

        num = 0

        # 连接百度AipSpeech
        client = self.connect_client()

        # 对每一段音频获取字幕
        for i in tqdm(range(len(chunks))):
            chunk = chunks[i]
            start = starts[i]
            end = ends[i]
            chunk_name = filename + '-%05d-%d-%d.wav' % (i, start, end)
            chunk_path = chunks_path + chunk_name
            chunk.export(chunk_path, format='wav')
            subtitle = self.get_subtitle(chunk_path, client)
            if subtitle is None:
                continue
            num += 1

            # 转换时间格式
            self.startTime.append(self.time_convert(start))
            self.endTime.append(self.time_convert(end))
            self.videoTextEnglish.append(subtitle)

        # 删除音频分段文件
        shutil.rmtree(chunks_path)

        self.allTextEnglish = " ".join(self.videoTextEnglish)

        return self.startTime, self.endTime, self.videoTextEnglish, self.allTextEnglish

    # 将视频转化为音频
    def convert2wav(self, video_path):
        (folderpath, fullfilename) = os.path.split(video_path)
        (filename, extension) = os.path.splitext(fullfilename)
        audio_name = filename + '-temp.wav'
        audio_path = folderpath + '/' + audio_name

        # 调用ffmpeg
        ffmpegFormatCode = 'ffmpeg -i {0} -f {1} -vn {2} -loglevel quiet'
        os.system(ffmpegFormatCode.format(video_path, 'wav', audio_path))

        wav_v = AudioSegment.from_wav(audio_path)
        mon = wav_v.set_frame_rate(16000).set_channels(1)
        audio_16k = folderpath + '/' + filename + '.wav'
        mon.export(audio_16k, format='wav', codec='pcm_s16le')
        os.remove(audio_path)
        return audio_16k

    # 连接百度AipSpeech客户端
    def connect_client(self):
        # 调用百度API的用户名，密码等
        APP_ID = '23191035'
        API_KEY = 'WAfGnCoaGkm1gog3ZGQ1t4Cn'
        SECRET_KEY = 'HiS3LGvv7yzivzXIRPWlo8hPx3MXM9ue'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        return client

    # 调用百度AipSpeech，获取单句字幕
    def get_subtitle(self, file_name, client):

        with open(file_name, 'rb') as fp:
            content = fp.read()
        return_content = client.asr(content, 'wav', 16000, {'dev_pid': 1737})
        if return_content['err_no'] != 0:
            return
        subtitle = str(return_content['result'])[2:-2]
        return subtitle

    # 转换时间格式为h:m:s:ms格式
    def time_convert(self, time):
        millisecond = time % 1000
        second = (time // 1000) % 60
        minute = ((time // 1000) // 60) % 60
        hour = ((time // 1000) // 60) // 60
        time_string = '%02d:%02d:%02d:%03d' % (hour, minute, second, millisecond)
        return time_string

    # 切分音频
    def split_audio(self, audio_segment, min_silence_len=500, silence_thresh=-30, keep_silence=100, seek_step=1):

        not_silence_ranges = detect_nonsilent(audio_segment, min_silence_len, silence_thresh, seek_step)

        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = itertools.tee(iterable)
            next(b, None)
            return zip(a, b)

        start_min = 0
        chunks = []
        audio_starts = []
        audio_ends = []

        for (start_i, end_i), (start_ii, end_ii) in pairwise(not_silence_ranges):
            end_max = end_i + (start_ii - end_i + 1) // 2
            start_i = max(start_min, start_i - keep_silence)
            end_i = min(end_max, end_i + keep_silence)

            chunks.append(audio_segment[start_i:end_i])
            audio_starts.append(start_i)
            audio_ends.append(end_i)
            start_min = end_max

        start_last = max(start_min, start_ii - keep_silence)
        end_last = min(len(audio_segment), end_ii + keep_silence)
        chunks.append(audio_segment[start_last:end_last])
        audio_starts.append(start_last)
        audio_ends.append(end_last)

        return chunks, audio_starts, audio_ends


if __name__ == '__main__':

    path = os.path.abspath('.') + '/1.mp4'
    S = Subtitle(path)
    startTime, endTime, videoTextEnglish, allTextEnglish = S.return_subtitle()
    print(startTime)
    print(endTime)
    print(videoTextEnglish)
