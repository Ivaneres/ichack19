import 'package:flutter/material.dart';
import 'package:speech_recognition/speech_recognition.dart';
import 'package:permission_handler/permission_handler.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

enum ListeningState { Waiting, Listening, Playing }

class _MyHomePageState extends State<MyHomePage> {
  var state = ListeningState.Waiting;
  SpeechRecognition _speech;

  bool _speechRecognitionAvailable = false;
  String transcription = '';

  String _currentLocale = 'en_US';

  @override
  initState() {
    super.initState();
//    _checkAudioPermission();

    Map<PermissionGroup, PermissionStatus> permissions = await PermissionHandler().requestPermissions([PermissionGroup.speech]);
    activateSpeechRecognizer();
  }

//
//  void _checkAudioPermission() async {
//    bool hasPermission =
//    await SimplePermissions.checkPermission(Permission.RecordAudio);
//    if (!hasPermission) {
//      await SimplePermissions.requestPermission(Permission.RecordAudio);
//    }
//  }
//  void errorHandler() => activateSpeechRecognizer();

  // Platform messages are asynchronous, so we initialize in an async method.
  void activateSpeechRecognizer() {
    print('_MyAppState.activateSpeechRecognizer... ');
    _speech = new SpeechRecognition();
    _speech.setAvailabilityHandler(onSpeechAvailability);
//    _speech.setCurrentLocaleHandler(onCurrentLocale);
    _speech.setRecognitionStartedHandler(onRecognitionStarted);
    _speech.setRecognitionResultHandler(onRecognitionResult);
    _speech.setRecognitionCompleteHandler(onRecognitionComplete);
    _speech
        .activate()
        .then((res) => setState(() => _speechRecognitionAvailable = res));
    _speech.setErrorHandler(errorHandler);
  }

  void errorHandler() => activateSpeechRecognizer();

  void onSpeechAvailability(bool result) =>
      setState(() => _speechRecognitionAvailable = result);

  void onRecognitionStarted() =>
      setState(() => state = ListeningState.Listening);

  void onRecognitionResult(String text) => setState(() => transcription = text);

  void onRecognitionComplete(String text) {
    transcription = text;
    setState(() => state = ListeningState.Waiting);
  }

  // TODO play stuff lol

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: new Padding(
          padding: new EdgeInsets.all(8.0),
          child: new Center(
            child: new Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                new Expanded(
                    child: new Container(
                        padding: const EdgeInsets.all(8.0),
                        color: Colors.grey.shade200,
                        child: new Text(transcription))),
                _buildButton(
                  onPressed: _speechRecognitionAvailable &&
                      state != ListeningState.Listening
                      ? () => start()
                      : null,
                  label: state == ListeningState.Listening
                      ? 'Listening...'
                      : 'Listen',
                ),
                _buildButton(
                  onPressed:
                  state == ListeningState.Listening ? () => cancel() : null,
                  label: 'Cancel',
                ),
                _buildButton(
                  onPressed:
                  state == ListeningState.Listening ? () => stop() : null,
                  label: 'Stop',
                ),
              ],
            ),
          )),
    );
  }

  void start() =>
      _speech
          .listen(locale: _currentLocale)
          .then((result) => print('_MyAppState.start => result $result'));

  void cancel() =>
      _speech
          .cancel()
          .then((result) => setState(() => state = ListeningState.Waiting));

  void stop() =>
      _speech.stop().then((result) {
        setState(() => state = ListeningState.Waiting);
      });

  Widget _buildButton({String label, VoidCallback onPressed}) =>
      new Padding(
          padding: new EdgeInsets.all(12.0),
          child: new RaisedButton(
            color: Colors.cyan.shade600,
            onPressed: onPressed,
            child: new Text(
              label,
              style: const TextStyle(color: Colors.white),
            ),
          ));
}
