import os
import pyttsx3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_audio(text, accent, gender):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Simple gender-based voice selection
        if gender == "female" and len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        else:
            engine.setProperty('voice', voices[0].id)

        engine.setProperty('rate', 150)

        audio_path = 'static/audio/output.wav'
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        engine.save_to_file(text, audio_path)
        engine.runAndWait()

        return audio_path
    except Exception as e:
        print("Error generating audio:", e)
        return None

@app.route('/')
def index():
    return render_template('ind.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('story_text', '').strip()
    accent = request.form.get('accent', 'us')
    gender = request.form.get('gender', 'Select')

    if not text:
        return jsonify({'error': 'Story text cannot be empty.'})

    audio_file = generate_audio(text, accent, gender)
    if not audio_file:
        return jsonify({'error': 'Failed to generate audio.'})

    return jsonify({'audio_url': '/' + audio_file})

if __name__ == '__main__':
    app.run(debug=True)
