const textToRead = document.getElementById('textContainer').innerText;
const button = document.getElementById('readButton');
let isReading = false;
const synth = window.speechSynthesis;
let utterance = new SpeechSynthesisUtterance(textToRead);

button.addEventListener('click', () => {
    if (!isReading) {
        synth.speak(utterance);
        button.classList.toggle('bg-light');
        isReading = true;
    } else {
        synth.cancel();
        button.classList.toggle('bg-light');
        isReading = false;
    }
});

// Reset button text when speech ends
utterance.onend = () => {
    // button.textContent = 'Start Reading';
    button.classList.toggle('bg-light');
    isReading = false;
};

document.getElementById('voiceAssistantButton').onclick = function () {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Your browser does not support speech recognition. Please try Google Chrome.');
        return;
    }

    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = function () {
        console.log('Voice recognition started. Speak into the microphone.');
    };

    recognition.onresult = function (event) {
        var transcript = event.results[0][0].transcript.toLowerCase().trim();
        console.log('You said: ' + transcript);
        fetch('/voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: transcript })
        })
            .then(response => {
                if (response.ok) {
                    window.location.href = response.url;
                } else {
                    console.error('Error navigating:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error navigating:', error);
            });
    };

    recognition.onerror = function (event) {
        console.error('Error occurred in recognition: ' + event.error);
    };

    recognition.onend = function () {
        console.log('Voice recognition ended.');
    };

    recognition.start();
};
