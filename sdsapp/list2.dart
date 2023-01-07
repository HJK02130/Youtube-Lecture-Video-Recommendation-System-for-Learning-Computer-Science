import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'video_main.dart';
import "dart:math";
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';

// 사용자가 이전에 시청한 영상의 카테고리를 기반으로 한 영상 추천 리스트를 출력해주는 위젯
class Hlist2 extends StatefulWidget {
  final page;
  final i;
  const Hlist2({this.page, this.i}); // 생성자: 행 번호와 추천 내용(byhistory, bythumbnail, bytitle)을 파라메터로 받음

  @override
  _Hlist2State createState() => _Hlist2State();
}

class _Hlist2State extends State<Hlist2> {
  final route = {0:"view", 1:"like", 2:"date"};
  final t = {0: "Recommendation by View Count", 1: "Recommendation by Like Count", 2:"Recently Uploaded Videos"};
  var imageheight = 120.0;
  @override
  Widget build(BuildContext context) {
    var randnum = Random().nextInt(9);
    return StreamBuilder(
      stream: FirebaseFirestore.instance.collection("video").snapshots(), // Firestore에서 video 컬렉션을 가져옴
      builder: (context, videosnapshot) {
        List<QueryDocumentSnapshot> l = videosnapshot.data.docs;
        var cat = videosnapshot.data.docs[l.indexWhere((element) => element.data()["id"] == widget.i)].data()["category"];

        return StreamBuilder(
          stream: FirebaseFirestore.instance.collection("recommendation").snapshots(), // Firestore에서 recommendation 컬렉션을 가져옴
          builder: (context, snapshot){
            List<QueryDocumentSnapshot> recl = snapshot.data.docs;
            var idx = recl.indexWhere((element) => element.data()["id"] == route[widget.page]);
            var item = snapshot.data.docs[idx].data()[cat]["rec$randnum"];
            return StreamBuilder(
              stream: FirebaseFirestore.instance.collection("user").snapshots(), // Firestore에서 user 컬렉션을 가져옴
              builder: (context, snapshot){
                List<QueryDocumentSnapshot> userl = snapshot.data.docs;
                var uidx = userl.indexWhere((element) => element.data()["id"]=="user1");
                var likehistory = snapshot.data.docs[uidx].data()["likehistory"];
                var viewhistory = snapshot.data.docs[uidx].data()["viewhistory"];
                CollectionReference users = FirebaseFirestore.instance.collection("user"); // 컬렉션 update를 하기 위한 CollectionReference 타입 변수
                return SingleChildScrollView( // 추천 영상 리스트를 한 행에 보여주기 위한 위젯
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(child:Text("$cat : ${t[widget.page]}", style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.5),),margin: EdgeInsets.only(left:10, top: 15.0, bottom:5, right:10)),
                      SizedBox(
                        height: 250,
                        width: 2500,
                        child: ListView.builder(
                          physics: const AlwaysScrollableScrollPhysics(),
                          scrollDirection: Axis.horizontal,
                          shrinkWrap: true,
                          itemCount: 10,
                          itemBuilder: (context, index) {
                            var viditem = videosnapshot.data.docs[l.indexWhere((e) => e.data()["id"] == item[index])].data();
                            return Container(
                              margin: EdgeInsets.only(left: 10, right: 10),
                              child: Column(
                                children: [

                                  Column(
                                    children: [
                                      SizedBox(
                                        width: 200,
                                        child: GestureDetector(
                                          child: Image.network(viditem["thumbnails"]),
                                          onTap: () {
                                            viewhistory.add(viditem["id"]);
                                            var newviewhistory = viewhistory.toSet().toList();
                                            users.doc("user1").update({ // 사용자가 영상을 시청하면 시청 기록에 새로운 영상 업데이트
                                              "id": "user1",
                                              "likehistory": likehistory,
                                              "viewhistory": newviewhistory
                                            });
                                            print("$newviewhistory");
                                            Navigator.push( // 영상을 클릭하면 영상을 재생하는 페이지로 넘아가도록 하는 Navigator
                                                context, MaterialPageRoute(
                                              builder: (context) => VideoMain(vid: viditem["id"]),
                                            )
                                            );
                                          },
                                        ),
                                      ),
                                      Container(
                                        margin: EdgeInsets.only(top:10, bottom: 10),
                                        child: SizedBox(
                                          width: 200,
                                          child: Text(viditem["title"]),
                                        ),
                                      )
                                    ],
                                  ),
                                ],
                              ),
                            );
                          },
                        ),
                      )
                    ],
                  ),
                );
              },
            );
          },
        );
      },
    );
  }
}