import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';


// 영상에서 중요한 부분의 자막을 출력하여 보여주는 위젯
class SummaryList extends StatefulWidget {
  final vid;
  const SummaryList({this.vid}); // 생성자: 영상의 id를 파라메터로 받음

  @override
  _SummaryListState createState() => _SummaryListState();
}
class _SummaryListState extends State<SummaryList> {
  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: FirebaseFirestore.instance.collection("video").snapshots(), // Firestore에서 video 컬렉션을 가져옴
      builder: (context, snapshot) {
        List<QueryDocumentSnapshot> l = snapshot.data.docs;
        var idx = l.indexWhere((element) => element.data()["id"]==widget.vid);
        var summaryitems = snapshot.data.docs[idx].data()["summary"].toList(); // 파라메터로 받은 id에 해당하는 영상의 요약 텍스트를 Firebase에서 가져옴 
        return ListView.builder( // 영상 자막을 화면에 출력하여 보여줌
          physics: const AlwaysScrollableScrollPhysics(),
          shrinkWrap: true,
          itemCount: summaryitems.length,
          itemBuilder: (context, index) {
            return Container(
              margin: EdgeInsets.only(left: 20, top: 20),
              width: MediaQuery.of(context).size.width * 0.8,
              child: Row(
                children: [
                  Text("${summaryitems[index]['timestamp']}", style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.3)),
                  Text(" : "),
                  Text("...${summaryitems[index]['text']}...")

                ],
              ),
            );
            },
          );

      },
    );
  }
}