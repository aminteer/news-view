#!/usr/bin/env python

import logging
import datetime
from PIL import Image 
import base64
from io import BytesIO
from components.image_gen_gateway import ImageGenGateway
from components.llm_gateway import LLM_gateway
from data.data_gateway import DataGateway

class Transformations:

    def __init__(self, stories):
        # Configure logging to write to a file, making sure to append log messages
        # and set the log level to DEBUG or higher
        logging.basicConfig(filename='transform_to_image.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logging.debug("Initiating Transform to Image class")    
        self.stories_json = stories
        self.llm = LLM_gateway()
        self.image_gen = ImageGenGateway()
        self.data_storage = DataGateway()
        
    def TransformJsonStoriesToRawSummary(self, stories = None):
        
        if stories==None : stories = self.stories_json
        story_list = []
        #transform json into a list of story descriptions
        for story in stories['articles']:
            title = story['title']
            description = story['description']
            if title!='[Removed]':
                #combine into responses list
                story_summary = f"title: {title}; description: {description}"
                logging.debug(story_summary)
                story_list.append(story_summary)
        
        summary = ""
        for story in story_list:
            summary += " " + story
            
        self.story_summary_raw = summary
        
        logging.debug(f"Json transformed to raw summary: {summary}") 
        
        return summary
    
    def TransformRawSummaryToRefinedSummary(self, summary = None):
        
        if summary==None : summary = self.story_summary_raw
        
        logging.debug(f"Transforming Raw Summary to Refined Summary") 
        refined = self.llm.create_summary(summary)
        self.story_summary_refined = refined
        logging.debug(f"Raw story summaries transformed to refined summary: {refined}") 
        
        return refined
    
    def TransformRefinedSummaryToImageGenPrompt(self, summary=None):
        
        if summary ==None : summary = self.story_summary_refined
        logging.debug(f"Transforming Refined Summary to Image Gen Prompt") 
        img_prompt = self.llm.create_image_prompt(summary)
        
        self.image_prompt = img_prompt
        
        return img_prompt
    
    def TransformImagePromptToImage(self, image_prompt=None):
        if image_prompt ==None : image_prompt = self.image_prompt
        
        logging.debug(f"Transforming Image Prompt into an image")
        img = self.image_gen.generate_summary_image(image_prompt)
        self.image_result = img
        
        return img
    
    def SaveGeneratedAssets(self):
        ds = self.data_storage
        logging.debug(f"Saving summary story")
        ds.save_refined_summary_as_file(self.story_summary_refined)
        logging.debug(f"Saving image file")
        ds.save_image_as_file(self.image_result)
        logging.debug(f"Saving stories to database")
        ds.write_stories_from_json_to_database(self.stories_json)
        
    
    def RunFullProcess(self, stories_json= None):
        if stories_json ==  None : stories_json = self. stories_json
        self.stories_json = stories_json
        self.TransformJsonStoriesToRawSummary()
        self.TransformRawSummaryToRefinedSummary()
        self.TransformRefinedSummaryToImageGenPrompt()
        self.TransformImagePromptToImage()
        self.SaveGeneratedAssets()
        

    
        
        
