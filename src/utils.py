import pandas as pd
from chromadb.api.models.Collection import Collection

def make_a_query(
        query: str,
        db: Collection,
        n_results: int = 3
) -> pd.DataFrame:
    """
    Makes a query into Embedding Database through semantic search. 

    Args:
        query: Query as string.
        db: Collection (Embedding database).
        n_results: Number of results to retrieve. Defaults to 3.

    Returns:
        DataFrame with results.
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