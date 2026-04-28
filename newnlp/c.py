import grpc
import story2audio_pb2
import story2audio_pb2_grpc

def generate_audio(story_text, accent, gender):
    channel = grpc.insecure_channel('localhost:50052')
    stub = story2audio_pb2_grpc.StoryToAudioStub(channel)

    response = stub.GenerateAudio(story2audio_pb2.AudioRequest(
        story_text=story_text,
        accent=accent,
        gender=gender
    ))

    if response.status == "SUCCESS":
        print("Audio generated successfully!")
        print(f"Audio URL: {response.audio_url}")
    else:
        print(f"Error generating audio: {response.error}")

if __name__ == "__main__":
    story_text = "Once upon a time..."
    accent = "us"
    gender = "female"

    generate_audio(story_text, accent, gender)
