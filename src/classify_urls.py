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
            # try:
                browser = launch()
                page = browser.newPage()
                page.goto(x)
                page.screenshot({'path': screenshot_direcctory+f"\{count}.png"})  #Update this path accordingly
                browser.close()
                count += 1
            # except:
            #     print("hi")
            #     pass



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

    urls_file = r"\\TRUENAS\nas\event_centre_urls.txt" # Update this with the path to the file consisting the urls to be classified
    model_path = r"\\TRUENAS\nas\resnet50-erroranalysis-test_acc_0.73944_epoch-143.pt" # update this with the model path
    json_path = r"\\TRUENAS\nas\erroranalysis_model_classes.json" # Update with json path
    number_of_threads = 10 # Update this to increase or decrease number of threads
    screenshot_directory = r"\\TRUENAS\nas\SS"
    classified_data_directory = r"\\TRUENAS\nas\Classified_data"
    urls =[]
    with open (urls_file,"r") as file:
        for x in file:
            urls.append(file.readline().strip())
    print(urls)
    batch_size = len(urls)//number_of_threads
    # for x in range(number_of_threads):
    #     os.mkdir(screenshot_directory + f"\{str(x)}")
    
    threads = []
    for x in range(number_of_threads):
        thread = threading.Thread(target=ai_detection,args=(urls[(x*batch_size) : ((x*batch_size)+batch_size)],screenshot_directory+f"\{x}",
                                                            model_path,json_path,classified_data_directory))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()




    







# def fuzz(urls, wordlist,output_file, ffuf_path):
#     """
#     Run ffuf on the file of urls and save the results to json file. 
#     Parameters: urls file, wordlist file, output file, ffuf.exe file
#     """

#     cmd = f'{ffuf_path} -w {urls}:URL -w {wordlist}:PATH -u URLPATH -ac -o {output_file} -of json -t 10000 -timeout 30'
#     subprocess.call(cmd, shell=True)


# def create_dictionary(data):
#     """
#     Create a dictionary from the json file, retains only final redirected url incase of results with a redirect location.
#     Parameters: json file data.
#     Returns: 2 identical dictionaries
#     """
#     filtered_responses = {}
#     filtered_responses_backup = {}
#     unfiltered_responses = {}
#     unfiltered_responses_backup = {}
#     for i in data["results"]:
#         unfiltered_responses[i['url']] = i
#         unfiltered_responses_backup[i['url']] = i
#         if i["redirectlocation"] == "":
#             filtered_responses[i['url']] = i
#             filtered_responses_backup[i['url']] = i
#         elif "http" not in i["redirectlocation"][:5] and len(i["redirectlocation"]) !=0 :
#             filtered_responses[i['url']+i["redirectlocation"]] = i
#             filtered_responses_backup[i['url']+i["redirectlocation"]] = i
#         else:
#             filtered_responses[i["redirectlocation"]] = i
#             filtered_responses_backup[i["redirectlocation"]] = i
#     return filtered_responses,unfiltered_responses,filtered_responses_backup,unfiltered_responses_backup

# def calculate_mode(urlDict):
#     """
#     Creates a list of all the lines and word of a response as a custom hash and calculate the stastical mode of the data
#     Parameters: A dictionary of the responses
#     Returns: Mode
#     """
#     words_lines_hash = []
#     for i in urlDict:
#         words_lines_hash.append(str(urlDict[i]["words"])+str(urlDict[i]["lines"]))
#     [int(x) for x in words_lines_hash]
#     mode = statistics.mode(words_lines_hash)

#     return mode

# def filter(urlDict):
#     """
#     Filters the results in the dictionary by recursively calculating the mode of the custom hash and eliminating all results with the same hash as the mode
#     but retaining just one result of each.
#     Parameters: Dictionary of response and their data
#     Returns: None
#     """
#     mode = calculate_mode(urlDict)
#     count = 0
#     for i in list(urlDict):
#         if str(urlDict[i]["words"])+str(urlDict[i]["lines"]) == mode:
#             count+= 1
#             if count != 1:
#                 del urlDict[i]
#     new_mode = calculate_mode(urlDict)
#     if new_mode != mode:
#         filter(urlDict)
#     else:
#         return 


# def remove_path_independant(urlDict,urls):
#     """
#     Removes all urls post filtration that are independant of their path and has the exact same response as their base url
#     Parameters: Dictionary of responses and their data, list of urls
#     Returns: A list of urls that were removed
#     """
#     removed_url = []
#     for i in urls:
#         try:
#             response = requests.get(i)
#             base_url = urlparse(i).scheme +"://"+ urlparse(i).netloc
#             alter_response = requests.get(base_url)
#             if response.text == alter_response.text:
#                 removed_url.append(i)
#                 urls.remove(i)
#                 del urlDict[str(i)]
#             elif custom_auto_calibrate(i,response):
#                 removed_url.append(i)
#                 urls.remove(i)
#                 del urlDict[str(i)]
#         except requests.exceptions.RequestException:
#             pass
#     return removed_url

# def custom_auto_calibrate(url,response):
#     """
#     Filters out urls that have the same response as their base url followed by a random stirng. Similar to auto calibrate in ffuf
#     Parameters: a string containing the url, the response of the url
#     """
#     try:
#         random_url = urlparse(url).scheme +"://"+ urlparse(url).netloc+"/abcxyz"
#         random_response = requests.get(random_url)
#         if response.content == random_response.content:
#             return True
#     except requests.exceptions.RequestException:
#             pass

# def retrieve_similar(backupDict,classfication,urlDict):
#     """
#     Maintaining a dictionary of unfiltered urls, given a list of urls, this function retrieves all other urls which have a similar response to the given urls
#     Parameters: An unfiltered dictionary of responses, list of urls, dictionary of filtered urls
#     Returns: None
#     """
#     Verified_Urls = list(classfication.keys())
#     if len(Verified_Urls) != 0:
#         success_urls = Verified_Urls
#         for url in success_urls:
#             lines = backupDict[url]['lines']
#             words = backupDict[url]['words']

#             for i in backupDict:
#                 if backupDict[i]["words"] == words and backupDict[i]["lines"] == lines:
#                     if i not in classfication:
#                         classfication[i] = classfication[url]
#                         urlDict[i] = backupDict[i]


    # output_file = r"C:\Users\rishi\Documents\event_centre_filtered.txt" # Replace with your output file
    # urls_file = r"\\TRUENAS\nas\event_centre_urls.txt" # Replace with your urls file
    # wordlist_file = r"\\TRUENAS\nas\empty.txt" # Replace with your wordlist file
    # ffuf_path = r"FFUF_PATH"  # Replace with the path to your ffuf.exe file
    # fuzz(urls_file,wordlist_file,output_file,ffuf_path)
    # file = open(output_file)
    # data = json.load(file)
    # urlDict , unfiltered_data, backupDict, unfiltered_data_backup = create_dictionary(data)
    # print(len(unfiltered_data))
    # # filter(unfiltered_data)
    # # print(len(unfiltered_data))
    # # urls = list(unfiltered_data.keys())
    # # # removed_urls = remove_path_independant(urlDict,urls)
    # # classification = ai_detection(urls,unfiltered_data)
    # # print(len(classification))
    # # retrieve_similar(unfiltered_data_backup,classification,unfiltered_data)
    # # print(len(classification))
    # # write_to_file(classification,"Event_centre_data_classified_unfiltered.txt")