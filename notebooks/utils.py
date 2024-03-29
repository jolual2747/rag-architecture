from gensim.parsing.preprocessing import strip_punctuation, strip_numeric, strip_short, stem_text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from chromadb.api.models.Collection import Collection
import re
import nltk
from typing import List

def download_nltk_resources(resources: List[str]) -> None:
    """Downloads nltk resources if not exists locally.

    Args:
        resources: List of resources.
    """
    for resource in resources:
        try:
            nltk.data.find(resource)
        except:
            print(f"Resource {resource} not found! Proceeding to download it...")
            nltk.download(resource)

def clean_text(sentence_batch) -> dict:
    """Cleans text in batch.

    Args:
        sentence_batch: Batch of data.

    Returns:
        dict: Cleaned text.
    """
    # Downloads nltk resources if not exits
    download_nltk_resources(resources=['corpora/stopwords', 'tokenizers/punkt'])

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

def make_a_query(
    query: str,
    db: Collection,
    n_results: int = 3
) -> pd.DataFrame:
    """Make a query to a vector store and retrieve results by semantic search.

    Args:
        query: Query.
        db: Vector database.
        n_results: N results to retrieve.

    Returns:
        DataFrame: DataFrame with metadata.
    """
    results = db.query(
        query_texts=[query],
        n_results=n_results
    )

    response_data = []

    for response in results["metadatas"][0]:
        response_data.append(
            {
                'Title' : response["movie title"],
                'Overview' : response["Overview"],
                'Director' : response["Director"],
                'Genre' : response["Generes"],
                'Rating' : response["Rating"]
            }
        )
    return pd.DataFrame.from_records(response_data)