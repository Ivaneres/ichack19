import 'package:flutter/material.dart';
import 'package:speech_recognition/speech_recognition.dart';

void main() => runApp(MyApp());

SpeechRecognition _speech = new SpeechRecognition();

  void activateSpeechRecognizer() {
    print('_MyAppState.activateSpeechRecognizer... ');
    _speech = new SpeechRecognition();
    _speech.setAvailabilityHandler(onSpeechAvailability);
    _speech.setCurrentLocaleHandler(onCurrentLocale);
    _speech.setRecognitionStartedHandler(onRecognitionStarted);
    _speech.setRecognitionResultHandler(onRecognitionResult);
    _speech.setRecognitionCompleteHandler(onRecognitionComplete);
    _speech
        .activate()
        .then((res) => setState(() => _speechRecognitionAvailable = res));
  }

void start() {
  activateSpeechRecognizer();
}

class MyApp extends StatelessWidget {
  SpeechRecognition _speech;

  String transcript = "";

  String lang = "en_US";



  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MadTunez',
      home: Scaffold(
        body: Center(
          child: Text('Hello World'),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: start,
        ),
      ),
    );
  }
}