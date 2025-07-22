""""
The purpose of this code is to directory-brute force a set of URLS using ffuf and filter the results to eliminate false positives
# Check main for instructions

"""
import json
import os
from urllib.parse import urlparse
import subprocess
from imageai.Classification.Custom import CustomImageClassification
from pyppeteer import launch
import threading
import asyncio




def ai_detection(urls,screenshot_direcctory,model_path,json_path,classfied_data_path):
    
    async def main(urls):
        count = 0
        for x in urls:
                browser = launch()
                page = browser.newPage()
                page.goto(x)
                page.screenshot({'path': screenshot_direcctory+f"\{count}.png"})  #Update this path accordingly
                browser.close()
                count += 1
            



    prediction = CustomImageClassification()
    prediction.setModelTypeAsResNet50()
    prediction.setModelPath(model_path)  
    prediction.setJsonPath(json_path) 
    prediction.loadModel()

    classified_data = {}
    classifications = ["Very High","High","Medium","Low"]
    for x in range(len(urls)):
        try:
            predictions, probabilities = prediction.classifyImage(screenshot_direcctory+f"\{x}.png", result_count=4)   
            classified_data[urls[x]] = {}
            count = 0
            for eachPrediction, eachProbability in zip(predictions, probabilities):
                classified_data[urls[x]][eachPrediction] = classifications[count]
                count+=1
        except ValueError:
            print("bye")
            classified_data[urls[x]] = "Unclassified"
            pass
    write_to_file(classifications,classfied_data_path)

    def write_to_file(classification,file):
        """
        Given a list of urls, wirtes them into a specified file.
        Parameters: A list of urls
        Returns: None
        """
        with open(file,"w") as f:
            f.write(str(classification))

if __name__ == "__main__":

    urls_file = "DATA_DIR/urls_to_classify.txt"
    model_path = "MODEL_PATH/model.pt"
    json_path = "MODEL_PATH/model_classes.json"
    screenshot_directory = "OUTPUT_DIR/screenshots"
    classified_data_directory = "OUTPUT_DIR/classified_data"

    urls = []
    number_of_threads = 10  #Update this to increase or decrease number of threads

    with open (urls_file,"r") as file:
        for x in file:
            urls.append(file.readline().strip())
    print(urls)
    batch_size = len(urls)//number_of_threads
    for x in range(number_of_threads):
         os.mkdir(screenshot_directory + f"\{str(x)}")
    
    threads = []
    for x in range(number_of_threads):
        thread = threading.Thread(target=ai_detection,args=(urls[(x*batch_size) : ((x*batch_size)+batch_size)],screenshot_directory+f"\{x}",
                                                            model_path,json_path,classified_data_directory))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()




    




