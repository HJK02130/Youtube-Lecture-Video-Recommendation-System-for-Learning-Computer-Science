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

# recommendation: 카테고리별로 조회수, 좋아요 수, 최신 영상 추천하기
rec = [{"id":"view"},{"id":"like"},{"id":"date"}]
for q in range(len(query_list)):

    if category_list[q] not in rec[0].keys():
        rec[0][category_list[q]] = {}
    if category_list[q] not in rec[1].keys():
        rec[1][category_list[q]] = {}
    if category_list[q] not in rec[2].keys():
        rec[2][category_list[q]] = {}

    videolist = os.listdir("subtitles/{}".format(query_list[q])) # query에 있는 json 파일 리스트
    reclist = {"id":query_list[q],"view":{}, "like":{}, "date":{}}
    if len(videolist) > 20:
        print(category_list[q])
        for videojsonfile in videolist:
            try:
                with open('videos/{}/{}'.format(query_list[q],videojsonfile), "r") as j:
                    vjson = json.load(j)
                    vid = vjson["id"]
                    #viewCount
                    if "N/A" in vjson["viewCount"]:
                        reclist["view"][vid] = 0
                    else:
                        reclist["view"][vid] = int(vjson["viewCount"])
                    #likeCount
                    if "N/A" in vjson["likeCount"]:
                        reclist["like"][vid] = 0
                    else:
                        reclist["like"][vid] = int(vjson["likeCount"])
                    #date
                    reclist["date"][vid] = vjson["publishedAt"]


            except Exception as e: 
                continue
            
        # 상위 20개 뽑기
        sorted_view = {k: v for k, v in sorted(reclist["view"].items(), key=lambda item: item[1])}
        sorted_view_keys = list(sorted_view.keys())
        sorted_view_keys.reverse()

        sorted_like = {k: v for k, v in sorted(reclist["like"].items(), key=lambda item: item[1])}
        sorted_like_keys = list(sorted_like.keys())
        sorted_like_keys.reverse()

        sorted_date = {k: v for k, v in sorted(reclist["date"].items(), key=lambda item: item[1])}
        sorted_date_keys = list(sorted_date.keys())
        sorted_date_keys.reverse()

        # 20개 중 랜덤으로 10개 뽑기, 순서도 랜덤
        #view
        c = 0
        viewreclist = []
        while c < 10:
            random.shuffle(real_videos)
            randlist = real_videos[:10]
            if randlist not in viewreclist:
                rec[0][category_list[q]]["rec{}".format(c)] = randlist
                viewreclist.append(randlist)
                c += 1
        

        #like
        c = 0
        likereclist = []
        while c < 10:
            random.shuffle(real_videos)
            randlist = real_videos[:10]
            if randlist not in likereclist:
                rec[1][category_list[q]]["rec{}".format(c)] = randlist
                likereclist.append(randlist)
                c += 1

        # print(likereclist)

        #date
        c = 0
        datereclist = []
        while c < 10:
            random.shuffle(real_videos)
            randlist = real_videos[:10]
            if randlist not in datereclist:
                rec[2][category_list[q]]["rec{}".format(c)] = randlist
                datereclist.append(randlist)
                c += 1

    else:
        #view
        c = 0
        viewreclist = []
        while c < 10:
            random.shuffle(real_videos)
            randlist = real_videos[:10]
            if randlist not in viewreclist:
                rec[0][category_list[q]]["rec{}".format(c)] = randlist
                viewreclist.append(randlist)
                c += 1

        #like
        c = 0
        likereclist = []
        while c < 10:
            random.shuffle(real_videos)
            randlist = real_videos[:10]
            if randlist not in likereclist:
                rec[1][category_list[q]]["rec{}".format(c)] = randlist
                likereclist.append(randlist)
                c += 1

        #date
        c = 0
        datereclist = []
        while c < 10:
            random.shuffle(real_videos)
            randlist = real_videos[:10]
            if randlist not in datereclist:
                rec[2][category_list[q]]["rec{}".format(c)] = randlist
                datereclist.append(randlist)
                c += 1






with open("new_recommendation.json", "w") as writefile:
    json.dump(rec, writefile)


with open("new_recommendation.json", "r") as readfile:
    temp = json.load(readfile)

# print(len(temp["videos"].keys()))