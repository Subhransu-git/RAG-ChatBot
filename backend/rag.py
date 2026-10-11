import faiss
import pickle
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer("all-MiniLM-L6-v2",local_files_only=True)

index = faiss.read_index("index.faiss")
documents, metadata = pickle.load(open("docs.pkl", "rb"))

def retrieve_context(query, k=2):
    query_embedding = embed_model.encode(
        [query],
        normalize_embeddings=True
    )

    distances, indices = index.search(query_embedding, k)

    if indices is None or len(indices[0]) == 0:
        return "", []

    contexts = []
    sources = []

    for idx, dist in zip(indices[0], distances[0]):

       
        def retrieve_context(query, k=3):
            query_embedding = embed_model.encode(
                [query],
                normalize_embeddings=True
            )

            distance, indices = index.search(query_embedding, k)

            contexts = []
            sources = []

        for idx in indices[0]:
            contexts.append(documents[idx])
            sources.append(metadata[idx])

        return "\n".join(contexts),list(set(sources))


        

    if not contexts:
        return "", []

    return "\n".join(contexts), list(set(sources))
