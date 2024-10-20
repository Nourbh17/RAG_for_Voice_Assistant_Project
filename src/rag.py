import getpass
import os
import torch
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import getpass


# Check for GROQ API key and prompt for it if not found
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

# Initialize the ChatGroq model
def load_croq():
    croq_model = ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return croq_model

# Load the SentenceTransformer model
def load_sentence_model():
    model_name = 'all-MiniLM-L6-v2'
    return SentenceTransformer(model_name)

# Function to retrieve embeddings with SentenceTransformer
def get_embedding(text, model):
    # Use SentenceTransformer to get the embedding
    embeddings = model.encode(text, convert_to_tensor=True)
    return embeddings.numpy()

# Retrieve relevant contexts from Qdrant
def retrieve_context(question, qdrant_client, collection_name, model, top_k=3):
    embedding = get_embedding(question, model)

    # Query Qdrant to retrieve the nearest points
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=embedding.tolist(),
        limit=top_k
    )

    # Extract contexts from the search results
    contexts = [hit.payload['context'] for hit in search_result]
    return contexts

# Main function to perform retrieval and generation
def get_ai(q):
    # Initialize Qdrant client
    qdrant_client = QdrantClient(host="localhost", port=6333)
    collection_name = "RAG_dataset2"

    # Load models: ChatGroq and SentenceTransformer
    croq_model = load_croq()
    sentence_model = load_sentence_model()

    # User input (question)
    # We can use here to write question if we want to use the rag here without the voice assistant
    # q = "Quel événement majeur se déroulera en France en 2024, et quel rôle joue Air France dans cet événement ?"

    # Retrieve the most relevant contexts
    contexts = retrieve_context(q, qdrant_client, collection_name, sentence_model)
    if not contexts:
        print("Réponse générée: Je ne sais pas.")
        return

    # Combine question and context for generation
    input_text = f"""
                    Voici une question et des contextes pertinents extraits d'une base de données. 
                    Si vous ne trouvez pas la réponse exacte dans le contexte fourni, répondez simplement : "Je ne sais pas".

                    ### Exemple
                    Contexte: ["xx Résultats annuels 2023 29 février 2024 Demande soutenue se traduisant par une progression de la marge opérationnelle à 5,7% Fonds propres du Groupe restaurés •Capacité du Groupe à 93% du niveau de 2019 et coefficient de remplissage à 87% •Chiffre d’affaires total du Groupe à 30,0 mds€, en hausse de 14% par rapport à l’année précédente •Résultat d’exploitation à 1,7 md€, avec une marge opérationnelle à 5,7%, en hausse de +1,2pt par rapport à l’année précédente •Résultat net à 0,9 md€, permettant un retour à des fonds propres positifs à 0,5 md€ pour la première fois depuis 2019 •Dette nette réduite de 1,3 md€ par rapport à la fin d’année 2022 se traduisant par un ratio de dette nette/EBITDA à 1,2x. Liquidités à 10,5 mds€ •2 notations de crédit inaugurales soulignant la poursuite de la transformation du Groupe et une structure financière améliorée Le Directeur général du Groupe, M. Benjamin Smith a déclaré: “En 2023, nous avons tenu nos engagements en réalisant de solides performances opérationnelles et financières, tout en maintenant notre position de groupe aérien de référence en matière de développement durable. Parmi nos principales réalisations, nous sommes satisfaits d’avoir pu renforcer davantage notre bilan et d’avoir restauré les fonds propres du Groupe. Nous avons également passé une commande historique de cinquante Airbus A350, assortie de droits d'acquisition pour quarante appareils supplémentaires, accélérant ainsi le renouvellement de notre flotte. Ces avions de dernière génération permettent une réduction de la consommation de carburant, des émissions de CO2 et de l’empreinte sonore. Ils offrent également une expérience plus agréable à nos clients. Nous avons par ailleurs confirmé notre position de premier utilisateur mondial de carburant d'aviation durable, démontrant ainsi notre détermination à tirer le plein parti de ce levier décarbonation pour atteindre nos objectifs en matière de développement durable. Je tiens à remercier tous les employés d'Air France-KLM qui ont travaillé sans relâche pour rendre ces réalisations possibles. En 2024, l'une de nos priorités sera de continuer à renforcer notre performance, en poursuivant la mise en œuvre de notre stratégie. Cette année sera doublement spéciale pour nous, avec d’une part le 20e anniversaire d'Air France-KLM, et la tenue des Jeux olympiques et paralympiques de Paris 2024 en France, dont Air France est fière d'être le sponsor officiel. Nous sommes impatients d'accueillir le monde - athlètes, délégués, supporters et autres - en France et à bord de nos avions pour célébrer cet évènement planétaire.” Groupe Air France-KLM Résultats annuels 2023 1"]
                    Question: Quel est le chiffre d'affaires total du Groupe Air France-KLM pour l'année 2023 ?
                    Réponse: Le chiffre d'affaires total du Groupe Air France-KLM pour l'année 2023 est de 30,0 milliards d'euros.

                    ### Maintenant à vous:
                    Contexte: {contexts}
                    Question: {q}
                    Réponse:"""

    # Prepare messages for ChatGroq
    messages = [
        (
            "system",
            "Vous êtes un assistant utile qui répond aux questions en utilisant le contexte fourni.",
        ),
        ("human", input_text),
    ]

    # Generate response using ChatGroq
    ai_msg = croq_model.invoke(messages)
    
    # Display the response
    print(f"Question: {q}\nRéponse: {ai_msg.content}")

# if __name__ == "__main__":
#     get_ai()
