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

recognition.onstart = function() { 
  console.log('Voice recognition activated. Try speaking into the microphone.');
}

recognition.onspeechend = function() {
  console.log('You were quiet for a while so voice recognition turned itself off.');
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
      } else {
          interim_transcript += event.results[i][0].transcript;
      }
  }

  // Choose which result may be useful for you

  console.log("Interim: ", interim_transcript);

  console.log("Final: ",final_transcript);

  console.log("Simple: ", event.results[0][0].transcript);
}