from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.constants import TEXT, INTENT, ENTITIES
from rasa.shared.nlu.training_data.message import Message
from typing import Any, Dict, List, Text
import requests
import logging

logger = logging.getLogger(__name__)

#process: This method processes a list of Rasa messages, makes API requests to Wit.ai, and extracts intents and entities, which are then added to each message.
#parse_wit_ai: Sends the input text to Wit.ai's API and receives a response.
#extract_intent: Extracts the highest confidence intent from the Wit.ai response and maps it to a Rasa intent (if a mapping exists).
#extract_entities: Extracts entities from Wit.ai response and maps them to Rasa entities (if mappings exist).


logger = logging.getLogger(__name__)

@DefaultV1Recipe.register(
    component_types=["MessageFeaturizer"],  # This defines what type of component it is
    is_trainable=False                      # Marking it as non-trainable
)
class WitAIComponent(GraphComponent):
    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
            "access_token": None,
            "intent_mappings": {},
            "entity_mappings": {}
        }

    def __init__(
        self,
        config: Dict[Text, Any],
        name: Text,
        resource: Resource,
        model_storage: ModelStorage,
        execution_context: ExecutionContext,
    ) -> None:
        self.access_token = config.get("access_token")
        self.intent_mappings = config.get("intent_mappings", {})
        self.entity_mappings = config.get("entity_mappings", {})
        if not self.access_token:
            raise ValueError("Wit.ai access token must be provided in the config.")

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config, cls.__name__, resource, model_storage, execution_context)

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            text = message.get(TEXT)
            if text:
                response = self.parse_wit_ai(text)
                intent = self.extract_intent(response)
                entities = self.extract_entities(response)

                message.set(INTENT, intent, add_to_output=True)
                message.set(ENTITIES, entities, add_to_output=True)
        return messages

    def parse_wit_ai(self, text: Text) -> Dict[Text, Any]:
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        params = {'q': text}
        try:
            response = requests.get('https://api.wit.ai/message', headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Wit.ai API request failed: {e}")
            return {}

    def extract_intent(self, response: Dict[Text, Any]) -> Dict[Text, Any]:
        intents = response.get('intents', [])
        if intents:
            wit_intent = intents[0]
            wit_intent_name = wit_intent.get('name', 'fallback')
            intent_name = self.intent_mappings.get(wit_intent_name, wit_intent_name)
            confidence = wit_intent.get('confidence', 0.0)
            return {'name': intent_name, 'confidence': confidence}
        else:
            return {'name': 'fallback', 'confidence': 0.0}

    def extract_entities(self, response: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = []
        wit_entities = response.get('entities', {})
        for entity_name, entity_list in wit_entities.items():
            for entity in entity_list:
                wit_entity_name = entity_name
                entity_name_mapped = self.entity_mappings.get(wit_entity_name, wit_entity_name)
                entities.append({
                    'entity': entity_name_mapped,
                    'value': entity.get('value'),
                    'confidence': entity.get('confidence', 1.0),
                    'start': entity.get('start'),
                    'end': entity.get('end'),
                })
        return entities
