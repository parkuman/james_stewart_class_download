import argparse
import urllib.request
import ssl
from bs4 import BeautifulSoup
import yt_dlp

ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser(description="Enter the url of the James Stewart course you'd like to save")

parser.add_argument("-u", "--url", type=str, required=True, help="The url to the James Stewart Course Page")

args = parser.parse_args()


def main():
    # strip the schedule.html part
    base_url = args.url[:-13]
    print("Fetching from course: " + base_url)

    contents = urllib.request.urlopen(base_url + "schedule.html").read()
    with open("schedule.html", "wb") as file:
       file.write(contents)
       
    # parse HTML
    soup = BeautifulSoup(str(contents), 'html.parser')

    # Find all the anchor tags in the parsed HTML
    anchor_tags = soup.find_all('a')

    yt_options = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': '%(title)s.%(ext)s',
    }

    # Iterate over the extracted anchor tags
    for anchor_tag in anchor_tags:
        vid_url = anchor_tag.attrs["href"]

        if vid_url.startswith("https://yout"):
            # download it
            print(vid_url)
            with yt_dlp.YoutubeDL(yt_options) as ydl:
                ydl.download([vid_url])

if __name__ == "__main__":
    main()
