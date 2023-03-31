import openai
import argparse

# Set up OpenAI API credentials
openai.api_key = "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"

# Define function to summarize text using OpenAI API
def summarize_text(text):
    # Use OpenAI API to summarize the text

    print("Summarizing text...")

    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize the following text to 100 words:\n{text}\n---\nSummary:",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Return the summarized text
    return response.choices[0].text.strip()

if __name__ == "__main__":

    #welcome message big "scraper"
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
    parser = argparse.ArgumentParser(description='Text summarizer')
    parser.add_argument('input_file', help='The input file name')
    parser.add_argument('-o', '--output', default='summary.txt', help='The output file name')
    args = parser.parse_args()

    # Read the text from the input file
    print("Reading text from file...")
    with open(args.input_file, 'r') as f:
        text = f.read()

    # Summarize the text using the OpenAI API
    summary = summarize_text(text)

    # Write the summary to the output file
    if args.output:
        with open(args.output, 'w') as f:
            f.write(summary)
    else:
        # Print the summary
        print(summary)

    print("Done!")