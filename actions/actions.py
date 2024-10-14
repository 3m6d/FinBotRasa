from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import replicate
import os
from rasa_sdk.events import Restarted
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
import logging
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

class ActionRestart(Action):

    def name(self) -> Text:
      return "action_restart"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

      return [Restarted(), AllSlotsReset()]



class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]




class ValidateAccountOpeningForm(FormValidationAction):
    def name(self) -> Text:
        """
        Returns the name of the validation action.

        Returns:
            str: Name of the validation action.
        """
        return "validate_account_opening_form"
    
    # Extract custom slot for account_type
    async def extract_account_type(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        """
        Validate user's account_type input.

        Check if the user has specified 'demat', 'trading', or 'both' as the account type.
        If not, ask the user to clarify.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user.
            tracker (Tracker): The state tracker for the current user conversation.
            domain (Dict): The bot's domain.

        Returns:
            Dict[Text, Any]: A dictionary with the slot and value of the account_type and both slots.
        """
       
        last_user_message = tracker.latest_message.get("text")

        account_type = None
        if tracker.get_intent_of_latest_message() in ["inform_account_opening"]:

            # Check for account types in the last user message
            if "demat" in last_user_message and "trading" in last_user_message and "both" in last_user_message:
                account_type = "both"
            elif "both" in last_user_message:
                account_type = "both"
            elif "demat" in last_user_message:
                account_type = "demat"
            elif "trading" in last_user_message:
                account_type = "trading"
        
            # Return the identified account type and the 'both' flag
            return {
                "account_type": account_type,
                "both": "both" in last_user_message
            }

        return {"account_type": None, "both": False}       

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict
    ) -> List[Text]:
        additional_slots = ["account_type", "both"]
        # If you want to dynamically modify the required slots, implement the logic here
        return domain_slots
    
    async def extract_definition(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        # Get the latest detected intent
        latest_intent = tracker.get_intent_of_latest_message()

        # Check if the intent is one of the definition-related intents
        if latest_intent in ["define_demat", "define_trading", "define_stock"]:
            # Extract the definition entity (with role 'concept' if applicable)
            definition_entity = next(tracker.get_latest_entity_values("definition", role="concept"), None)
            
            # If an entity was found, return it as a slot
            if definition_entity:
                return {"definition": definition_entity}
        
        # If no entity was found, or it's not a definition intent, return None
        return {"definition": None}



    
class ActionAccountTypeHandle(Action): 
    def name(self) -> Text:
        """
        Returns the name of this action.

        Returns:
            Text: The name of this action
        """
        return "action_account_type_handle"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        """
        Execute the side effects of this action.

        If the account type is set to one of the options, ask a follow-up question
        to the user. If it is not set, ask the user to specify the account type.

        Args:
            dispatcher: The dispatcher which is used to send messages back to the user.
            tracker: The state tracker for the current user.
            domain: The bot's domain

        Returns:
            List of SlotSet events. The account_type slot is set to the value of
            the account type selected by the user.
        """
        if tracker.get_intent_of_latest_message() == "inform_account_opening":
            account_type = tracker.get_slot("account_type")
            last_user_message = tracker.latest_message.get("text")
            
            if "both" in last_user_message or account_type == "both":
                dispatcher.utter_message(response="utter_ask_both_account_opening")
                dispatcher.utter_message(response="utter_ask_demat_account_opening")
                dispatcher.utter_message(response="utter_ask_trading_account_opening")
            elif "demat" in last_user_message or account_type == "demat":
                dispatcher.utter_message(response="utter_ask_demat_account_opening")
            elif "trading" in last_user_message or account_type == "trading":
                dispatcher.utter_message(response="utter_ask_trading_account_opening")
            else:
                dispatcher.utter_message(text="Please specify the account type.")

            return []
