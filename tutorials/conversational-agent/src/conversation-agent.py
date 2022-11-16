import random
import time
import speech_recognition as sr
import pyttsx3

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["Transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    return response

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        return response.query_result.fulfillment_text

if __name__ == '__main__':
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    engine = pyttsx3.init()
    engine.setProperty('rate', 120)     # setting up new voice rate
    
    PROJECT_ID = 'smarttrashcan-wbmh'
    SESSION_ID = '1235'
    LANGUAGE_CODE = 'en-US'
    

    while True:
        print("Say something into the mic")
        guess = recognize_speech_from_mic(recognizer, microphone)
        # print(guess)
        print("Processing.....")
        if guess["error"] is None:
            text = guess["Transcription"]
            print(text)
            # print(type(text))
            text = [text]
            result = detect_intent_texts(PROJECT_ID, SESSION_ID, text, LANGUAGE_CODE)
            print(result)
            engine.say(result)
            engine.runAndWait()
        