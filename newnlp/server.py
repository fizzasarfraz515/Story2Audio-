import grpc
from concurrent import futures
from gtts import gTTS
import os
import story2audio_pb2
import story2audio_pb2_grpc

class StoryToAudioServicer(story2audio_pb2_grpc.StoryToAudioServicer):
    def GenerateAudio(self, request, context):
        try:
            # Use gTTS to generate speech from the provided text
            tts = gTTS(text=request.story_text, lang='en')
            audio_path = "static/audio/output.mp3"
            
            # Make sure the directory exists
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            # Save the audio as an MP3 file
            tts.save(audio_path)
            
            # Return the success response with the audio URL
            return story2audio_pb2.AudioResponse(
                status="SUCCESS",
                audio_url=f"http://localhost:8000/{audio_path}",
                error=""
            )
        except Exception as e:
            # Handle errors and return failure response
            return story2audio_pb2.AudioResponse(
                status="FAILURE",
                audio_url="",
                error=str(e)
            )

def serve():
    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    story2audio_pb2_grpc.add_StoryToAudioServicer_to_server(StoryToAudioServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Server running...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
