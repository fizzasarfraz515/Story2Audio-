from flask import Flask, render_template, request
import grpc
import story2audio_pb2
import story2audio_pb2_grpc

app = Flask(__name__)

# Function to generate audio using gRPC
def generate_audio(story_text, accent, gender):
    # Create a gRPC channel and stub
    channel = grpc.insecure_channel('localhost:50052')
    stub = story2audio_pb2_grpc.StoryToAudioStub(channel)

    # Send a request to the gRPC server
    response = stub.GenerateAudio(story2audio_pb2.AudioRequest(
        story_text=story_text,
        accent=accent,
        gender=gender
    ))

    if response.status == "SUCCESS":
        return response.audio_url
    else:
        return None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_audio_route():
    story_text = request.form['story_text']
    accent = request.form['accent']
    gender = request.form['gender']

    audio_url = generate_audio(story_text, accent, gender)
    return render_template("index.html", audio_url=audio_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
