from speech2txt import Subtitle
from eng2chn import Translation
from textEmbedding import Embedding
import json


def get_videoContent(path):
    '''
        path: video path
        return: "videoContent" data
    '''
    print("[VideoToContent]")
    S = Subtitle(path)
    startTime, endTime, videoTextEnglish, allTextEnglish = S.return_subtitle()

    print("[Translation]")
    T = Translation(videoTextEnglish, site="baidu")
    videoTextChinese, allTextChinese = T.parse_chinese()

    print("[Embedding]")
    E = Embedding()
    embeddings = E.text_embedding(videoTextEnglish)

    video_list = []
    video_size = len(startTime)
    for i in range(0, video_size):
        videoContent = {
            "startTime": startTime[i],
            "endTime": endTime[i],
            "textEnglish": videoTextEnglish[i],
            "textEmbedding": embeddings[i],
            "textChinese": videoTextChinese[i]
        }
        video_list.append(videoContent)

    return video_list


if __name__ == '__main__':
    try:
        path = "/data/zjj/code/Information_Retrival/search-low-levelmasterdosearch/local/video/1.mp4"
        video_list = get_videoContent(path)
        print("finish " + path)
    except Exception as e:
        print(e)
        print("error " + path)
    else:
        with open("output.json", "w", encoding="utf-8") as fout:
            output = json.dumps(video_list, ensure_ascii=False, indent=2, separators=(',', ': '))
            fout.write(output)
