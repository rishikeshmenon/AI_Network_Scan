"""
Code to downlaod images from the web given a set of keywords.
"""

def download_images(keywords,number_images):
    from simple_image_download import simple_image_download as simp
    response = simp.Downloader 
    for x in keywords:
        response().download(x, number_images)

def main():
    keywords = [] #Add the keywords of the websites data you want to dowanload images of. Make sure there are no spaces in any keyword
    number_images = 1000  #Changes the number of images to be downloaded of each keyword

    download_images(keywords,number_images)

main()
"""
The keywords need to be entered as individual string in the list. Each keyword should only be one word. Ensure there are no spaces in a string
as the word will be treated as 2 key words and only the first half will be downloaded. E.g.: Valid: "LoginPages" Ivalid: "Login Pages"
"""