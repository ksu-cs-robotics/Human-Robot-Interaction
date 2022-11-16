import uuid

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
        print(response)
        return response.query_result.fulfillment_text

if __name__ == "__main__":
    PROJECT_ID = 'smarttrashcan-wbmh'
    SESSION_ID = '1234'
    LANGUAGE_CODE = 'en-US'
    print('Sample conversation agent') 
    print('Enter your messages, enter \'quit\' at any time to quit')

    while True:
        user_expression = input(">>> ")
        if user_expression == 'quit':
            break
        user_expression = [user_expression]
        result = detect_intent_texts(PROJECT_ID, SESSION_ID, user_expression, LANGUAGE_CODE)
        print(result)
