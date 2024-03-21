from gensim.parsing.preprocessing import strip_punctuation, strip_numeric, strip_short, stem_text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')

def clean_text(sentence_batch) -> dict:
    # extrae el texto de la entrada
    text_list = sentence_batch['text']

    cleaned_text_list = []
    for text in text_list:
        # Convierte el texto a minúsculas
        text = text.lower()

        # Elimina URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        # Elimina las menciones @ y '#' de las redes sociales
        text = re.sub(r'\@\w+|\#\w+', '', text)

        # Elimina los caracteres de puntuación
        text = strip_punctuation(text)

        # Elimina los números
        text = strip_numeric(text)

        # Elimina las palabras cortas
        text = strip_short(text, minsize=4)

        # Elimina las palabras comunes (stop words)
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [word for word in word_tokens if word not in stop_words]

        cleaned_text_list.append(filtered_text)

    # Devuelve el texto limpio
    return {'text': cleaned_text_list}