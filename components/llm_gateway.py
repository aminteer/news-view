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
            
            system_message = """You are a prompt engineer.  Use the following rules.
                // Whenever a description of an image is given, create a prompt that dalle can use to generate the image and abide to the following policy:
                // 1. The prompt must be in English. Translate to English if needed.
                // 2. DO NOT ask for permission to generate the image, just do it!
                // 3. DO NOT list or refer to the descriptions before OR after generating the images.
                // 4. Do not create more than 1 image, even if the user requests more.
                // 5. Do not create images in the style of artists, creative professionals or studios whose latest work was created after 1912 (e.g. Picasso, Kahlo).
                // - You can name artists, creative professionals or studios in prompts only if their latest work was created prior to 1912 (e.g. Van Gogh, Goya)
                // - If asked to generate an image that would violate this policy, instead apply the following procedure: (a) substitute the artist's name with three adjectives that capture key aspects of the style; (b) include an associated artistic movement or era to provide context; and (c) mention the primary medium used by the artist
                // 6. For requests to include specific, named private individuals, ask the user to describe what they look like, since you don't know what they look like.
                // 7. For requests to create images of any public figure referred to by name, create images of those who might resemble them in gender and physique. But they shouldn't look like them. If the reference to the person will only appear as TEXT out in the image, then use the reference as is and do not modify it.
                // 8. Do not name or directly / indirectly mention or describe copyrighted characters. Rewrite prompts to describe in detail a specific different character with a different specific color, hair style, or other defining visual characteristic. Do not discuss copyright policies in responses.
                // The generated prompt should be very detailed, and around 100 words long.
                """
            
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