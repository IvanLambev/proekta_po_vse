import bs4
import requests
import psutil
import os

import summary


def get_text(url):
    # Make request to the website
    response = requests.get(url)

    # Parse HTML content with BeautifulSoup
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    # Extract all text from the website
    text = soup.get_text()

    return text


def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except:
        return False


def is_valid_path(path):
    if os.path.exists(path):
        return True
    else:
        return False


def has_ethernet_access():
    interfaces = psutil.net_if_stats()
    for ifname, ifstat in interfaces.items():
        if ifstat.isup and psutil.net_if_addrs().get(ifname):
            addrs = psutil.net_if_addrs()[ifname]
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    return True
    return False


def scrape_and_output_to_file(url_count, url, file_path, file_name):
    url_count = int(url_count)  # convert to int
    print(url_count)
    default_file_path = os.path.join(os.getcwd() , "output_files")
    print(default_file_path)
    default_file_name = "file_"

    if file_path == "":
        file_path = default_file_path
    else:
        pass

    if file_name == "":
        file_name = default_file_name
    else:
        pass

    for i in range(url_count):
        if is_valid_url(url[i]):
            text = get_text(url[i])
            scraped_file_name = file_name + str(i) + ".txt"
            file_pathname = os.path.join(file_path, scraped_file_name)
            print(file_pathname+"\n")
            #
            with open(file_pathname, "w") as f:
                f.write(str(text.encode("utf-8")))
            print("File saved to: " + file_pathname)
            print("")
        else:
            print("Invalid URL")
            print("Skipping...")
            pass


def summarize(path_to_file, summary_file_name, summary_file_path):
    if is_valid_path(path_to_file):
        with open(path_to_file, "r") as f:
            text_to_summarize = f.read()
            summarized_text = summary.summarize_text(text_to_summarize)
            default_file_path = "./output_files"
            default_file_name = "file_summarized"

            if summary_file_path == "":
                summary_file_path = default_file_path
            else:
                pass

            if summary_file_name == "":
                summary_file_name = default_file_name
            else:
                pass

            file_name = summary_file_name + ".txt"
            file_pathname = os.path.join(summary_file_path, summary_file_name)

            with open(file_pathname, "w") as f:

                f.write(str(summarized_text.encode("utf-8")))
    else:
        return "Invalid path to file"


if __name__ == "__main__":

    if not os.path.exists("output_files"):
        os.mkdir("output_files")

    # welcome message "scraper"
    print('''

 __          __  _        _____                                      
 \ \        / / | |      / ____|                                     
  \ \  /\  / /__| |__   | (___   ___ _ __ __ _ _ __  _ __   ___ _ __ 
   \ \/  \/ / _ \ '_ \   \___ \ / __| '__/ _` | '_ \| '_ \ / _ \ '__|
    \  /\  /  __/ |_) |  ____) | (__| | | (_| | |_) | |_) |  __/ |   
     \/  \/ \___|_.__/  |_____/ \___|_|  \__,_| .__/| .__/ \___|_|   
                                              | |   | |              
                                              |_|   |_|              

    ''')

    print('Starting web scraper...')
    print("Welcome to the web scraper")

    if has_ethernet_access() == False:
        print("No ethernet connection")
        print("Exiting...")
        exit()
    else:
        pass

    print("Please enter mode \n 1 - scrape and output to a file  \n 2 - scrape and summarize \n 3 - exit")
    mode = input("Enter mode: ")

    if mode == "1":

        url_count = int(input("Enter number of urls to scrape: "))
        url = []
        for i in range(url_count):
            url_input = input("Enter url: ")
            url.append(url_input)
        print(url[i])
        file_path = input("Enter file path: ")
        file_name = input("Enter file name: ")

        scrape_and_output_to_file(url_count, url, file_path, file_name)

    elif mode == "2":

        url_count = int(input("Enter number of urls to scrape: "))
        url = input("Enter url: ")
        file_path = input("Enter file path: ")
        file_name = input("Enter file name: ")
        scrape_and_output_to_file(url_count, url, file_path, file_name)
