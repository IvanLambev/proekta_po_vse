import nlpcloud


def summarize_text(text_to_summarize):
    client = nlpcloud.Client("bart-large-cnn", "f771bc4e9647a3607f917eae5b5f609f7b320219", gpu=False, lang="en")
    response = client.summarization(text_to_summarize, size="long")
    summary_text = response['summary_text']
    return summary_text


def translate_text(text_to_translate, target_lang):
    client = nlpcloud.Client("t5-small", "f771bc4e9647a3607f917eae5b5f609f7b320219", gpu=False, lang="en")
    response = client.translation(text_to_translate, target_lang)
    translated_text = response['translated_text']
    return translated_text
