import json

with open("C:\ProjectX\AI\Databses\_select_target_from_alert_a_alert_detail_ad_where_a_id_ad_alert__202308111151.json","r") as file:
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