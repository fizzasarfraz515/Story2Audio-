from flask import Flask, render_template, request
from gtts import gTTS
import os

app = Flask(__name__)

# Function to generate audio using gTTS
def generate_audio(story_text, accent, gender, emotion, age_group):
    # Language mapping for gTTS (using English as default)
    language = 'en'
    
    # You can customize the language based on accent, but gTTS doesn't directly support accents.
    # We are using 'en' for now. You can extend this later if needed.
    if accent == "us":
        language = 'en'
    elif accent == "uk":
        language = 'en'
    elif accent == "aus":
        language = 'en'
    elif accent == "indian":
        language = 'en'

    # Create the TTS object with the selected language
    tts = gTTS(text=story_text, lang=language, slow=False)
    
    # Define the output file path
    output_path = "static/audio/gradio_output.mp3"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the audio to the specified path
    tts.save(output_path)
    
    # Return the audio file path (Flask will serve this file)
    return output_path

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_audio_route():
    story_text = request.form['story_text']
    accent = request.form['accent']
    gender = request.form['gender']
    emotion = request.form['emotion']
    age_group = request.form['age_group']

    audio_url = generate_audio(story_text, accent, gender, emotion, age_group)
    return render_template("index.html", audio_url=audio_url)

if __name__ == '__main__':
    app.run(debug=True)
