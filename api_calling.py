from google import genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import io

# loading the environment variable
load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY")

#initializing a client
client = genai.Client(api_key = my_api_key)

#note generator
def note_generator(images):
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[images,"Summarize the picture in note format at max 100 words, make sure to add necessary markdown to differentiate different section"]
    )
    return response.text

#audio transcript
def audio_transcript(text):
    speech = gTTS(text, lang='en', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer

#quiz generator
def quiz_generator(images, difficulty):
    prompt = f"Generate 3 quizzes based on the {difficulty}. Make sure to add a markdown to differentiate the options. Add the correct answers at the end of the quiz with the heading 'Answer Key'"
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[*images, prompt]
    )
    return response.text
