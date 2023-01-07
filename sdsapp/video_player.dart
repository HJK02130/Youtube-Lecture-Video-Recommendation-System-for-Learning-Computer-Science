import 'package:flutter/material.dart';
import "summary.dart";
import 'package:youtube_player_flutter/youtube_player_flutter.dart';
import 'package:firebase_core/firebase_core.dart';
import "package:cloud_firestore/cloud_firestore.dart";

// 영상이 실제로 출력되는 위젯
class Player extends StatefulWidget {
  final vid;
  const Player({this.vid}); // 생성자: 영상의 id를 파라메터로 받음
  @override
  _PlayerState createState() => _PlayerState();
}

class _PlayerState extends State<Player> {

  @override
  Widget build(BuildContext context) {
    YoutubePlayerController _controller = YoutubePlayerController(
      initialVideoId: widget.vid,
      flags: YoutubePlayerFlags(
        autoPlay: true,
        mute: true,
      ),
    );
    return YoutubePlayer(
      controller: _controller,
      showVideoProgressIndicator: true,

    );
  }
}

// 영상의 정보(제목, 채널, 설명 등)를 보여주는 위젯
class VideoInfo extends StatefulWidget {
  final vid;
  const VideoInfo({this.vid});
  @override
  _VideoInfoState createState() => _VideoInfoState();
}

class _VideoInfoState extends State<VideoInfo> {
  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: FirebaseFirestore.instance.collection("video").snapshots(), // Firestore에서 video 컬렉션을 가져옴
      builder: (context, snapshot){
        List<QueryDocumentSnapshot> l = snapshot.data.docs;
        var idx = l.indexWhere((element) => element.data()["id"]==widget.vid);
        var item = snapshot.data.docs[idx].data();
        print(item);
        return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Container(
                padding: EdgeInsets.fromLTRB(20, 20, 20, 20),
                child: Text(item["title"], style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.3),)
            ),

            Container(
                padding: EdgeInsets.fromLTRB(20, 10, 0, 0),
                child: Text(item["channelTitle"], style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.3),)
            ),
            Container(
                padding: EdgeInsets.fromLTRB(20, 20, 20, 10),
                child: Text(item["description"], style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.0),)
            ),
            SizedBox(
              height: 10.0,
            )

          ],
        );
      }
    );
  }
}

// 좋아요버튼
class LikeButtons extends StatefulWidget {
  final vid;
  const LikeButtons({this.vid});

  @override
  _LikeButtonsState createState() => _LikeButtonsState();
}

class _LikeButtonsState extends State<LikeButtons> {
  bool like = false;
  var added = false;
  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: FirebaseFirestore.instance.collection("user").snapshots(), // Firestore에서 user 컬렉션을 가져옴
      builder: (context, snapshot) {
        List<QueryDocumentSnapshot> l = snapshot.data.docs;
        var idx = l.indexWhere((element) => element.data()["id"]=="user1");
        var items = snapshot.data.docs[idx].data()["likehistory"];
        var viewitems = snapshot.data.docs[idx].data()["viewhistory"];
        var cnt = items.where((element) => element==widget.vid);
        print("$items");
        print("$cnt");
        CollectionReference users = FirebaseFirestore.instance.collection("user"); // 컬렉션 update를 하기 위한 CollectionReference 타입 변수

        return InkWell(
        child: Icon(
        like ? Icons.favorite : Icons.favorite_border,
          color: like ? Colors.red : null,
          ),
        onTap: () {
          setState(() {
            if (cnt.isEmpty)
            {
              if (added == false)
              {
                items.add(widget.vid);
                added=true;
                users.doc("user1").update({ // 사용자가 좋아요 버튼을 누르면 좋아요 기록 업데이트
                  "id":"user1",
                  "likehistory": items.toSet().toList(),
                  "viewhistory": viewitems
                  });
                print("added: $items");
              }
            }
                like ? like = false : like = true;
          });
          },
        );


      },
    );


  }
}


// 영상 재생 페이지에 필요한 모든 위젯을 모아놓은 페이지
class VideoPlayer extends StatefulWidget {
  final vid;
  const VideoPlayer({Key key, this.vid}) : super(key: key);
  @override
  _VideoPlayerState createState() => _VideoPlayerState();
}

class _VideoPlayerState extends State<VideoPlayer> {
  @override
  Widget build(BuildContext context) {

    return ListView(
        children: <Widget>[
          Player(vid:widget.vid),
          VideoInfo(vid:widget.vid),
          LikeButtons(vid:widget.vid),
          SummaryList(vid:widget.vid),
        ]
    );
  }
}