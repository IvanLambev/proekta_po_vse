import requests
import bs4
import argparse
import summary


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
    with open('first_half.txt', 'w') as f:
        f.writelines(first_half)

    # Write the second half to a new file
    with open('second_half.txt', 'w') as f:
        f.writelines(second_half)


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
    parser = argparse.ArgumentParser(description='Web scraper')
    parser.add_argument('url', help='The URL of the website to scrape')
    parser.add_argument('-o', '--output', default='result.txt', help='The output file name')
    args = parser.parse_args()

    print('Scraping website...')
    # Get the text from the website
    text = get_text(args.url)

    #make a loading bar to show progress
    print('Scraping complete. Saving to file...')
    # Write the text to the output file
    if args.output:
        with open(args.output, 'w') as f:
            f.write(text)
    else:
        # Print the text with new lines after each element
        print('\n'.join(text.split('\n')))

    print('Done scraping!')

    answer = input('Would you like to summarize the text? (y/n): ')

    if answer == 'y':

        with open("result.txt", "r") as file:
            content = file.read()
            word_count = len(content.split())
            if word_count < 1200:
                print("The file contains {} words.".format(word_count))
                print('Summarizing...')
                print(summary.summarize_text(text))
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
                            print(summary.summarize_text(text))
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
                            print(summary.summarize_text(text))
                else:
                    print('Exiting...')
                    exit()

    else:
        print('Exiting...')
        exit()