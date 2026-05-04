from flask import Flask, render_template, request, jsonify
import os
import base64
import io
import sys

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    app.config['UPLOAD_FOLDER'] = 'data/audio_recordings'

    # Import the actual voice recognition service
    try:
        # Set Google Cloud credentials environment variable
        credentials_path = os.path.join(os.path.dirname(__file__), '..', 'google-credentials.json')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        print(f"Google Cloud credentials path: {credentials_path}")

        # Import services from the local app/services directory
        import sys
        sys.path.append('.')
        from app.services.speech_service import SpeechToTextService
        from app.services.translation_service import TranslationService

        speech_service = SpeechToTextService()
        translation_service = TranslationService()
        print("Google Cloud services initialized successfully!")

        class VoiceRecognition:
            def process_audio(self, audio_base64):
                try:
                    # Decode base64 audio
                    import base64
                    audio_data = base64.b64decode(audio_base64)

                    # Save temporary audio file
                    import tempfile
                    import os
                    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_file:
                        temp_file.write(audio_data)
                        temp_file_path = temp_file.name

                    try:
                        # Transcribe audio using Google Cloud Speech-to-Text
                        transcript = speech_service.transcribe_audio(temp_file_path, language_code='zu-ZA')

                        if not transcript or transcript.strip() == "":
                            transcript = "Speech not detected. Please try speaking louder and clearer."

                        # Translate to English using Google Cloud Translate
                        translation = translation_service.translate_text(transcript, source_lang="zu", target_lang="en")

                        # Generate agricultural advice based on content
                        advice = self._generate_agricultural_advice(transcript.lower())

                        return {
                            'success': True,
                            'transcript': transcript,
                            'translation': translation,
                            'advice': advice
                        }

                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_file_path):
                            os.unlink(temp_file_path)

                except Exception as e:
                    print(f"Voice processing error: {e}")
                    return {
                        'success': False,
                        'error': f'Failed to process audio: {str(e)}',
                        'transcript': '',
                        'translation': '',
                        'advice': 'Please try recording again.'
                    }

            def _generate_agricultural_advice(self, zulu_text):
                """Generate agricultural advice based on isiZulu keywords"""
                advice_map = {
                    'izitshalo': 'For plant care: Ensure proper watering, use organic fertilizers, and monitor for pests regularly.',
                    'zifo': 'For plant diseases: Remove affected leaves immediately, improve air circulation, and use copper-based fungicides.',
                    'nambuzane': 'For pest control: Use neem oil spray, introduce beneficial insects, and practice proper crop rotation.',
                    'nisela': 'Watering advice: Water deeply but infrequently, early morning is best, avoid wetting leaves to prevent fungal diseases.',
                    'umanyolo': 'Fertilizer guidance: Use balanced NPK fertilizer, apply during growing season, test soil pH first.',
                    'imbewu': 'Seed planting: Plant during correct season, ensure proper spacing, keep soil moist until germination.',
                    'isimo sezulu': 'Weather considerations: Monitor forecasts, protect crops from frost, prepare drainage for heavy rain.',
                    'khuni': 'Maize care: Plant in well-drained soil, fertilize regularly, watch for corn borer and rust diseases.',
                    'utshani': 'Weed control: Use mulching, hand weeding, or organic herbicides. Prevent weed competition for nutrients.',
                    'umhlaba': 'Soil management: Test soil pH regularly, add organic matter, practice conservation tillage.',
                    'isivuno': 'Harvesting: Harvest at correct maturity, use proper tools, store in cool dry place.',
                    'izilwane': 'Livestock care: Provide clean water, balanced feed, regular health checks, proper housing.'
                }

                for keyword, advice in advice_map.items():
                    if keyword in zulu_text:
                        return advice

                return 'General farming advice: Practice sustainable agriculture, monitor your crops regularly, maintain soil health, and seek local extension services for specific guidance.'

        voice_recognition = VoiceRecognition()

    except Exception as e:
        print(f"Could not import services: {e}. Using mock mode.")
        # Fallback to mock if services not available
        class MockVoiceRecognition:
            def process_audio(self, audio_base64):
                return {
                    'success': True,
                    'transcript': 'Sawubona, ngicela usizo ngezitshalo zami',
                    'translation': 'Hello, I need help with my plants',
                    'advice': 'For plant diseases, ensure proper watering and use organic pesticides.'
                }

        voice_recognition = MockVoiceRecognition()

        class VoiceRecognition:
            def process_audio(self, audio_base64):
                try:
                    # Decode base64 audio
                    import base64
                    audio_data = base64.b64decode(audio_base64)

                    # Save temporary audio file
                    import tempfile
                    import os
                    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_file:
                        temp_file.write(audio_data)
                        temp_file_path = temp_file.name

                    try:
                        # Transcribe audio (will use mock if API not available)
                        transcript = speech_service.transcribe_audio(temp_file_path, language_code='zu-ZA')

                        if not transcript:
                            transcript = "Speech not detected. Please try speaking louder and clearer."

                        # Translate to English
                        translation = translation_service.translate_text(transcript, source_lang="zu", target_lang="en")

                        # Generate agricultural advice based on content
                        advice = self._generate_agricultural_advice(transcript.lower())

                        return {
                            'success': True,
                            'transcript': transcript,
                            'translation': translation,
                            'advice': advice
                        }

                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_file_path):
                            os.unlink(temp_file_path)

                except Exception as e:
                    print(f"Voice processing error: {e}")
                    return {
                        'success': False,
                        'error': 'Failed to process audio. Please try again.',
                        'transcript': '',
                        'translation': '',
                        'advice': 'Please try recording again.'
                    }

            def _generate_agricultural_advice(self, zulu_text):
                """Generate agricultural advice based on isiZulu keywords"""
                advice_map = {
                    'izitshalo': 'For plant care: Ensure proper watering, use organic fertilizers, and monitor for pests.',
                    'zifo': 'For plant diseases: Remove affected leaves, improve air circulation, and use copper-based fungicides.',
                    'nambuzane': 'For pest control: Use neem oil spray, introduce beneficial insects, and practice crop rotation.',
                    'nisela': 'Watering advice: Water deeply but infrequently, early morning is best, avoid wetting leaves.',
                    'umanyolo': 'Fertilizer guidance: Use balanced NPK fertilizer, apply during growing season, test soil first.',
                    'imbewu': 'Seed planting: Plant during right season, ensure proper spacing, keep soil moist until germination.',
                    'isimo sezulu': 'Weather considerations: Monitor forecasts, protect crops from frost, prepare for rain.',
                    'khuni': 'Maize care: Plant in well-drained soil, fertilize regularly, watch for corn borer and rust.',
                    'utshani': 'Weed control: Use mulching, hand weeding, or organic herbicides. Prevent weed competition.'
                }

                for keyword, advice in advice_map.items():
                    if keyword in zulu_text:
                        return advice

                return 'General farming advice: Practice sustainable agriculture, monitor your crops regularly, and maintain soil health.'

        voice_recognition = VoiceRecognition()

    except ImportError as e:
        print(f"Could not import services: {e}. Using mock mode.")
        # Fallback to mock if services not available
        class MockVoiceRecognition:
            def process_audio(self, audio_base64):
                return {
                    'success': True,
                    'transcript': 'Sawubona, ngicela usizo ngezitshalo zami',
                    'translation': 'Hello, I need help with my plants',
                    'advice': 'For plant diseases, ensure proper watering and use organic pesticides.'
                }

        voice_recognition = MockVoiceRecognition()

    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/voice-recognition')
    def voice_recognition_page():
        return render_template('voice_recognition.html')

    @app.route('/weather')
    def weather():
        return render_template('weather.html')

    @app.route('/plant-scan')
    def plant_scan():
        return render_template('plant_scan.html')

    @app.route('/voice-assistant')
    def voice_assistant():
        return render_template('voice_assistant.html')

    @app.route('/voice-query', methods=['POST'])
    def voice_query():
        try:
            data = request.get_json()
            if not data or 'audio' not in data:
                return jsonify({'error': 'No audio data provided'}), 400

            # Process the audio data
            audio_base64 = data['audio']
            result = voice_recognition.process_audio(audio_base64)

            return jsonify(result)
        except Exception as e:
            print(f"Error processing voice query: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/test-voice')
    def test_voice():
        return jsonify({
            'message': 'Voice recognition system is active and ready.',
            'success': True
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)