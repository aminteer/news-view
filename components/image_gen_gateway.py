#!/usr/bin/env python

import requests
from dotenv import load_dotenv
import os
import logging
from openai import OpenAI
import openai
import datetime
from PIL import Image 
import base64
from io import BytesIO




class ImageGenGateway:

    def __init__(self):
        # Configure logging to write to a file, making sure to append log messages
        # and set the log level to DEBUG or higher
        logging.basicConfig(filename='image_gen_gateway.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logging.debug("Initiating ImageGenGateway")
        load_dotenv()
        self.Client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
    def generate_summary_image(self, summary_prompt = 'none'):
        try:
            logging.debug(f"Starting the image generation process \n")
            prompt_start = ""
            
            #prompt_full = (f"{prompt_start}Subject: {summary_prompt} Style: Hyperrealistic, whimsical, humorous, photorealistic and magazine cover styling. ")
            #alternatives
            #prompt_full = (f"{prompt_start}Subject: {summary_prompt} Style: Hyperrealistic, whimsical, humorous, photorealistic and magazine cover styling. ")
            prompt_full = (f"{prompt_start}Subject: {summary_prompt} Style: Hyperrealistic, whimsical, crisp, photorealistic and collage style. ")
            #prompt_full = (f"{prompt_start}Subject: {summary_prompt} Style: photorealistic, journalism, landscape style. ")
            logging.debug(f"Image Gen prompt: {prompt_full}")
            response = self.Client.images.generate(
                model="dall-e-3",
                prompt=prompt_full,
                size="1024x1792",
                quality="standard",
                style='vivid',
                n=1,
                response_format="b64_json",
                )
            
            #get revised prompt to log to debug if Dalle3 changes the prompt
            revised_prompt = response.data[0].revised_prompt
            logging.debug(f"DallE3 revised prompt: {revised_prompt}")
            
            #assume there may be more than 1 image reponse to be safe
            # note the use of pydantic "model.data" style reference and its model_dump() method
            image_url_list = []
            image_data_list = []
            for image in response.data:
                image_url_list.append(image.model_dump()["url"])
                image_data_list.append(image.model_dump()["b64_json"])
            
            # Initialize an empty list to store the Image objects   
            image_objects = []
            
            #store images locally for debug and loggin purposes
            # make a file name prefix from date-time of response
            dt = datetime.datetime
            images_dt = dt.utcfromtimestamp(response.created)
            img_filename = images_dt.strftime('news_summary-%Y%m%d_%H%M%S')  # like 'DALLE-20231111_144356'
            
            if image_url_list and all(image_url_list):
                #log all urls
                logging.debug("URLs of returned images")
                for url in image_url_list:
                    logging.debug(url)
            elif image_data_list and all(image_data_list):  # if there is b64 data
                # Convert "b64_json" data to png file
                for i, data in enumerate(image_data_list):
                    image_objects.append(Image.open(BytesIO(base64.b64decode(data))))  # Append the Image object to the list
                    image_objects[i].save(f"{img_filename}_{i}.png")
                    logging.debug(f"{img_filename}_{i}.png was saved")
            else:
                logging.debug("No image data was obtained. This is a problem!")    
            #print(response.data[0].url)
            img = image_objects[0]
            return img
        except openai.APIConnectionError as e:
            error_msg = "Server connection error: {e.__cause__}"
            print(error_msg)
            logging.debug(error_msg)
            raise
        except openai.RateLimitError as e:
            print(f"OpenAI RATE LIMIT error {e.status_code}: (e.response)")
            raise
        except openai.APIStatusError as e:
            error_msg = f"OpenAI STATUS error {e.status_code}: (e.response)"
            print(error_msg)
            logging.debug(error_msg)
            raise
        except openai.BadRequestError as e:
            error_msg =f"OpenAI BAD REQUEST error {e.status_code}: (e.response)"
            print(error_msg)
            logging.debug(error_msg)
            raise
        except Exception as e:
            error_msg =f"An unexpected error occurred: {e}"
            print(error_msg)
            logging.debug(error_msg)
            raise


if __name__ == "__main__":
    client = ImageGenGateway()
    #server = Server()
    #server.listen()