import chromadb

chroma_client = chromadb.Client()
client_persistent = chromadb.PersistentClient(path='./data/data_embeddings')