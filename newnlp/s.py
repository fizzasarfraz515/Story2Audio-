import grpc
from concurrent import futures
import pyttsx3
import os
import story2audio_pb2
import story2audio_pb2_grpc

class StoryToAudioServicer(story2audio_pb2_grpc.StoryToAudioServicer):
    def GenerateAudio(self, request, context):
        try:
            # Initialize the TTS engine
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)  # Set speech rate (optional)
            engine.setProperty('volume', 1)  # Set volume (optional)
            
            # Set voice based on gender (pyttsx3 default voices)
            voices = engine.getProperty('voices')
            if request.gender == "female":
                engine.setProperty('voice', voices[1].id)  # Female voice
            else:
                engine.setProperty('voice', voices[0].id)  # Male voice

            # Output path for the audio file
            audio_path = "static/audio/output.mp3"
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)

            # Save the generated speech as an audio file
            engine.save_to_file(request.story_text, audio_path)
            engine.runAndWait()  # Ensure the audio is saved

            # Return success response with the audio URL
            return story2audio_pb2.AudioResponse(
                status="SUCCESS",
                audio_url=f"http://localhost:8000/{audio_path}",
                error=""
            )
        except Exception as e:
            return story2audio_pb2.AudioResponse(
                status="FAILURE",
                audio_url="",
                error=str(e)
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    story2audio_pb2_grpc.add_StoryToAudioServicer_to_server(StoryToAudioServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Server running on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
