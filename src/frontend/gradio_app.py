import gradio as gr
import pandas as pd
import os
import chromadb
from chromadb.utils import embedding_functions
from chromadb.api.models import Collection
from typing import List
from utils import make_a_query

def load_collection(path: str, collection_name: str) -> Collection:
    """Loads collection from vector database.

    Args:
        path: Path to Chroma's data.
        collection_name: Collection's name to load.

    Raises:
        FileNotFoundError: If not found the path to Chroma's data.

    Returns:
        Collection with data.
    """
    # chroma_client = chromadb.Client()
    try:
        client_persistent = chromadb.PersistentClient(path=path)
    except Exception:
        raise FileNotFoundError(f"Path for database vector may not exists {path}")

    if not any([collection_name == collection.name for collection in client_persistent.list_collections()]):
        raise FileNotFoundError(f"Collection may not exists {collection_name}")
    
    if "openai" in collection_name:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name = 'text-embedding-ada-002'
        )
    else:
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    db_embeddings = client_persistent.get_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    return db_embeddings

def get_available_collections() -> List[str]:
    """Gets all available collections.

    Returns:
        List with available collections names.
    """
    client_persistent = chromadb.PersistentClient(path='./data/data_embeddings') 
    return [collection.name for collection in client_persistent.list_collections()]

def make_query_wrapper(
        collection_name: str, 
        query: str,
        n_results: int
) -> pd.DataFrame: 
    """
    Wrapper for make query function for Gradio interface.

    Args:
        collection_name: Collection name from Chroma's data.
        query: Description.
        n_results: Number of results to retrieve.

    Returns:
        DataFrame with results.
    """
    db = load_collection(path='./data/data_embeddings', collection_name=collection_name)
    return make_a_query(
        query=query,
        db = db,
        n_results=int(n_results)
    )

def main() -> None:
    """
    Main of the Gradio's app.
    """
    collections = get_available_collections()
    interface = gr.Interface(
        fn=make_query_wrapper,
        inputs=[
            gr.Dropdown(choices=collections, label = "Available Collections"),
            gr.Textbox(lines=5, placeholder="Enter your description...", label="Query"),
            gr.Number(minimum=1, maximum=10, value=3, label="Number of results")
        ],
        outputs=gr.Dataframe(type="pandas", label="Results", style={"font-size": "12px"}),
        title="Movies Search Engine",
        description="Enter a description to get movies recommendations.",
        style={"width": "300px"}
    )

    # Launch the interface
    interface.launch(debug=True)

if __name__ == "__main__":
    main()