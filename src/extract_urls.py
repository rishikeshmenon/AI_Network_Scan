import json

path_to_json_file = "DIR_HERE"

with open(path_to_json_file,"r") as file:
    data = json.load(file)
    urls = []
    for x in data["results"]:
        dict = json.loads(x["target"])
        if "location" in dict.keys():
            if len(dict["location"]) == 0:
                urls.append(dict["url"])
            else:
                urls.append(dict["location"][0])
        elif "ip" in dict.keys():
            if len(dict["service_name"].split("/")) == 1:
                urls.append("https://"+ dict["ip"])
            elif len(dict["service_name"].split("/")) == 2:
                urls.append("https://" + dict["ip"]+":"+dict["service_name"].split("/")[1])
    print(len(urls))

with open("event_centre_urls.txt","w") as output:
    for url in urls:
        output.write(url + "\n")