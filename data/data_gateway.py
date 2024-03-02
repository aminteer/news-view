import requests
from dotenv import load_dotenv
import os
import logging
import json
import boto3
from botocore.exceptions import ClientError
from PIL import Image
from io import BytesIO, StringIO

# Configure logging to write to a file, making sure to append log messages
# and set the log level to DEBUG or higher
logging.basicConfig(filename='data_gateway.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
IMAGE_FILE_NAME = "news_summary.png"
NEWS_SUMMARY_FILE_NAME = "news_summary.txt"

class DataGateway:
        def __init__(self):
            load_dotenv()
            self.app_url = os.getenv('APP_URL')
            self.aws_access_key_id = os.getenv('BUCKETEER_AWS_ACCESS_KEY_ID')
            self.aws_region = os.getenv('BUCKETEER_AWS_REGION')
            self.aws_secret_key = os.getenv('BUCKETEER_AWS_SECRET_ACCESS_KEY')
            self.aws_bucket_name = os.getenv('BUCKETEER_BUCKET_NAME')
            self.add_stories_route = '/addstories'
            #set up AWS
            
        
        def write_stories_from_json_to_database(self, stories='no stories today'):
            #required to add stories in json format
            #simply post the json file to the flask app
            #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            url_add = str(self.app_url) + str(self.add_stories_route)
            logging.debug(f"Saving stories to database using the route: {url_add}")
            resp = requests.post(url=url_add, json=stories)
            if resp.status_code != 200:
                logging.debug(f"Error, stories save to database post not successful.  Status code: {resp.status_code}; message info: {resp.json()}; posted json: {stories}")
                raise Exception("Stories failed to post to add stories end point")
            
        def save_refined_summary_as_file(self, summary_text='no stories today'):
            #establish s3 bucket connection
            filename = NEWS_SUMMARY_FILE_NAME

            # Open the file in write mode ('w') and write the string
            with open(filename, 'w') as file:
                file.write(summary_text)
            
            if self.__upload_file(filename,self.aws_bucket_name):
                logging.debug("News summary file successfully saved to S3")
            else:
                logging.debug("ERROR! News summary file not saved.")
                
        def save_image_as_file(self, img=None):
            #establish s3 bucket connection
            filename = IMAGE_FILE_NAME
            
            if img!=None:
                news_img = img #Image(img)
                
                #resize image
                width, height = news_img.size
                # Calculate the new size, shrinking it by 20%
                scale = 0.8

                # Resize the image
                resized_image = news_img.resize((int(width * scale), int(height*scale)),resample=Image.BICUBIC) 
                # save the file locall
                resized_image.save(filename)
                
                if self.__upload_file(filename,self.aws_bucket_name):
                    logging.debug("News summary image successfully saved to S3")
                else:
                    logging.debug("ERROR! News summary image file not saved.")
                    
        def get_news_summary_image (self):
            filename = IMAGE_FILE_NAME
            obj = self.__download_file(bucket=self.aws_bucket_name,file_name=filename, type = 'image')
            img = Image.open(BytesIO(obj))
            logging.debug("News summary image downloaded from S3")
            #save a copy locally for debug purposes
            img.save("news_summary_image_debug.png")
            return img
        
        def get_news_summary_txt (self):
            filename = NEWS_SUMMARY_FILE_NAME
            obj = self.__download_file(bucket=self.aws_bucket_name,file_name=filename, type = 'text')
            text_obj = str(obj)
            logging.debug("News summary text downloaded from S3")
            return text_obj


        def __upload_file(self, file_name, bucket, object_name=None):
            """Upload a file to an S3 bucket

            :param file_name: File to upload
            :param bucket: Bucket to upload to
            :param object_name: S3 object name. If not specified then file_name is used
            :return: True if file was uploaded, else False
            """

            # If S3 object_name was not specified, use file_name
            if object_name is None:
                object_name = os.path.basename(file_name)

            # Upload the file
            s3_client = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_key)
            try:
                response = s3_client.upload_file(file_name, bucket, object_name)
            except ClientError as e:
                logging.error(e)
                return False
            return True
        
        def __download_file(self, bucket, file_name, type = 'text'):
            """
            Read the content of a file stored in an AWS S3 bucket.

            Parameters:
            - bucket_name: Name of the S3 bucket.
            - s3_object_name: S3 object name (file name in the bucket).
            - type: accepts either 'text' or 'image', defaults to text
            
            Returns:
            The content of the file.
            """
            try:
                # Create an S3 resource
                s3 = boto3.resource('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_key)
                obj = s3.Object(bucket,file_name)
                # Read the file's content
                if type == 'text':
                    file_content=obj.get()['Body'].read().decode()
                else:
                    file_content = obj.get()['Body'].read()
                #obj.close()
                #file_content = obj.get()['Body'].read().decode('utf-8')
                return file_content
            except Exception as e:
                print(f"An error occurred: {e}")
                return None