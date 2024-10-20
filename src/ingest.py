import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

# Fonction pour générer les embeddings
def get_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')  
    embeddings = model.encode(text)  # Generate embeddings
    return embeddings

# Fonction principale pour ingérer les données
def main():
    splits = {'train': 'data/train-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
    df = pd.read_parquet("hf://datasets/sujet-ai/Sujet-Financial-RAG-FR-Dataset/" + splits["train"])

    
    # Initialiser le client Qdrant
    qdrant_client = QdrantClient(host="localhost", port=6333)
    
    # Créer une collection dans Qdrant
    collection_name = "RAG_dataset2"
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=rest.VectorParams(size=384, distance="Cosine")  # Change size to match the embedding dimension
    )

    
    # Ajouter les embeddings au dataset
    for idx, row in df.iterrows():
        question = row['question']
        context = row['context']
        
        # Générer l'embedding pour le contexte ou la combinaison des deux
        embedding = get_embedding(question + " " + context)
        
        # Ajouter l'embedding à Qdrant
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                rest.PointStruct(
                    id=idx,  # L'ID unique pour chaque ligne
                    vector=embedding.tolist(),
                    payload={
                        "question": question,
                        "context": context
                    }
                )
            ]
        )
    print("Données ingérées avec succès.")


if __name__ == "__main__":
    main()
