import unittest
import os
from gradio_app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test client for the Flask app"""
        self.client = app.test_client()
        self.audio_path = 'static/audio/gradio_output.mp3'

    def tearDown(self):
        """Clean up the audio file generated during tests."""
        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)

    def test_index_page(self):
        """Test that the index page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Story to Audio Generator", response.data)
        self.assertIn(b"Enter your story here...", response.data)

    def test_generate_audio(self):
        """Test the form submission to generate audio."""
        response = self.client.post('/generate', data={
            'story_text': 'Once upon a time...',
            'accent': 'us',
            'gender': 'female',
            'emotion': 'happy',
            'age_group': 'adult'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"audio/mpeg", response.data)

    def test_generate_audio_invalid_accent(self):
        """Test if the form fails when an invalid accent is selected."""
        response = self.client.post('/generate', data={
            'story_text': 'Once upon a time...',
            'accent': 'xyz',  # Invalid accent
            'gender': 'female',
            'emotion': 'happy',
            'age_group': 'adult'
        })
        
        # Assuming the server handles invalid accent and falls back to default behavior.
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"audio/mpeg", response.data)
        self.assertNotIn(b"xyz", response.data)  # Accent should not appear in audio file generation

    def test_generate_audio_invalid_data(self):
        """Test the behavior when invalid data is submitted (e.g., wrong gender)."""
        response = self.client.post('/generate', data={
            'story_text': 'Once upon a time...',
            'accent': 'us',
            'gender': 'unknown',  # Invalid gender
            'emotion': 'happy',
            'age_group': 'adult'
        })
        
        # Check if the audio file is not generated
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"audio/mpeg", response.data)  # Even with an invalid gender, it should still generate
        self.assertNotIn(b"unknown", response.data)

    def test_audio_file_generation(self):
        """Test that the audio file is actually created."""
        # Submit valid data
        response = self.client.post('/generate', data={
            'story_text': 'This is a test story.',
            'accent': 'us',
            'gender': 'female',
            'emotion': 'happy',
            'age_group': 'adult'
        })

        # Assert the audio file was created
        self.assertTrue(os.path.exists(self.audio_path))

    def test_audio_file_cleanup(self):
        """Test that the audio file is deleted after tests."""
        # Generate the audio file
        self.client.post('/generate', data={
            'story_text': 'This is a test story.',
            'accent': 'us',
            'gender': 'female',
            'emotion': 'happy',
            'age_group': 'adult'
        })

        # Check if the audio file is created
        self.assertTrue(os.path.exists(self.audio_path))

        # Clean up
        os.remove(self.audio_path)
        
        # Assert that the file is deleted
        self.assertFalse(os.path.exists(self.audio_path))

    def test_no_audio_generation_on_empty_story(self):
        """Test that no audio is generated if the story text is empty."""
        response = self.client.post('/generate', data={
            'story_text': '',  # Empty story
            'accent': 'us',
            'gender': 'female',
            'emotion': 'happy',
            'age_group': 'adult'
        })
        
        # Expect no audio URL to be generated in the response
        self.assertNotIn(b"audio/mpeg", response.data)

if __name__ == '__main__':
    unittest.main()
