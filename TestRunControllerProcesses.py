#!/usr/bin/env python
from components import llm_gateway, image_gen_gateway, news_gateway
from PIL import Image 


# import llm_gateway
# import image_gen_gateway
# import news_gateway


def compile_stories_into_summary (stories):
    summary = ""
    for story in stories:
        summary += " " + story
    
    return summary

if __name__ == '__main__':
    #run through a sample process of obtaining top stories and creating prompts
    print('\nGrabbing news top stories')
    news = news_gateway.NewsGateway()
    #top_stories = news.get_top_stories('business')
    top_stories = news.get_top_stories('general')
    print(f"\n\nlist of top stories: \n {top_stories}")
    
    summarized = compile_stories_into_summary(top_stories)
    print(f"\n\nSummarized raw: {summarized}")
    
    #send to LLM to make more cohesive summary
    llm = llm_gateway.LLM_gateway()
    #summarized = "The hotel took down the sign due to economic issues and high vacancy rates"    #try this for diagnostics
    nice_summary = llm.create_summary(summarized)
    print(f"\n\nNice summary: {nice_summary}")
    
    #save the summary to a file
    file_path = "news_summary.txt"
    file_path2 = "\assets\news_summary.txt"
    # Open the file in write mode ('w') and write the string to it
    with open(file_path, 'w') as file:
        file.write(nice_summary)
    print(f"String has been successfully saved to {file_path}")
    
    #get the image gen prompt
    prompt = llm.create_image_prompt(nice_summary)
    print(f"\n\nImage gen prompt: {prompt}")
    
    #generate an image and save it locally
    image_gen = image_gen_gateway.ImageGenGateway()
    img = image_gen.generate_summary_image(summary_prompt=prompt)
    #save img to local file
    img.save(f"news_summary.png")
    print(f"\n\nScript complete, image should be completed")
    
    