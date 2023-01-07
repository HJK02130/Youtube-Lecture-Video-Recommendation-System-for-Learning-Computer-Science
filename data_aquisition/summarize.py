from __future__ import unicode_literals
import argparse
import os
import re
from itertools import starmap
import multiprocessing
from pytube.cli import on_progress
from pytube import YouTube
import json
import sys
import time

import pysrt
import youtube_dl
import chardet
import nltk
nltk.download('punkt')

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from youtube_transcript_api import YouTubeTranscriptApi

def summarize(srt_file, n_sentences, language="english"):
    """ Generate segmented summary
    Args:
        srt_file(str) : The name of the SRT FILE
        n_sentences(int): No of sentences
        language(str) : Language of subtitles (default to English)
    Returns:
        list: segment of subtitles
    """
    parser = PlaintextParser.from_string(
        srt_to_txt(srt_file), Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    segment = []
    for sentence in summarizer(parser.document, n_sentences):
        index = int(re.findall("\(([0-9]+)\)", str(sentence))[0])
        item = srt_file[index]
        segment.append(srt_segment_to_range(item))

    print(segment)
    jsonfile = []
    for i in segment:
        temp = {}
        temp["start"] = i[0]
        temp["end"] = i[1]
        jsonfile.append(temp)

    global summarytextfilename
    # with open(summarytextfilename, "w") as writefile:
    #     json.dump(jsonfile, writefile)
    #     print("write json in {}".format(summarytextfilename))

    global srtfilename
    global videoid
    
    # print("file created")
    # summary_text()
    # os.remove(videofilename+".mp4")
    return segment

def srt_to_txt(srt_file):
    """ Extract text from subtitles file
    Args:
        srt_file(str): The name of the SRT FILE
    Returns:
        str: extracted text from subtitles file
    """
    text = ''
    for index, item in enumerate(srt_file):
        if item.text.startswith("["):
            continue
        text += "(%d) " % index
        text += item.text.replace("\n", "").strip("...").replace(
                                     ".", "").replace("?", "").replace("!", "")
        text += ". "
    return text

def srt_segment_to_range(item):
    """ Handling of srt segments to time range
    Args:
        item():
    Returns:
        int: starting segment
        int: ending segment of srt
    """
    start_segment = item.start.hours * 60 * 60 + item.start.minutes * \
        60 + item.start.seconds + item.start.milliseconds / 1000.0
    end_segment = item.end.hours * 60 * 60 + item.end.minutes * \
        60 + item.end.seconds + item.end.milliseconds / 1000.0
    return start_segment, end_segment

def time_regions(regions):
    """ Duration of segments
    Args:
        regions():
    Returns:
        float: duration of segments
    """
    return sum(starmap(lambda start, end: end - start, regions))

def find_summary_regions(srt_filename, duration=300, language="english"):
    """ Find important sections
    Args:
        srt_filename(str): Name of the SRT FILE
        duration(int): Time duration
        language(str): Language of subtitles (default to English)
    Returns:
        list: segment of subtitles as "summary"
    """
    srt_file = pysrt.open(srt_filename)

    enc = chardet.detect(open(srt_filename, "rb").read())['encoding']
    srt_file = pysrt.open(srt_filename, encoding=enc)

    # generate average subtitle duration
    subtitle_duration = time_regions(
        map(srt_segment_to_range, srt_file)) / len(srt_file)
    # compute number of sentences in the summary file
    n_sentences = duration / subtitle_duration
    summary = summarize(srt_file, n_sentences, language)
    total_time = time_regions(summary)
    too_short = total_time < duration
    count = 0
    if too_short:
        while total_time < duration and count < 3:
            count += 1
            n_sentences += 1
            summary = summarize(srt_file, n_sentences, language)
            total_time = time_regions(summary)
    else:
        while total_time > duration:
            n_sentences -= 1
            summary = summarize(srt_file, n_sentences, language)
            total_time = time_regions(summary)
    return summary

def get_summary(subtitles="1.srt"):
    """ Abstract function
    Args:
        filename(str): Name of the Video file (defaults to "1.mp4")
        subtitles(str): Name of the subtitle file (defaults to "1.srt")
    Returns:
        True
    """
    regions = find_summary_regions(subtitles, 120, "english")
    # summary = create_summary(filename, regions)
    # base, ext = os.path.splitext(filename)
    # output = "{0}_1.mp4".format(base)
    # summary.to_videofile(
    #             output,
    #             codec="libx264",
    #             temp_audiofile="temp.m4a", remove_temp=True, audio_codec="aac")
    return True

def download_video_srt(subs):
    """ Downloads specified Youtube video's subtitles as a vtt/srt file.
    Args:
        subs(str): Full url of Youtube video
    Returns:
        True
    The video will be downloaded as 1.mp4 and its subtitles as 1.(lang).srt
    Both, the video and its subtitles, will be downloaded to the same location
    as that of this script (sum.py)
    """
    ydl_opts = {
        'format': 'best',
        'outtmpl': '1.%(ext)s',
        'subtitlesformat': 'srt',
        'writeautomaticsub': True,
        # 'allsubtitles': True # Get all subtitles
    }

    movie_filename = ""
    subtitle_filename = ""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([subs])
        result = ydl.extract_info("{}".format(url), download=True)
        movie_filename = ydl.prepare_filename(result)
        subtitle_info = result.get("requested_subtitles")
        subtitle_language = list(subtitle_info.keys())[0]
        subtitle_ext = subtitle_info.get(subtitle_language).get("ext")
        subtitle_filename = movie_filename.replace(".mp4", ".%s.%s" %
                                                   (subtitle_language,
                                                    subtitle_ext))
    return movie_filename, subtitle_filename

def make_srt(q,videoid) : # 태원 이 함수 연결하면 돼 메인 파일에...
    raw_filename = 'subtitles/"Artificial intelligence" AND ("lecture"OR"course"OR"class")/' + videoid + ".json"
    raw_filename = "subtitles/{}/{}.json".format(q,videoid)
    # srt_filename = videoid + ".srt"  # 태원 여기 파일 디렉토리 설정해야돼

    with open(raw_filename, 'r') as raw_file :
        raw_data = json.load(raw_file)

        total_write = ""
        for raw_time in range(len(raw_data)):
            raw_start_time = float(raw_data[raw_time]["start"])
            raw_duration = float(raw_data[raw_time]["duration"])
            raw_text = raw_data[raw_time]["text"]
            
            raw_end_time = raw_start_time + raw_duration
            start_time = time.strftime('%H:%M:%S', time.gmtime(raw_start_time))
            end_time = time.strftime('%H:%M:%S', time.gmtime(raw_end_time))

            raw_start_second = str(round(raw_start_time % 1,3))[2:5]
            if len(raw_start_second) == 2 :
                raw_start_second = raw_start_second + "0"
            elif len(raw_start_second) == 1 :
                raw_start_second = raw_start_second + "00"
            elif len(raw_start_second) == 0 :
                raw_start_second = "000"
            
            raw_end_second = str(round(raw_end_time % 1,3))[2:5]
            if len(raw_end_second) == 2 :
                raw_end_second = raw_end_second + "0"
            elif len(raw_end_second) == 1 :
                raw_end_second = raw_end_second + "00"
            elif len(raw_end_second) == 0 :
                raw_end_second = "000"

            firstline = str(raw_time + 1)
            secondline = "{},{} --> {},{}".format(start_time, raw_start_second, end_time, raw_end_second)
            thirdline = raw_text.replace("\n"," ")

            total_write = total_write + firstline + "\n" + secondline + "\n" + thirdline + "\n" + "\n"
            
        srtfilename = "data/srt/{}.srt".format(videoid)
        with open(srtfilename, "w") as writefile:
            writefile.write(total_write)

def summary_text(videoid):
    
    summary_filename = "data/summary/" + videoid + ".json"
    raw_filename = "data/rawjson/" + videoid + ".json"

    with open(summary_filename, 'r') as summary_file, open(raw_filename, 'r') as raw_file :
        raw_data = json.load(raw_file)
        summary_data = json.load(summary_file) 

        raw_time = 0
        timeline_list = []
        

        for summary_time in range(len(summary_data)) :
            sum_start_time = summary_data[summary_time][0]
            sum_end_time = summary_data[summary_time][1]

            timeline = {}
            cont = True
            # raw_time = 0
            summary = ""

            count = 0

            while cont and count < 3 :
                count += 1
                raw_start_time = float(raw_data[raw_time]["start"])
                raw_duration = float(raw_data[raw_time]["duration"])
                raw_text = raw_data[raw_time]["text"]
                raw_end_time = raw_start_time + raw_duration

                # if sum_start_time <= raw_start_time and raw_end_time <= sum_end_time :
                if sum_start_time <= raw_start_time <= sum_end_time :
                    summary = summary + raw_text

                elif sum_end_time < raw_start_time :
                    cont = False
                    sum_start_time_min = int(sum_start_time // 60)
                    sum_start_time_sec = int(sum_start_time % 60)
                    if len(str(sum_start_time_sec)) == 1 :
                        sum_start_time_sec = str(0)+str(sum_start_time_sec)
                    sum_start = str(sum_start_time_min) + ":" + str(sum_start_time_sec)
                    
                    if len(summary) > 10 :
                        timeline["start_min"] = sum_start
                        timeline["start_sec"] = sum_start_time
                        timeline["value"] = "... {} ...".format(summary)
                        timeline_list.append(timeline)
                        
                
                raw_time = raw_time + 1
            

    with open("data/summary_text/" + videoid + ".json", 'w') as outfile :
        json.dump(timeline_list, outfile)
 
def summary(q,vid):

    videoid = vid
    summaryjsonfilename = 'summary/{}.json'.format(videoid)

    if os.path.isfile(summaryjsonfilename):
        with open(summaryjsonfilename, "r") as json_file:
            json_data = json.load(json_file)
        # return json_data
    
    else:
        
        print("summarizing process")

        # rawjson = YouTubeTranscriptApi.get_transcript(videoid)
        # rawjsonfilename = 'subtitles/"Artificial intelligence" AND ("lecture"OR"course"OR"class")/{}.json'.format(videoid)

        # with open(rawjsonfilename,"w") as json_file:
            # json.dump(rawjson, json_file)
            # print("raw json file saved")


        video_link = "https://www.youtube.com/watch?v=" + videoid
        filename = "data/summary/" + videoid

        videofilename = videoid
        srtfilename = "data/srt/{}.srt".format(videoid)

        # yt = YouTube(video_link, on_progress_callback=on_progress)
        
        # caption = yt.captions.get_by_language_code(('en', "en-GB"))
        make_srt(q,videoid)
        print("srt saved")
        
        region = find_summary_regions(srtfilename)
        
        summarytextfilename = "data/summary/{}.json".format(videoid)
        
        with open(summarytextfilename,"w") as json_file:
            json.dump(region, json_file)
            print("summary region file saved {}".format(summarytextfilename))

        # summary_text(videoid)

        
        # with open(summaryjsonfilename, "r") as json_file:
        #     json_data = json.load(json_file)


    # print("type: {}".format(type(json_data)))

    # return json_data


def summary_to_json(query,vid):

    if not os.path.isdir("data/summarytext/{}/".format(query)):
        os.mkdir("data/summarytext/{}".format(query))

    subtitletextpath = "subtitles/{}/{}.json".format(query, vid) #원본 자막 text
    summarytimepath = "data/summary/{}.json".format(vid) # 요약 시간 timeline
    summarytextpath = "data/summarytext/{}/{}.json".format(query,vid) # 요약된 텍스트 저장할 주소

    with open(subtitletextpath, "r") as subtitletext:
        subtitletext_json_data = json.load(subtitletext)
    with open(summarytimepath, "r") as summmarytime:
        summmarytime_json_data = json.load(summmarytime)
    # with open(summarytextpath, "w") as summmarytext:
    #     summmarytext_json_data = json.load(summmarytext)
    
    summmarytext_json_data = []
    timelist = []
    c = 0

    for i in range(len(summmarytime_json_data)):
        summary_start_time = summmarytime_json_data[i][0]
        previous_time = summmarytime_json_data[i][0]
        for j in range(len(subtitletext_json_data)):
            if subtitletext_json_data[j]["start"] == summary_start_time:
                if (len(timelist) < 1) or ((summary_start_time - timelist[-1]) > 15.0): # 이전것과 시간차이가 5초 이상일때는 따로 저장
                    summmarytext_json_data.append({"text": subtitletext_json_data[j]["text"], "start":subtitletext_json_data[j]["start"]})
                    timelist.append(summary_start_time)
            elif subtitletext_json_data[j]["start"] == summary_start_time and len(timelist) > 0 : 
                if ((summary_start_time - timelist[-1]) <= 15.0) :# 이전것과 시간차이가 5초 이하일때는 이전 것과 같이 저장
                    summmarytext_json_data[-1]["text"] += " "
                    summmarytext_json_data[-1]["text"] += subtitletext_json_data[j]["text"]
            else:
                continue
    
    with open(summarytextpath, "w") as summmarytext:
        json.dump(summmarytext_json_data, summmarytext)

    print("summary text created {}".format(summarytextpath))
    
    


sample_query1 = '"Theory of computation" AND ("lecture"OR"course"OR"class")'
sample_query2 = '"Information and coding theory" AND ("lecture"OR"course"OR"class")'
sample_query3 = '"Data structures and algorithms" AND ("lecture"OR"course"OR"class")'
sample_query4 = '"Programming language theory and formal methods" AND ("lecture"OR"course"OR"class")'
sample_query5 = '"Artificial intelligence" AND ("lecture"OR"course"OR"class")'
sample_query6 = '"Computer architecture and organization" AND ("lecture"OR"course"OR"class")'
sample_query7 = '"Concurrent, parallel and distributed computing" AND ("lecture"OR"course"OR"class")'
sample_query8 = '"Computer networks" AND ("lecture"OR"course"OR"class")'
sample_query9 = '"Computer security and cryptography" AND ("lecture"OR"course"OR"class")'
sample_query10 = '"Databases and data mining" AND ("lecture"OR"course"OR"class")'
sample_query11 = '"Computer graphics and visualization" AND ("lecture"OR"course"OR"class")'
sample_query12 = '"Image and sound processing" AND ("lecture"OR"course"OR"class")'
sample_query13 = '"Computational science, finance and engineering" AND ("lecture"OR"course"OR"class")'
sample_query14 = '"Social computing and human-computer interaction" AND ("lecture"OR"course"OR"class")'
sample_query15 = '"Software engineering" AND ("lecture"OR"course"OR"class")'
query_list = [sample_query1, sample_query2, sample_query3, sample_query4, sample_query5, sample_query6, sample_query7, sample_query8, sample_query9, sample_query10, sample_query11, sample_query12, sample_query13, sample_query14, sample_query15]



def main():
    error_list = []
    for q in query_list:
        
        videos = os.listdir("subtitles/{}/".format(q))
        video_list = [i[:-5] for i in videos] # 이미 메타데이터가 저장된 영상의 id list

        for vid in video_list:
            if not os.path.isfile("data/summarytext/{}/{}.json".format(q,vid)):
                try:
                    summary(q,vid)
                    summary_to_json(q,vid)
                except:
                    error_list.append({"q":q, "vid":vid})
                    continue
                # summary(vid)
                # summary_to_json(q,vid)
    
    print(error_list)
main()