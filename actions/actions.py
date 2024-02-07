# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Dict, Text, List, Optional, Any

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa.core.actions.forms import FormAction

from hugchat import hugchat
from hugchat.login import Login

import os

#if 'CHAT_USER' in os.environ and 'CHAT_PASSWORD' in os.environ:
#    email = os.environ['CHAT_USER']
#    password = os.environ['CHAT_PASSWORD']
#else:
#    raise Exception("chat.user and chat.password must be set in environment variables")

sign = Login("hirofushikar@gmail.com", "") #fill in your email and password here
cookie_path_dir = "./cookies_snapshot"
try:
    cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.
except Exception:
    cookies = sign.login()
    sign.saveCookiesToDir(cookie_path_dir)

chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
chatbot.switch_llm(1)
id = chatbot.new_conversation()
chatbot.change_conversation(id) # switch once to the new conversation

biography_question="Can you share with me the story of your life, starting from your earliest memories, focusing on your family situation, education, past and present relationships, and how these experiences have shaped your current lifestyle?"
sexuality_question="How would you describe your journey of sexual development and experiences from childhood to now, and how do these experiences reflect in your current romantic relationships or perceptions of intimacy?"
self_perception_question="When you reflect on who you are, how would you describe your self-image and the thoughts and feelings that shape your perception of yourself?"
psychiatric_history_question="Can you walk me through your medical history, particularly focusing on any psychiatric diagnoses or treatments you've received, and how these experiences have impacted your life and wellbeing?"
addiction_history_question="Let's discuss any past or present experiences with addiction, whether substance-related or not. How have these addictions interacted with your values, life choices, and overall wellbeing?"
psychosocial_question="Can you tell me about your family's mental health history, including any known mental disorders or behaviors that might suggest a predisposition to certain conditions, and how this history has influenced your life and relationships?"
somatic_history_question="I'd like to understand more about your physical health history. Can you discuss any significant illnesses or injuries you've experienced, particularly those that have had mental or emotional repercussions?"
forensic_history_question="It's also important to talk about any encounters with the law or behaviors that might be connected to your mental health. Can you share any such experiences, and how you believe they relate to your overall mental and emotional state?"

def get_prompt(question, user_response):
    return "In the context of an initial therapy session (anamnesis), does the following response by a client satisfy the question '"+question+"'\nClient's response: '"+user_response+"'\n Just answer with a 'yes' or 'no' response. one word response only, do not reason or explain."

def extract_slot(slot_name, question, tracker: Tracker):
  current_slot_values = tracker.current_slot_values()
  if(current_slot_values['requested_slot'] != slot_name):
    return current_slot_values
  text_of_last_user_message = tracker.latest_message.get("text")
  new_slot_value = None
  for resp in chatbot.query(
    get_prompt(question, text_of_last_user_message),
    stream=True
  ):
    print(resp)
    if('yes' in resp['token'].lower()):
      new_slot_value = text_of_last_user_message
      break
    elif('no' in resp['token'].lower()):
      break
  #chatbot.delete_conversation(id) # dont delete for debugging
  current_slot_values[slot_name] = new_slot_value
  return current_slot_values

class ValidateAnamnesisForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_anamnesis_form"

    async def extract_biography_done(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
      return extract_slot("biography_done", biography_question, tracker)

    async def extract_sexuality_done(
      self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
      return extract_slot("sexuality_done", sexuality_question, tracker)

    async def extract_self_perception_done(
      self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
      return extract_slot("self_perception_done", self_perception_question, tracker)

    async def extract_psychiatric_history_done(
      self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
      return extract_slot("psychiatric_history_done", psychiatric_history_question, tracker)

    async def extract_addiction_history_done(
      self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
      return extract_slot("addiction_history_done", addiction_history_question, tracker)

    async def extract_psychosocial_done(
      self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
      return extract_slot("psychosocial_done", psychosocial_question, tracker)
      
    async def extract_somatic_history_done(
      self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
      return extract_slot("somatic_history_done", somatic_history_question, tracker)

    async def extract_forensic_history_done(
      self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
      return extract_slot("forensic_history_done", forensic_history_question, tracker)
