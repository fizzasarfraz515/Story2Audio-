import unittest
from gradio_app import app

class FlaskTestCase(unittest.TestCase):
    
    # Setting up a test client for Flask
    def setUp(self):
        self.client = app.test_client()
    
    # Test the index route
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Story to Audio Generator", response.data)
    
    # Test the audio generation functionality
    def test_generate_audio(self):
        response = self.client.post('/generate', data={
            'story_text': 'Once upon a time...',
            'accent': 'us',
            'gender': 'female',
            'emotion': 'happy',
            'age_group': 'adult'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"audio/mpeg", response.data)

if __name__ == '__main__':
    unittest.main()
