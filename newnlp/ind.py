<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Story to Audio Generator</title>
    <script src="https://cdn.jsdelivr.net/npm/wavesurfer.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .form-control {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            font-size: 16px;
        }
        #waveform {
            width: 100%;
            height: 200px;
            margin-top: 20px;
            background-color: #eee;
        }
        #audioControls {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Story to Audio Generator</h1>
        <form id="audioForm">
            <textarea class="form-control" id="story_text" placeholder="Enter your story..." rows="5"></textarea>
            <select class="form-control" id="accent">
                <option value="us">US</option>
                <option value="uk">UK</option>
                <option value="aus">Australia</option>
                <option value="indian">Indian</option>
            </select>
            <select class="form-control" id="gender">
                <option value="female">Female</option>
                <option value="male">Male</option>
            </select>
            <button type="submit" class="form-control" style="background-color: #4CAF50; color: white;">Generate Audio</button>
        </form>

        <div id="waveform"></div>

        <div id="audioControls" style="display: none;">
            <audio id="audioPlayer" controls>
                <source id="audioSource" src="" type="audio/mp3">
            </audio>
        </div>
    </div>

    <script>
        document.getElementById("audioForm").addEventListener("submit", function (event) {
            event.preventDefault();
            let storyText = document.getElementById("story_text").value;
            let accent = document.getElementById("accent").value;
            let gender = document.getElementById("gender").value;

            // Make an AJAX request to generate the audio
            fetch("/generate", {
                method: "POST",
                body: new FormData(document.getElementById("audioForm"))
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                // Set the audio source
                let audioPlayer = document.getElementById("audioPlayer");
                let audioSource = document.getElementById("audioSource");
                audioSource.src = data.audio_url;
                audioPlayer.load();

                // Show the audio player and play button
                document.getElementById("audioControls").style.display = "block";

                // Initialize Waveform using wavesurfer.js
                let wavesurfer = WaveSurfer.create({
                    container: '#waveform',
                    waveColor: 'violet',
                    progressColor: 'purple',
                    height: 150,
                    barWidth: 2,
                    barHeight: 1,
                    barGap: 3
                });

                // Load the audio and create the waveform
                wavesurfer.load(data.audio_url);

                // Play audio when the user clicks on the play button
                audioPlayer.play();
            })
            .catch(error => {
                alert("An error occurred while generating the audio.");
            });
        });
    </script>
</body>
</html>
