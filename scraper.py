import requests
import bs4
import requests
import psutil
import os
import translate
#import summary


def get_text(url):
    # Make request to the website
    response = requests.get(url)

    # Parse HTML content with BeautifulSoup
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    # Extract all text from the website
    text = soup.get_text()

    return text

def split_file(file_path):
    # Read the contents of the file
    with open(file_path, 'r') as f:
        contents = f.readlines()

    # Split the contents in half
    split_index = len(contents) // 2
    first_half = contents[:split_index]
    second_half = contents[split_index:]

    # Write the first half to a new file
    with open('/output_files/first_half.txt', 'w') as f:
        f.writelines(first_half)

    # Write the second half to a new file
    with open('/output_files/second_half.txt', 'w') as f:
        f.writelines(second_half)


def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except:
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


if __name__ == "__main__":

#welcome message "scraper"
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

    print ('Starting web scraper...')
    print("Welcome to the web scraper")

    if has_ethernet_access() == False:
        print("No ethernet connection")
        print("Exiting...")
        exit()
    else:
        pass

    print("Please enter mode \n 1 - scrape \n 2 - summarize \n 3 - scrape and summarize \n 4 - help \n 5 - exit")
    mode = input("Enter mode: ")

    if mode == "1":
        print("Starting scrape...")

        num_urls = int(input("How many urls would you like to scrape max = 10? "))
        if num_urls > 10:
            print("Too many urls")
            print("Exiting...")
            exit()
        else:
            pass

        urls = []
        for i in range(num_urls):
            if num_urls == 1:

                urls.append(input("Enter url: "))

                if urls[i] == "":
                    print("No url entered")
                    print("Exiting...")
                    exit()

                if is_valid_url(urls[i]) == False:
                    print("Invalid url")
                    print("Exiting...")
                    exit()
                else:
                    pass

            else:
                urls.append(input("Enter url number " + str(i + 1)  +" : "))

        use_default = input("Use default file name? (y/n): ")
        if use_default == "y":
            file_path = "output_files/output.txt"
        else:
            file_path = input("Enter file name: ")

        for url in urls:
            print('Scraping website...')
            # Get the text from the website
            text = get_text(url)
            print('Scraping complete. Saving to file...')
            # Write the text to the output file
            try:
                # Split the file path into directory and file name
                dir_path, file_name_with_ext = os.path.split(file_path)
                file_name, file_ext = os.path.splitext(file_name_with_ext)

                for n in range(num_urls):
                    # Add the index and file extension to the file name
                    indexed_file_name = f"{file_name}_{n}{file_ext}"

                    # Join the directory and indexed file name to create the full file path
                    indexed_file_path = os.path.join(dir_path, indexed_file_name)

                    # Open the file and write the text
                    with open(indexed_file_path, 'w') as f:
                        f.write(text)

                    print('Done scraping ' + url)

                    input = input("Do you want to translate the text? (y/n): ")
                    if input == "y":
                        translate_to = __builtins__.input("Enter language to translate to (en)(fr)(de)(it)(ru): ")

                        translated_text = translate.translate_text(text, str(translate_to))

                        print("Translation complete.")
                        path_to_save = __builtins__.input("Enter path to save translation (if you want to use the default path type 1): ")
                        if path_to_save == "1":
                            path_to_save = "output_files/translation.txt"
                        else:
                            pass


                        with open(path_to_save, 'w') as f:
                            f.write(translated_text)



            except FileNotFoundError:
                print("File not found")
                print("Exiting...")
                exit()


    elif mode == "2":

        path = input("Enter file path for default use DEFAULT: ")
        if path == "DEFAULT":
            path = "output_files/result.txt"

        else :
            pass

        print("Starting summarize...")
        try :
            with open(path, "r") as file:
                content = file.read()
                word_count = len(content.split())

        except FileNotFoundError:
            print("File not found")
            if word_count < 1200:
                print("The file contains {} words.".format(word_count))
                print('Summarizing...')
                #print(summary.summarize_text(text))
            else:
                print("The file contains {} words.".format(word_count))
                print('The file is too long to summarize.')
                answer = input('Would you like to split the file? (y/n): ')
                if answer == 'y':
                    print('Spliting file...')
                    split_file('result.txt')
                    print('Done splitting!')

                    with open("first_half.txt", "r") as file:
                        content = file.read()
                        text = content
                        word_count = len(content.split())
                        if word_count > 1200:
                            split_file('first_half.txt')
                            print("The file contains {} words.".format(word_count))
                            print('Can not summarize...')
                            pass
                        else:
                            print("The file contains {} words.".format(word_count))
                            print('Summarizing...')
                            #print(summary.summarize_text(text))
                    with open("second_half.txt", "r") as file:
                        content = file.read()
                        word_count = len(content.split())
                        text = content
                        if word_count > 1200:
                            split_file('second_half.txt')
                            print("The file contains {} words.".format(word_count))
                            print('Can not summarize...')
                            pass
                        else:
                            print("The file contains {} words.".format(word_count))
                            print('Summarizing...')
                            #print(summary.summarize_text(text))
                else:
                    print('Exiting...')
                    exit()


    elif mode == "3":
        print("Starting scrape and summarize...")
        num_urls = int(input("How many urls would you like to scrape? "))
        urls = []
        for i in range(num_urls):
            urls.append(input("Enter url: "))

        for url in urls:
            print('Scraping website...')
            # Get the text from the website
            text = get_text(url)
            print('Scraping complete. Saving to file...')
            # Write the text to the output file
            with open('result.txt', 'w') as f:
                f.write(text)
            print('Done scraping ' + url)
        with open("result.txt", "r") as file:
            content = file.read()
            word_count = len(content.split())
            if word_count < 1200:
                print("The file contains {} words.".format(word_count))
                print('Summarizing...')
                #print(summary.summarize_text(text))
            else:
                print("The file contains {} words.".format(word_count))
                print('The file is too long to summarize.')
                answer = input('Would you like to split the file? (y/n): ')
                if answer == 'y':
                    print('Spliting file...')
                    split_file('result.txt')
                    print('Done splitting!')

                    with open("first_half.txt", "r") as file:
                        content = file.read()
                        text = content
                        word_count = len(content.split())
                        if word_count > 1200:
                            split_file('first_half.txt')
                            print("The file contains {} words.".format(word_count))
                            print('Can not summarize...')
                            pass
                        else:
                            print("The file contains {} words.".format(word_count))
                            print('Summarizing...')
                            #print(summary.summarize_text(text))
                    with open("second_half.txt", "r") as file:
                        content = file.read()
                        word_count = len(content.split())
                        text = content
                        if word_count > 1200:
                            split_file('second_half.txt')
                            print("The file contains {} words.".format(word_count))
                            print('Can not summarize...')
                            pass
                        else:
                            print("The file contains {} words.".format(word_count))
                            print('Summarizing...')
                            #print(summary.summarize_text(text))
                else:
                    print('Exiting...')
                    exit()
    elif mode == "4":

        mode = input("Enter 1 for usage manual or 2 for descryption: ")
        if mode == "1":
            print('''Scrape mode:
    1. Enter the number of urls you would like to scrape.
    2. Enter the urls you would like to scrape.
    3. The program will scrape the urls and save the text to a file called result.txt in your direcetory.
    4. The program will then ask if you would like to summarize the text.
    5. If you would like to summarize the text enter y.
    6. If you would like to exit enter n.
    7. If the file is too long to summarize the program will ask if you would like to split the file.
    8. If you would like to split the file enter y.
    9. If you would like to exit enter n.
    10. The program will then split the file into two files called first_half.txt and second_half.txt and then summarize them.
    
    Summarize mode:
    1. Enter the file path for the file you would like to summarize.
    2. The program will ask if you would like to summarize the text.
    3. If you would like to summarize the text enter y.
    4. If you would like to exit enter n.
    5. If the file is too long to summarize the program will ask if you would like to split the file.
    6. If you would like to split the file enter y.
    7. If you would like to exit enter n.
    
    Scrape and summarize mode:
    1. Enter the number of urls you would like to scrape.
    2. Enter the urls you would like to scrape.
    3. The program will scrape the urls and save the text to a file called result.txt in your direcetory.
    4. The program will then ask if you would like to summarize the text.
    5. If you would like to summarize the text enter y.
    6. If you would like to exit enter n.
    
''')
