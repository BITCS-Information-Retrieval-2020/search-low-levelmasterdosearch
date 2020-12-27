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
# import hashlib
# import urllib

class Subtitle(object):
    def __init__(self, path):
        self.path = path
        self.startTime = []
        self.endTime = []
        self.videoText = []
    
    def return_subtitle(self):
        if not os.path.exists('res'):
            os.mkdir('res')
        for root, dirs, files in os.walk(path):
            for f in files:
                video_path = os.path.join(root, f)

                audio_path = self.convert2wav(video_path)
                #print(audio_path)

                sound = AudioSegment.from_file(audio_path, format='wav')
                chunks, starts, ends = self.split_audio(sound, min_silence_len=300, silence_thresh=-30, keep_silence=100)
                os.remove(audio_path)

                (filepath, tempfilename) = os.path.split(audio_path)
                (filename, extension) = os.path.splitext(tempfilename)
                chunks_folder_name = filename + '_audio_chunks'
                chunks_path = filepath + '/' + chunks_folder_name + '/'
                if not os.path.exists(chunks_path):
                    os.mkdir(chunks_path)

                srt_name = filename + '.srt'
                srt_path = 'res/' + srt_name
                srt_file = open(srt_path, 'w+')
                num = 0

                client = self.connect_AipSpeech()

                for i in range(len(chunks)):
                    chunk = chunks[i]
                    start = starts[i]
                    end = ends[i]
                    chunk_name = filename + ',%04d,%d,%d.wav' % (i, start, end)
                    chunk_path = chunks_path + chunk_name
                    chunk.export(chunk_path, format='wav')
                    subtitle = self.get_subtitle(chunk_path, client)
                    if subtitle is None: 
                        continue
                    num += 1

                    #写入srt
                    srt_str = str(num)+'\n'
                    self.startTime.append(self.time_convert(start))
                    self.endTime.append(self.time_convert(end))
                    self.videoText.append(subtitle)
                    srt_str += self.time_convert(start) + ' - ' + self.time_convert(end) + '\n'
                    srt_str += subtitle + '\n' + '\n'
                    srt_file.write(srt_str)

                srt_file.close()
                shutil.rmtree(chunks_path)
        return self.startTime, self.endTime, self.videoText

    def convert2wav(self, video_path):
        (folderpath, fullfilename) = os.path.split(video_path)
        (filename, extension) = os.path.splitext(fullfilename)
        audio_name = filename + '_temp.wav'
        audio_path = folderpath + '/' + audio_name
        #print(audio_path)

        ffmpegFormatCode = 'ffmpeg -i {0} -f {1} -vn {2}'
        os.system(ffmpegFormatCode.format(video_path, 'wav', audio_path))

        wav_version = AudioSegment.from_wav(audio_path)
        mono = wav_version.set_frame_rate(16000).set_channels(1)
        audio_16k_path = folderpath + '/' + filename + '.wav'
        mono.export(audio_16k_path, format='wav', codec='pcm_s16le')
        os.remove(audio_path)  # 删除生成的中间wav文件
        return audio_16k_path

    # 连接百度AipSpeech客户端
    def connect_AipSpeech(self):
        # 调用百度API的用户名，密码等
        APP_ID = '23191035'
        API_KEY = 'WAfGnCoaGkm1gog3ZGQ1t4Cn'
        SECRET_KEY = 'HiS3LGvv7yzivzXIRPWlo8hPx3MXM9ue'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        return client

    # 调用百度AipSpeech，将符合格式的音频转换为英文文字
    def get_subtitle(self, file_name, client):
        # 识别本地文件，dev_pid=1737表示英语
        with open(file_name,'rb') as fp:
            content = fp.read()
        return_parameters = client.asr(content, 'wav', 16000, {'dev_pid': 1737})
        if return_parameters['err_no'] != 0:  # 失败返回
            print("------------------fail------------------")
            return 
        return_subtitle = str(return_parameters['result'])[2:-2]  # 正确返回，取返回参数中的字幕部分
        #print(return_subtitle)
        return return_subtitle


    # 时间格式转换，将毫秒值转换为h:m:s,ms格式
    def time_convert(self, time_ms):
        millisecond = time_ms % 1000
        time_s = time_ms // 1000
        second = time_s % 60
        time_m = time_s // 60
        minute = time_m % 60
        hour = time_m // 60
        return_string = '%02d:%02d:%02d,%03d'%(hour, minute, second, millisecond)
        return return_string

    def split_audio(self, audio_segment, min_silence_len=1000, silence_thresh=-16, keep_silence=100, seek_step=1):

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
            end_max = end_i + (start_ii - end_i + 1) // 2  # +1 for rounding with integer division
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

# if __name__ == '__main__':

#     path = os.path.abspath('.') + '/video'
#     S = Subtitle(path)
#     startTime, endTime, videoText = S.return_subtitle()
#     print(startTime)
#     print(endTime)
#     print(videoText)
