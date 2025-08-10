// static/recorder.js
let mediaRecorder;
let audioChunks = [];

function startRecording(duration, callback) {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                callback(audioBlob);
                stream.getTracks().forEach(track => track.stop()); // Stop the stream
            };
            
            mediaRecorder.start();
            setTimeout(() => {
                mediaRecorder.stop();
            }, duration * 1000); // Stop after specified duration (in seconds)
        })
        .catch(err => {
            alert('Error accessing microphone: ' + err.message);
        });
}

function uploadAudio(blob, formId) {
    const formData = new FormData(document.getElementById(formId));
    formData.set('audio_file', blob, 'recorded_audio.wav'); // Replace file input with recorded audio
    
    fetch(formId === 'trainForm' ? '/' : '/verify', {
        method: 'POST',
        body: formData
    }).then(response => response.text())
      .then(html => {
          document.open();
          document.write(html);
          document.close();
      });
}

// Event listeners for training page
document.addEventListener('DOMContentLoaded', () => {
    const trainRecordBtn = document.getElementById('recordTrain');
    if (trainRecordBtn) {
        trainRecordBtn.addEventListener('click', () => {
            startRecording(15, (blob) => uploadAudio(blob, 'trainForm'));
        });
    }

    const verifyRecordBtn = document.getElementById('recordVerify');
    if (verifyRecordBtn) {
        verifyRecordBtn.addEventListener('click', () => {
            startRecording(3, (blob) => uploadAudio(blob, 'verifyForm'));
        });
    }
});