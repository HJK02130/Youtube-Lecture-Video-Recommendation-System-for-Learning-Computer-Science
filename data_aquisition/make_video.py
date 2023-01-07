import json, os, random

total = []

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

cat1 = "Theory of Computation"
cat2 = "Information and coding theory"
cat3 = "Data structures and algorithms"
cat4 = "Programming language theory and formal methods"
cat5 = "Artificial intelligence"
cat6 = "Computer architecture and organization"
cat7 = "Concurrent, parallel and distributed computing"
cat8 = "Computer networks"
cat9 = "Computer security and cryptography"
cat10 = "Databases and data mining"
cat11 = "Computer graphics and visualization"
cat12 = "Image and sound processing"
cat13 = "Computational science, finance and engineering"
cat14 = "Social computing and human-computer interaction"
cat15 = "Software engineering"
category_list = [cat1, cat2, cat3, cat4, cat5, cat6, cat7, cat8, cat9, cat10, cat11, cat12, cat13, cat14, cat15]

with open("videos.json", "r") as jsonfile:
  videodata = json.load(jsonfile)
  videodata = list(videodata["videos"].keys())

with open("title_based_rec.json", "r") as tfile:
    title_data = json.load(tfile)
    real_videos = list(title_data[0].keys())
    print(len(real_videos))

# video metadata 시트 불러오기
for q in range(len(query_list)):
    videolist = os.listdir("subtitles/{}".format(query_list[q])) # query에 있는 json 파일 리스트
    # print(category_list[q])
    for videojsonfile in videolist:
        vidinfo = {}
        v = videojsonfile[:-5]
        # print(v)
        if v in real_videos:
            try:
                with open('videos/{}/{}'.format(query_list[q],videojsonfile), "r") as j:
                    vjson = json.load(j)
                with open('data/summarytext/{}/{}'.format(query_list[q],videojsonfile), "r") as j:
                    sjson = json.load(j)

                    vid = vjson["id"]
                    #id
                    vidinfo["id"] = vid
                    # category
                    vidinfo["category"] = category_list[q] 
                    # title
                    vidinfo["title"] = vjson["title"]
                    #channelTitle
                    vidinfo["channelTitle"] = vjson["channelTitle"]
                    #duration
                    vidinfo["duration"] = vjson["duration"]
                    #description
                    vidinfo["description"] = vjson["description"]
                    #thumbnail
                    vidinfo["thumbnails"] = vjson["thmbnails"]
                    #viewCount
                    vidinfo["viewCount"] = vjson["viewCount"]
                    #likeCount
                    vidinfo["likeCount"] = vjson["likeCount"]
                    #dislikeCount
                    vidinfo["dislikeCount"] = vjson["dislikeCount"]

                    #recommendation: 이후 수정 필. 일단 랜덤으로 넣기
                    vidinfo["recommendation"] = {"bytitle":[], "byhistory": [], "bythumbnail":[]}
                    random.shuffle(real_videos)
                    for i in range(10):
                        vidinfo["recommendation"]["bytitle"] = title_data[0][vid]
                    for i in range(10):
                        vidinfo["recommendation"]["byhistory"].append(real_videos[i+10])
                    for i in range(10):
                        print(real_videos[i+20])
                        vidinfo["recommendation"]["bythumbnail"].append(real_videos[i+20])
                    #summary
                    # start time: sec -> mm:ss
                    for t in sjson:
                        start = t["start"]
                        start = int(start)
                        startminute = start // 60
                        startsecond = start % 60

                        newstart = "{}:{}".format(startminute, startsecond)
                        t["timestamp"] = newstart

                    vidinfo["summary"] = sjson

            except Exception as e:
                print(e)
                continue
            total.append(vidinfo)


with open("new_video.json", "w") as writefile:
    json.dump(total, writefile)

with open("new_video.json", "r") as readfile:
    temp = json.load(readfile)
