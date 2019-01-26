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

Track getTrack(String lyrics) {
  var uri = Uri("http", )
}