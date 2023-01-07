import 'package:flutter/material.dart';
import "video_player.dart";
import "summary.dart";


// 영상 플레이어 위젯
class VideoMain extends StatefulWidget {
  final vid;
  const VideoMain({Key key, this.vid}) : super(key: key);
  @override
  _VideoMainState createState() => _VideoMainState();
}

class _VideoMainState extends State<VideoMain> {
  @override
  Widget build(BuildContext context) {
    final title = 'YouTube Lectures List';

    return Scaffold(
      appBar: AppBar(title: Text("Video"),backgroundColor: Colors.red,),
      body:
      VideoPlayer(vid:widget.vid),
    );
  }
}