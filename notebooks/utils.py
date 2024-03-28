from gensim.parsing.preprocessing import strip_punctuation, strip_numeric, strip_short, stem_text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')

def clean_text(sentence_batch) -> dict:

    # Extracts text from the batch
    text_list = sentence_batch['text']

    cleaned_text_list = []
    for text in text_list:
        # Text to lower
        text = text.lower()

        # Delete URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        # Delete mentions @ and '#' from social media
        text = re.sub(r'\@\w+|\#\w+', '', text)

        # Delete punctuation
        text = strip_punctuation(text)

        # Delete numbers
        text = strip_numeric(text)

        # Delete short words
        text = strip_short(text, minsize=4)

        # Delete stop words
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [word for word in word_tokens if word not in stop_words]

        cleaned_text_list.append(filtered_text)

    return {'text': cleaned_text_list}