import bs4
import requests
import psutil
import os

import summary

default_file_path = os.path.join(os.getcwd(), "output_files")



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


def scrape_and_output_to_file(url, file_path, file_name):
    print(url)

    if is_valid_url(url):
        print("Valid URL")
        text = get_text(url)
        scraped_file_name = file_name + str(i) + ".txt"
        file_pathname = os.path.join(file_path, scraped_file_name)
        if os.path.isfile(file_pathname):
            print("File already exists")
            will_overwrite = input("Overwrite? (y/n): ")
            will_overwrite = will_overwrite.lower()
            if will_overwrite == "y":
                pass
            else:
                print("Skipping...")
                return
        else:
            pass

        
        with open(file_pathname, "w") as f:
            f.write(str(text.encode("utf-8")))
            f.close()
        print("File " + str(i) + " saved to: " + file_pathname)
        print("")
    else:
        print("Invalid URL")
        print("Skipping...")
        return "Invalid URL"


def summarize(path_to_file, summary_file_name, summary_file_path):
    if is_valid_path(path_to_file):
        os.chmod(path_to_file, 0o777)
        os.chmod(file_path, 0o777)   # set permissions of the output_files folder
           # set permissions of the file to be written
        with open(path_to_file, "r") as f:
            text_to_summarize = f.read()
            summarized_text = summary.summarize_text(text_to_summarize)
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
            file_pathname = os.path.join(summary_file_path, file_name)
            
            with open(file_pathname, "w") as f:

                f.write(str(summarized_text.encode("utf-8")))
                f.close()
    else:
        return "Invalid path to file"


if __name__ == "__main__":

    if not os.path.exists("output_files"):
        os.mkdir("output_files")
        os.chmod("output_files", 0o777)

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

    if not has_ethernet_access():
        print("No ethernet connection")
        print("Exiting...")
        exit()
    else:
        pass

    print("Please enter mode \n 1 - scrape and output to a file  \n 2 - scrape and summarize \n 3 - exit")
    mode = input("Enter mode: ")

    if mode == "1":

        url_count = int(input("Enter number of urls to scrape: "))

        for i in range(url_count):
            url = input("Enter url " + str(i + 1) + ": ")
            print(is_valid_url(url))
            file_path = input("Enter file path: ")
            file_name = input("Enter file name: ")



            default_file_name = "file_"

            if file_path == "":
                file_path = default_file_path
            elif not os.path.exists(file_path):
                os.mkdir(file_path)
            else:
                pass

            if file_name == "":
                file_name = default_file_name
            else:

                pass

            print("Starting...")
            scrape_and_output_to_file(url, file_path, file_name)
            print("Done")

    elif mode == "2":

        url_count = int(input("Enter number of urls to scrape: "))
        default_file_name = "file_summarized"
        for i in range(url_count):
            url = input("Enter url " + str(i + 1) + ": ")
            print(is_valid_url(url))
            file_path = input("Enter file path: ")
            file_name = input("Enter file name: ")

            if file_path == "":
                file_path = default_file_path
            elif not os.path.exists(file_path):
                os.mkdir(file_path)
            else:
                pass

            if file_name == "":
                file_name = default_file_name
            else:

                pass

            print("Starting...")
            scrape_and_output_to_file(url, file_path, file_name)
            print("Done")

            summarize(file_path, file_name, file_path)
            print("Done")
