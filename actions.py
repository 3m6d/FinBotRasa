# actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import replicate
import os

class ActionLlamaResponse(Action):
    def name(self) -> Text:
        return "action_llama_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Ensure the Replicate API token is set
        if 'REPLICATE_API_TOKEN' not in os.environ:
            # You can set the API token here, but it's recommended to set it as an environment variable
            os.environ['REPLICATE_API_TOKEN'] = 'your_api_token_here'  # Replace with your API token

        # Get the last user message
        user_message = tracker.latest_message.get('text')

        # Prepare the input for the model
        input_params = {
            "top_p": 1,
            "prompt": user_message,
            "temperature": 0.75,
            "max_new_tokens": 150
        }

        # Run the model using Replicate's API
        try:
            # Get the model
            model = replicate.models.get("meta/llama-2-7b-chat")

            # Run the model and get the output
            output = model.predict(**input_params)

            # The output is a list of strings; concatenate them
            response_text = ''.join(output)

            # Send the response back to the user
            dispatcher.utter_message(text=response_text)

        except Exception as e:
            # Handle exceptions appropriately
            dispatcher.utter_message(text="I'm sorry, I couldn't process your request at the moment.")
            print(f"Error: {e}")

        return []
