import json
import requests
import ast
import time
import os
from youtube_transcript_api import YouTubeTranscriptApi

class Crawler:
    def __init__(self, key):
        self.newurl = ''
        self.newdate = ''
        self.date = ''
        self.beforesecond = ''
        self.now = time.gmtime(time.time())
        self.year = str(self.now.tm_year)    #Current year
        self.month = str(self.now.tm_mon)    #Current month
        self.day = str(self.now.tm_mday)     #Current day
        self.hour = str(self.now.tm_hour)    #Current hour
        self.minute = str(self.now.tm_min)   #Current minute
        self.second = str(self.now.tm_sec)   #Current second
        self.status = True
        self.items = ''
        self.publisheddate = [] #list that contains dates of published

        #Current time  
        self.publishedBefore = "publishedBefore=" + self.year+"-" + self.month + "-" + self.day +"T" + self.hour + ":" + self.minute + ":" +self.second +"Z" 

        self.api_key = key

        self.count = 0

    # 검색 결과 -> 영상 id 저장
    def GetDataBySearchResult(self, query):
        self.query = query
        self.url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&order=date&q={}&relevanceLanguage=En&type=video&videoCaption=none&videoDuration=any&videoType=any&key={}&{}".format(self.query,self.api_key, self.publishedBefore)
        print(self.url)
        r=requests.get(self.url)
        t=json.loads(r.content,encoding='utf-8')
        files = ast.literal_eval(json.dumps(t))
        self.items = files["items"]
        
        results = self.items # 리스트 타입

        self.videoid_list = [i["id"]["videoId"] for i in results]
        print(self.videoid_list)
        print("\n")
        

        self.save_file_name = "search_result/{}.txt".format(self.query)
        if os.path.isfile(self.save_file_name): #  같은 검색어의 파일이 이미 존재하면 이어붙이기
            with open(self.save_file_name, "r") as read_file:
                l = [i[:-1] for i in read_file.readlines()]

            with open(self.save_file_name, "a") as save_file:
                for vid in self.videoid_list: # 파일에 없는 id만 붙이기
                    if vid not in l:
                        save_file.write("{}\n".format(vid))
        
        else: # 같은 검색어의 파일이 없으면 새로 만들기
            with open(self.save_file_name, "w") as save_file:
                for vid in self.videoid_list:
                    save_file.write("{}\n".format(vid))

        # self.count += 1
        # if self.count == 3: 
        #     self.status = False

        for i in range(len(self.items)):
            self.publisheddate.append(self.items[i]['snippet']['publishedAt'])

        self.date ="&publishedBefore="+ self.publisheddate[-1]  #"&publishedBefore=2008-10-16T12%3A35%3A37.000Z"
        self.year = self.date[17:21]        #0000
        self.month = self.date[22:24]       #00
        self.day = self.date[25:27]         #00
        self.hour = self.date[28:30]        #00
        self.minute = self.date[31:33]      #00
        self.second = self.date[34:36]

        #time format: 2017-08-11T17:02:37.000Z

        #Manage Time AND Exception Handling
        if self.second == "00":
            self.second = str((int(self.second) - 1)%60)
            self.minute = str((int(self.minute) - 1)%60)
            if self.minute == "00":
                self.minute = str((int(self.minute) - 1)%60)
                self.hour = str((int(self.hour) - 1)%12)
                if self.hour == "00":
                    self.hour = str((int(self.hour) - 1)%12)
                    if self.day == "01":
                        self.day = str(int(self.day)-1)
                        if self.month == "01":
                            self.month = str((int(self.month)-1)%12)
                            self.year = str(int(self.year) -1)
                        else:
                            self.month = str((int(self.month)-1)%12)

        else:
            self.second = str(int(self.second)-1)
        
        self.publishedBefore = "publishedBefore=" + self.year+ "-" + self.month + "-"\
                      + self.day +"T" + self.hour + ":" + self.minute + ":" +self.second +".000Z"
        

        if len(self.items) != 50:
            self.status = False
            print("DONE")

        print(self.publishedBefore)

    # 영상별 정보 저장
    def GetDataByVideo(self, query):
        
        if not os.path.isdir("videos/{}/".format(query)):
            os.mkdir("videos/{}/".format(query))
            self.video_list = []

        else:
            # 기존에 저장된 영상 list
            self.videos = os.listdir("videos/{}/".format(query))
            self.video_list = [i[:-5] for i in self.videos] # 이미 메타데이터가 저장된 영상의 id list
            # print(self.video_list)


        self.subtitlelist = [i[:-5] for i in os.listdir("subtitles/{}".format(query))]


        # 검색어에 있는 영상 id 가져오기
        search_result_file = "search_result/{}.txt".format(query)
        id_list = []
        with open(search_result_file, "r") as results:
            l = results.readlines()
            id_list = [i[:-1] for i in l] 

        for vid in id_list:
            if vid not in self.video_list and vid in self.subtitlelist:
                self.id = vid
                self.snippet_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}".format(self.id, self.api_key)
                self.contentDetails_url = "https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}".format(self.id, self.api_key)
                self.statistics_url = "https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}".format(self.id, self.api_key)

                self.result = {"id":self.id}

                # snippet
                r=requests.get(self.snippet_url)
                files=json.loads(r.content,encoding='utf-8')
                # print(type(t))
                # files = ast.literal_eval(json.dumps(t))
                # print(type(files))
                # exit()
                
                if len(files["items"]) > 0:
                    print(self.snippet_url)
                    self.items = files["items"][0]["snippet"] # dict -> snippet

                    self.result["categoryId"]=self.items["categoryId"]
                    self.result["description"]=self.items["description"]
                    self.result["publishedAt"]=self.items["publishedAt"]
                    self.result["title"]=self.items["title"]
                    self.result["thmbnails"]=self.items["thumbnails"]["high"]["url"]
                    self.result["channelTitle"]=self.items["channelTitle"]

                    # contentDetails
                    r=requests.get(self.contentDetails_url)
                    files=json.loads(r.content,encoding='utf-8')
                    self.items = files["items"][0]["contentDetails"] # dict -> contentDetails

                    self.result["duration"]=self.items["duration"]
                    self.result["caption"]=self.items["caption"]

                    # statistics
                    r=requests.get(self.statistics_url)
                    files=json.loads(r.content,encoding='utf-8')
                    # files = ast.literal_eval(json.dumps(t))
                    self.items = files["items"][0]["statistics"] # dict -> statistics

                    try:

                        self.result["viewCount"]=self.items["viewCount"]
                    except:
                        self.result["viewCount"]="N/A"
                    try:
                        self.result["likeCount"]=self.items["likeCount"] # likecount가 없는 영상도 있음
                    except:
                        self.result["likeCount"]="N/A"
                    try:
                        self.result["dislikeCount"]=self.items["dislikeCount"]
                    except:
                        self.result["dislikeCount"]="N/A"
                    try:
                        self.result["favoriteCount"]=self.items["favoriteCount"]
                    except:
                        self.result["favoriteCount"]="N/A"
                    try:
                        self.result["commentCount"]=self.items["commentCount"]
                    except:
                        self.result["commentCount"]="N/A"

                    self.save_file_name = "videos/{}/{}.json".format(query,vid)

                    with open(self.save_file_name, "w") as save_video:
                        json.dump(self.result, save_video)
                else:
                    print("Error in {}".format(self.snippet_url))
                    self.save_file_name = "videos/{}/{}.json".format(query, vid)

                    with open(self.save_file_name, "w") as save_video:
                        json.dump(self.result, save_video)

    # 영상 자막 가져오기               
    def GetSubtitle(self, query):

        if not os.path.isdir("subtitles/{}/".format(query)):
            os.mkdir("subtitles/{}/".format(query))
            self.video_list = []

        else:
            # 기존에 저장된 영상 list
            self.videos = os.listdir("subtitles/{}/".format(query))
            self.video_list = [i[:-5] for i in self.videos] # 이미 메타데이터가 저장된 영상의 id list
            print(self.video_list)


        # 검색어에 있는 영상 id 가져오기
        search_result_file = "search_result/{}.txt".format(query)
        id_list = []
        with open(search_result_file, "r") as results:
            l = results.readlines()
            id_list = [i[:-1] for i in l] 

        for vid in id_list:
            self.sub = ""
            if vid not in self.video_list:

                self.save_file_name = "subtitles/{}/{}.json".format(query, vid)

                try:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(vid)
                    try:
                        transcript = str(transcript_list.find_manually_created_transcript(['en']))
                        if transcript.startswith("en"):
                            print("transcript available {}".format(vid))
                            self.sub = YouTubeTranscriptApi.get_transcript(vid)
                    except:
                        try:
                            transcript_generated = str(transcript_list.find_generated_transcript(['en']))
                            if transcript_generated.startswith("en"):
                                print("generated transcript available {}".format(vid))
                                self.sub = YouTubeTranscriptApi.get_transcript(vid)
                        except:
                            print("transcript not available on video {}".format(vid))

                except:
                    print("transcript not available on video {}".format(vid))

            if len(self.sub) > 0:
                with open(self.save_file_name, "w") as save_video:

                    json.dump(self.sub, save_video)
                    print(vid)


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


API_KEY = "[YOUR_API_KEY]"

def main():
    a = Crawler(API_KEY) #api key

    # 영상 id 가져오기
    while a.status:
        a.GetDataBySearchResult(sample_query15)

    # 영상마다 데이터 가져오기
    a.GetDataByVideo(sample_query1)

    for q in query_list:
        a.GetDataByVideo(q)

    # 영상 자막 가져오기
    for q in query_list:
        a.GetSubtitle(q)
main()