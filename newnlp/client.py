import grpc
import story2audio_pb2
import story2audio_pb2_grpc

channel = grpc.insecure_channel('localhost:50052')
stub = story2audio_pb2_grpc.StoryToAudioStub(channel)
response = stub.GenerateAudio(story2audio_pb2.AudioRequest(
    story_text="Once upon a time...",
    accent="us",
    gender="female"
))
print("Status:", response.status)
print("Audio URL:", response.audio_url)