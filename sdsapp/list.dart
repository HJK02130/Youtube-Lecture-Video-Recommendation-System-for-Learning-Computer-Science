import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'video_main.dart';
import "dart:math";
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';

// 사용자가 이전에 시청한 영상을 기반으로 한 영상 추천 리스트를 출력해주는 위젯
class Hlist extends StatefulWidget { 
  final page;
  final i;
  const Hlist({this.page, this.i}); // 생성자: 행 번호와 카테고리 이름 파라메터로 받음
  @override
  _HlistState createState() => _HlistState();
}

class _HlistState extends State<Hlist> {
  final imageheight = 120.0;
  var router = {0: ["byhistory","bythumbnail", "bytitle"], 1:[0,1,2]};
  @override
  Widget build(BuildContext context) {

    return StreamBuilder(
      stream: FirebaseFirestore.instance.collection("user").snapshots(), // Firestore에서 user 컬렉션을 가져옴
      builder: (context, snapshot) {
        List<QueryDocumentSnapshot> l = snapshot.data.docs.reversed.toList();
        var idx = l.indexWhere((element) => element.data()["id"] == "user1");
        var items = snapshot.data.docs[idx].data()["viewhistory"];
        var likehistory = snapshot.data.docs[idx].data()["likehistory"];
        var lastitem = items.last;
        var catlist = [];
        CollectionReference users = FirebaseFirestore.instance.collection("user"); // 컬렉션 update를 하기 위한 CollectionReference 타입 변수
        return StreamBuilder(
          stream: FirebaseFirestore.instance.collection("video2").snapshots(), // Firestore에서 video 컬렉션을 가져옴
          builder: (context, snapshot) {
            List<QueryDocumentSnapshot> vidl = snapshot.data.docs.reversed.toList();
            var lastitemdata = snapshot.data.docs[vidl.indexWhere((e) => e.data()["id"] == lastitem)].data();
            return SingleChildScrollView( // 추천 영상 리스트를 한 행에 보여주기 위한 위젯
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(
                    height: 250,
                    width: 2500,
                    child: ListView.builder(
                      physics: const AlwaysScrollableScrollPhysics(),
                      scrollDirection: Axis.horizontal,
                      shrinkWrap: true,
                      itemCount: 10,
                      itemBuilder: (context, index){
                        print("${lastitemdata["recommendation"]['${widget.i}']}");
                        var vid = lastitemdata["recommendation"]['${widget.i}'][index];
                        var viditem = snapshot.data.docs[vidl.indexWhere((element) => element.data()["id"] == vid)];
                        return Container(
                          margin: EdgeInsets.only(left: 10, right: 10),
                          child: Column(
                            children: [
                              SizedBox(
                                width: 200,
                                child: GestureDetector(
                                  child: Image.network(viditem["thumbnails"]),
                                  onTap: () {
                                    items.add(viditem["id"]);
                                    var newviewhistory = items.toSet().toList();
                                    users.doc("user1").update({ // 사용자가 영상을 시청하면 시청 기록에 새로운 영상 업데이트
                                      "id":"user1",
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
                              ),
                            ],
                          )
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
  }
}