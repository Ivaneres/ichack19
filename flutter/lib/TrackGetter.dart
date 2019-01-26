import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

class Track {
  final String artistName;
  final String songName;

  Track({this.artistName, this.songName});

  factory Track.fromJson(Map<String, dynamic> json) {
    return Track(
      artistName: json['artistName'],
      songName: json['songName'],
    );
  }
}

Future<Track> getTrack(String lyrics) async {
  var resp = await http.post(
      "https://singaroke.herokuapp.com/", body: {"lyrics": lyrics});
  var decoded = jsonDecode(resp.body);
  return Track.fromJson(decoded);}

