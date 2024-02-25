#!/usr/bin/env python

import requests
from dotenv import load_dotenv
import os
import logging
from openai import OpenAI
import openai



class LLM_gateway:

    def __init__(self):
        # Configure logging to write to a file, making sure to append log messages
        # and set the log level to DEBUG or higher
        logging.basicConfig(filename='llm_gateway.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logging.debug("Initiating LLM_gateway")
        load_dotenv()
        self.Client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def create_summary(self, stories_text = 'none'):
        # OpenAI model options gpt-4, gpt-4-turbo-preview, gpt-3.5-turbo
        try:
            logging.debug("Creating News Summary. Sending the following to OpenAI chat completion: {}".format(stories_text))
            prompt_start = "Summarize the following raw news stories data on top stories for the day with short descriptions into one short summary.  Ignore the words DEBUG and None.  This is the list of descriptions:  "
            chat_completion = self.Client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional journalist."},
                    {"role": "user","content": f"{prompt_start}{stories_text}",}
                ],
                model="gpt-3.5-turbo",
            )
            summary = chat_completion.choices[0].message.content
            logging.debug(f"Response from OpenAI: {summary}")
            return summary
        except openai.APIConnectionError as e:
            logging.debug("ERROR: The server could not be reached")
            logging.debug(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except openai.RateLimitError as e:
            logging.debug("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            logging.debug("Another non-200-range status code was received")
            logging.debug(e.status_code)
            logging.debug(e.response)
            
    def create_image_prompt(self, story_summary = 'none'):
        try:
            logging.debug("Creating Image Prompt. Sending the following to OpenAI chat completion: {}".format(story_summary))
            prompt_start = "Convert the following description into a text prompt for an image generation model.  This prompt should instruct to produce a high quality but funny image true to the key concepts in the description.  Here is the description:  "
            chat_completion = self.Client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a prompt engineer."},
                    {"role": "user","content": f"{prompt_start}{story_summary}",}
                ],
                model="gpt-4",
            )
            summary = chat_completion.choices[0].message.content
            logging.debug(f"Response from OpenAI: {summary}")
            return summary
        except openai.APIConnectionError as e:
            logging.debug("ERROR: The server could not be reached")
            logging.debug(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except openai.RateLimitError as e:
            logging.debug("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            logging.debug("Another non-200-range status code was received")
            logging.debug(e.status_code)
            logging.debug(e.response)


if __name__ == "__main__":
    client = LLM_gateway()
    #server = Server()
    #server.listen()