import gradio as gr
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from chromadb.api.models import Collection
from src.utils import make_a_query

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
    chroma_client = chromadb.Client()
    try:
        print(chromadb.__version__)
        client_persistent = chromadb.PersistentClient(path=path) #'../data/data_embeddings'
    except:
        raise FileNotFoundError(f"Path for database vector may not exists {path}")

    sentence_transformer_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    db_embeddings = client_persistent.get_or_create_collection(
        name=collection_name, 
        embedding_function= sentence_transformer_function
    )

    return db_embeddings

def make_query_wrapper(
        collection_name: str, 
        query: str,
        n_results: int
) -> pd.DataFrame: 
    db = load_collection(path='./data/data_embeddings', collection_name=collection_name)
    return make_a_query(
        query=query,
        db = db,
        n_results=int(n_results)
    )

def main():
    """
    Main of the Gradio's app.
    """
    db = load_collection('./data/data_embeddings', 'movies_db_embeddings')
    interface = gr.Interface(
        fn=make_query_wrapper,
        inputs=[
            gr.Textbox(lines=5, placeholder="Collection name", label="Collection name"),
            gr.Textbox(lines=5, placeholder="Enter your description...", label="Query"),
            gr.Number(minimum=1, maximum=10, value=3, label="Número de resultados")
        ],
        outputs=gr.Dataframe(type="pandas", label="Resultados"),
        title="Buscador de pelí­culas",
        description="Introduce tu consulta, selecciona un género y define una puntuación mí­nima para buscar pelí­culas.",
    )

    # Launch the interface
    interface.launch()

if __name__ == "__main__":
    main()