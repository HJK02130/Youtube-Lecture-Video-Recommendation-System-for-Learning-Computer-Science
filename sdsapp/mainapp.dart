import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'list(mypage).dart';
import 'list.dart';
import 'list2.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';

void main() async  {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var _index = 0; //_index : 페이지 인덱스 0, 1, 2
  var _pages = [
    Page1(),
    Page2(),
    Page3()
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.red, //제목 배경색
        title: Text('강추: 강의영상 추천 시스템'), //제목

      ),
      body:
      _pages[_index],
      bottomNavigationBar: BottomNavigationBar(
        onTap: (index) {
          setState(() {
            _index = index; // 선택된 탭의 인덱스로 _index를 변경
          });
        },
        currentIndex: _index,
        items: <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            title: Text('Persoanl rcmd'),
            icon: Icon(Icons.person),
          ),
          BottomNavigationBarItem(
            title: Text('Category rcmd'),
            icon: Icon(Icons.category),
          ),
          BottomNavigationBarItem(
            title: Text('MY'),
            icon: Icon(Icons.account_circle),
          ),
        ],
      ),
    );
  }
}

// 사용자가 이전에 시청한 영상 데이터 기반 추천 영상을 보여주는 페이지
class Page1 extends StatefulWidget {
  @override
  _Page1State createState() => _Page1State();
}

class _Page1State extends State<Page1> {
  @override
  Widget build(BuildContext context) {
    final title = 'YouTube Lectures List';

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: title,
      home: Scaffold(
        body: ListView(
          children: <Widget>[
            // 시청 기록 기반 추천 영상 리스트 출력
            Container(child:Text("  Recommendation by History", style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.4),),margin: EdgeInsets.only(top: 15.0, bottom:10)),
            Hlist(page: 0, i: "byhistory",),
            // 영상 썸네일 기반 추천 영상 리스트 출력
            Container(child:Text("  Recommendation by Thumbnail", style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.4),),margin: EdgeInsets.only(bottom: 10),),
            Hlist(page: 0, i: "bythumbnail" ),
            // 영상 제목 기반 추천 영상 리스트 추천
            Container(child:Text(" Recommendation by Title", style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.4),),margin: EdgeInsets.only(bottom: 10),),
            Hlist(page: 0, i: "bytitle",),
          ],
        ),
      ),
    );
  }
}

// 사용자가 이전에 시청한 영상의 카테고리 기반 추천 영상을 보여주는 페이지
class Page2 extends StatefulWidget {
  @override
  _Page2State createState() => _Page2State();
}

class _Page2State extends State<Page2> {
  @override
  Widget build(BuildContext context) {
    final title = 'YouTube Lectures List';

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: title,
      home: Scaffold(
        body: StreamBuilder(
          stream: FirebaseFirestore.instance.collection("user").snapshots(),
          builder: (context, snapshot){
            List<QueryDocumentSnapshot> l = snapshot.data.docs.reversed.toList();
            var idx = l.indexWhere((element) => element.data()["id"] == "user1");
            var item = snapshot.data.docs[idx].data()["viewhistory"].last;
                return ListView(
                  children: <Widget>[
                    // 카테고리에서 상위 조회수 영상 리스트 출력
                    Hlist2(page: 0, i: item,),
                    // 카테고리에서 상위 좋아요 영상 리스트 출력
                    Hlist2(page: 1, i: item,),
                    // 카테고리에서 최근에 업로드된 영상 리스트 출력
                    Hlist2(page: 2, i: item,),
                  ],
                );
          }
        ),
      ),
    );
  }
}

// 시청 기록, 좋아요 기록을 볼 수 있는 페이지
class Page3 extends StatefulWidget {
  @override
  _Page3State createState() => _Page3State();
}

class _Page3State extends State<Page3> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body:
      ListView(
        scrollDirection: Axis.vertical,
        children: <Widget>[
          SizedBox(
            height:40,
          ),
          Row(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Align(
                alignment: Alignment.topLeft,
                child: CircleAvatar(
                  child: Icon(Icons.person),
                ),
              ),
              Text('  user', style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 2.0)),
            ],
          ),
          SizedBox(
            height:40,
          ),
          ListTile(
            leading:Icon(Icons.restore, size: 35),
            title: Text('시청기록', style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.4)),
            trailing:Icon(Icons.navigate_next),
            onTap:() {
              Navigator.push( // 시청기록 페이지로 이동하는 Navigator
                context,
                MaterialPageRoute( 
                  builder: (context) => ViewHistoryPage(),
                ),
              );
              //이벤트 함수
            },
          ),
          SizedBox(
            height:10,
          ),
          ListTile(
            leading:Icon(Icons.favorite, size: 35),
            title: Text('좋아요를 누른 영상', style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.4)),
            trailing:Icon(Icons.navigate_next),
            onTap:() {
              Navigator.push( // 좋아요 기록 페이지로 이동하는 Navigator
                context,
                MaterialPageRoute(
                  builder: (context) => LikePage(),
                ),
              );
              //이벤트 함수
            },
          ),
        ],
      ),
    );
  }
}

class ViewHistoryPage extends StatefulWidget {
  @override
  _ViewHistoryPageState createState() => _ViewHistoryPageState();
}

class _ViewHistoryPageState extends State<ViewHistoryPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.red, //제목 배경색
        title: Text('시청기록'), //제목
        centerTitle: true,
      ),
      body: ListView(
        children: <Widget>[
          Mlist(theme:"viewhistory"), // 사용자의 시청기록을 보여주는 위젯
        ],
      ),
    );
  }
}

class LikePage extends StatefulWidget {
  @override
  _LikePageState createState() => _LikePageState();
}

class _LikePageState extends State<LikePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.red, //제목 배경색
        title: Text('좋아요를 누른 영상'), //제목
        centerTitle: true,
      ),
      body: ListView(
        children: <Widget>[
          Mlist(theme: "likehistory"), // 사용자의 좋아요 기록을 보여주는 위젯
        ],
      ),
    );
  }
}