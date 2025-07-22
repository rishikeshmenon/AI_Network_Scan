""""
The purpose of this code is to directory-brute force a set of URLS using ffuf and filter the results to eliminate false positives
# Check main for instructions

"""
import json
import requests
import statistics
from urllib.parse import urlparse
import subprocess


def fuzz(urls, wordlist,output_file, ffuf_path):
    """
    Run ffuf on the file of urls and save the results to json file. 
    Parameters: urls file, wordlist file, output file, ffuf.exe file
    """

    cmd = f'ffuf -w {urls}:URL -w {wordlist}:PATH -u URLPATH -mc all -o {output_file} -of json -t 1000'
    print(cmd)
    subprocess.call(cmd, shell=True)


def create_dictionary(data):
    """
    Create a dictionary from the json file, retains only final redirected url incase of results with a redirect location.
    Parameters: json file data.
    Returns: 2 identical dictionaries
    """
    filtered_responses = {}
    filtered_responses_backup = {}
    unfiltered_responses = {}
    unfiltered_responses_backup = {}
    for i in data["results"]:
        unfiltered_responses[i['url']] = i
        unfiltered_responses_backup[i['url']] = i
        if i["redirectlocation"] == "":
            filtered_responses[i['url']] = i
            filtered_responses_backup[i['url']] = i
        elif "http" not in i["redirectlocation"][:5] and len(i["redirectlocation"]) !=0 :
            filtered_responses[i['url']+i["redirectlocation"]] = i
            filtered_responses_backup[i['url']+i["redirectlocation"]] = i
        else:
            filtered_responses[i["redirectlocation"]] = i
            filtered_responses_backup[i["redirectlocation"]] = i
    return filtered_responses,unfiltered_responses,filtered_responses_backup,unfiltered_responses_backup

def calculate_mode(urlDict):
    """
    Creates a list of all the lines and word of a response as a custom hash and calculate the stastical mode of the data
    Parameters: A dictionary of the responses
    Returns: Mode
    """
    words_lines_hash = []
    for i in urlDict:
        words_lines_hash.append(str(urlDict[i]["words"])+str(urlDict[i]["lines"]))
    [int(x) for x in words_lines_hash]
    mode = statistics.mode(words_lines_hash)

    return mode

def filter(urlDict):
    """
    Filters the results in the dictionary by recursively calculating the mode of the custom hash and eliminating all results w  ith the same hash as the mode
    but retaining just one result of each.
    Parameters: Dictionary of response and their data
    Returns: None
    """
    mode = calculate_mode(urlDict)
    count = 0
    for i in list(urlDict):
        if str(urlDict[i]["words"])+str(urlDict[i]["lines"]) == mode:
            count+= 1
            if count != 1:
                del urlDict[i]
    new_mode = calculate_mode(urlDict)
    if new_mode != mode:
        filter(urlDict)
    else:
        return 

def write_to_file(urls,file):
    """
    Given a list of urls, wirtes them into a specified file.
    Parameters: A list of urls
    Returns: None
    """
    with open(file,"w") as output:
        for i in urls:
            output.write(i)
            output.write("\n")

if __name__ == "__main__":
    output_file = "DATA_DIR/output.txt"
    urls_file = "DATA_DIR/urls.txt"
    wordlist_file = "DATA_DIR/wordlist.txt"
    ffuf_path = "FFUF_PATH"
    fuzz(urls_file,wordlist_file,output_file,ffuf_path)
    file = open(output_file)
    data = json.load(file)
    urlDict , unfiltered_data, backupDict, unfiltered_data_backup = create_dictionary(data)
    filter(unfiltered_data)
    urls = list(unfiltered_data.keys())
    write_to_file(urls,"ClientX_filtered_train_data.txt") # Update file path 
    [print(x) for x in urls]
    print("Results before filtration: ",len(unfiltered_data_backup))
    print("Results post filtration: ", len(unfiltered_data))

    







