try {
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
}
catch(e) {
  console.error(e);
  $('.no-browser-support').show();
  $('.app').hide();
}

function sendApiRequest(s, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
          callback(xmlHttp.responseText);
  }
  xmlHttp.open( "GET", "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + s + "&key=AIzaSyCx_yuFHq28261Q8q7itujyjSKRKhP3UfU&type=video", false ); // false for synchronous request
  xmlHttp.send(null);
}

recognition.onstart = function() { 
  console.log('Voice recognition activated. Try speaking into the microphone.');
  $("#voice-recognition-output").html("Listening...");
}

recognition.onspeechend = function() {
  console.log('You were quiet for a while so voice recognition turned itself off.');
  $("#voice-recognition-output").html("Processing...");
}

recognition.onerror = function(event) {
  if(event.error == 'no-speech') {
    console.log('No speech was detected. Try again.');  
  };
}

recognition.onresult = function(event) {
  var interim_transcript = '';
  var final_transcript = '';

  for (var i = event.resultIndex; i < event.results.length; ++i) {
      // Verify if the recognized text is the last with the isFinal property
      if (event.results[i].isFinal) {
          final_transcript += event.results[i][0].transcript;
          queryLyricServer(final_transcript);
          recognition.stop();
          $('.buttons').fadeOut();
          
      } else {
          interim_transcript += event.results[i][0].transcript;
      }
  }

  // Choose which result may be useful for you

  console.log("Interim: ", interim_transcript);
  document.getElementById("voice-recognition-output").innerHTML = interim_transcript;

  console.log("Final: ",final_transcript);

  console.log("Simple: ", event.results[0][0].transcript);

  if (final_transcript !== "") {
    // queryLyricServer(final_transcript);

  }
}

 queryLyricServer = function(lyrics) {
 // Content-Type: application/json 
 // POST
 // {"lyrics":"string"}
 // https://singaroke.herokuapp.com/
  
   fetch("https://singarokev2.herokuapp.com/", {
            method:"POST",
            headers: {
                "Content-Type": "application/json"},
            body: JSON.stringify({"lyrics":lyrics})
        }).then(response => {return response.json();})
          .then(data => {sendApiRequest(data.artistName + " - " + data.songName + " lyrics", function(obj){
                        document.getElementById("voice-recognition-output").innerHTML = data.songName + " - " + data.artistName;
                        var obj2 = JSON.parse(obj);
                        console.log(obj2);
                        console.log(obj2.items[0].id.videoId);
                        console.log(data.timestamp);
                        document.getElementById("ytplayer").innerHTML = '<iframe width="1200" height="600" src="https://www.youtube.com/embed/' + JSON.parse(obj)["items"][0]["id"]["videoId"] + '?autoplay=1&start=' + (Math.round(data.timestamp) + 5) + '" frameborder="0" allow="autoplay"></iframe>'
          })})
          .catch(err => {
            $("#voice-recognition-output").html("Error - not found :(");
            console.log("Big chungus: " + err);});
 }
