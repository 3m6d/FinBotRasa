import openai 

from rasa_sdk import Action 


openai.api_key = "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"  # Replace with your actual API key



class GPT2Action(Action):

    def name(self):

        return "action_gpt2_response"



    def run(self, dispatcher, tracker, domain):

        user_input = tracker.latest_message['text']

        prompt = f"User: {user_input} \n Bot:"  # Construct the prompt with context

        response = openai.Completion.create( 

            engine="text-davinci-003",  # Choose the GPT-2 model

            prompt=prompt,

            max_tokens=50

        )

        generated_text = response["choices"][0]["text"]

        dispatcher.utter_message(text=generated_text) 

        return [] 
