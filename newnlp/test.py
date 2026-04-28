from gtts import gTTS
import os

# Text to convert to speech
text = "Once upon a time"

# Create a gTTS object
tts = gTTS(text=text, lang='en', slow=False)  # slow=False means the speech will be at normal speed

# Save the audio file
output_path = "once_upon_a_time.mp3"
tts.save(output_path)

print(f"Audio content written to {output_path}")
