# RAG_for_Voice_Assistant_Project

## Introduction : 

Ce projet a pour objectif d'intégrer un système RAG (Retrieval-Augmented Generation) à une application d'assistant virtuel existante, en utilisant une base de données vectorielle pour améliorer la récupération d'informations. L'objectif principal est de renforcer la capacité de l'assistant à générer des réponses précises et contextuellement pertinentes en interrogeant une base de connaissances, améliorant ainsi les interactions au-delà des capacités classiques des modèles de langage.

## Architecture : 

![image](https://github.com/user-attachments/assets/872e255e-9a75-4efe-9b76-8e2217696773)

Cette architecture se base sur l'intégration d'un système de génération augmentée par récupération (RAG) pour améliorer la précision et la pertinence des réponse. Voici comment cela fonctionne :

#### 1)Dataset :
Les données, provenant de Hugging Face, sont transformées en vecteurs d'embeddings à l'aide d'un modèle de création d'embeddings adapté, permettant une représentation numérique des informations du dataset.

 #### 2)Embeddings Vectoriels :
Les embeddings capturent la signification et la relation entre les concepts des données sources, facilitant leur recherche et leur comparaison.

 #### 3)Base de Données Vectorielle :
Ces vecteurs d'embeddings sont ensuite stockés dans une base de données vectorielle qui permet des recherches efficaces basées sur la similarité des vecteurs pour identifier les éléments les plus pertinents en réponse à une requête.

#### 4)Requête (Query) : 
Lorsque l'utilisateur pose une question, celle-ci est convertie en embeddings de requête. Ces vecteurs sont comparés aux vecteurs stockés dans la base de données vectorielle afin de récupérer les informations les plus pertinentes.

#### 5)Contexte Récupéré : 
la base de données vectorielle renvoie les résultats les plus proches de la requête, offrant un contexte pertinent tiré du dataset.

#### 6) Modèle LLM : 
Le modèle de langage utilise ce contexte pour générer une réponse adaptée, en tenant compte du contenu spécifique extrait de la base de données vectorielle.

#### 7)Réponse : 
L'assistant virtuel renvoie ensuite une réponse contextualisée et précise, issue de la combinaison du contexte récupéré et de la génération du modèle.

## Choix de la Base de Données Vectorielle : Qdrant

Dans le cadre de cette architecture RAG, j'ai choisi d'utiliser Qdrant comme base de données vectorielle pour stocker et rechercher les embeddings générés à partir du dataset. Ce choix a été motivé par plusieurs facteurs, en tenant compte des caractéristiques de Qdrant ainsi que d'autres options populaires comme Weaviate et Pinecone.

#### Qdrant VS Weaviate VS Pinecone :

Pour ce mini projet en local, j'ai choisi Qdrant en raison de sa facilité d'utilisation et de sa performance dans la gestion de données vectorielles. Contrairement à d'autres bases de données comme Weaviate et Pinecone, qui peuvent être plus adaptées à des déploiements en cloud ou à des cas d'utilisation plus complexes, Qdrant offre une configuration simple et des fonctionnalités robustes pour effectuer des recherches de similarité rapidement. Son architecture permet de travailler efficacement avec des ensembles de données de taille modérée, ce qui en fait un choix idéal pour des projets nécessitant une mise en œuvre rapide et une gestion performante des vecteurs.

![image](https://github.com/user-attachments/assets/c91fe699-c895-4fd9-b0a5-3cc9f668e585)

## Choix du modèle d'embeddings :

Au départ, j'ai choisi CamemBERT, qui est spécifiquement conçu pour le traitement des données en français et utilise des vecteurs de taille 768. Bien qu'il soit adapté aux corpus francophones, j'ai finalement opté pour le modèle MiniLM-L6-v2, qui utilise des vecteurs de taille 384. Ce modèle, basé sur une architecture transformer, est reconnu pour sa capacité à générer des embeddings de phrases de manière efficace, tout en préservant le sens contextuel. Mais, il n'a pas donné des résultats pertinents.

MiniLM-L6-v2 est optimisé pour offrir un bon équilibre entre performance et vitesse, ce qui le rend particulièrement adapté aux applications nécessitant des traitements rapides. Les tests que j'ai réalisés ont montré que ce modèle produisait des embeddings plus cohérents et pertinents, améliorant ainsi la qualité des résultats dans le cadre de ce projet. Toutefois, sa légèreté facilite son intégration dans des environnements locaux, rendant le processus de génération d'embeddings plus efficace.

## Choix du modèle LLM (Groq):

J'ai d'abord expérimenté avec les modèles FLAN-T5 et llama3.1. Malheureusement, ces essais n'ont pas donné les bonnes résultats. Le modèle T5 avait générer des réponses qui incluaient des éléments contextuels non pertinents, tandis que Llama-3.1 fournissait des réponses souvent inexactes ou déconnectées des attentes. 

Après avoir évalué ces performances, j'ai conclu que le meilleur choix pour mon application actuelle est Groq. Ce modèle s'est révélé plus adapté aux besoins, offrant des résultats plus précis et pertinents, tout en améliorant la qualité des interactions dans le cadre de mes tâches de génération de texte. Groq a donc été retenu comme la solution la plus efficace pour atteindre les objectifs fixés dans ce projet.

#### Quelques résultats avec LLma3 et T5 :

![image](https://github.com/user-attachments/assets/56aba8a7-66f5-45df-a19e-4dc5943dc6a3)

![image](https://github.com/user-attachments/assets/0ba0e0e6-443a-4247-a258-dcfe8db7da53)

![image](https://github.com/user-attachments/assets/a2c40ba8-a886-415b-b0ca-dd2f38da8f8e)

![image](https://github.com/user-attachments/assets/462a46c5-020b-4a54-84d0-0cfceb0c5dcb)

#### Quelques résultats avec Groq :

![image](https://github.com/user-attachments/assets/c46eeba7-a500-468d-aeb9-3aca3cee8d84)

## Optimisation des réponses du LLM :

Pour améliorer la qualité des réponses générées par le modèle LLM, j'ai intégré plusieurs techniques d'optimisation des prompts, notamment l'optimisation par exemple utilisation de : One-shot Prompting. 

L'idée est d'entraîner le modèle à fournir des réponses pertinentes en lui présentant un exemple clair et contextualisé avant de poser la question.

## Bonus : 

### 1) Implémentation d'un mécanisme de "fallback" lorsque le LLM ne trouve pas d'information pertinente dans le dataset

Dans mon projet, j'ai intégré un mécanisme de "fallback" pour gérer les situations où le modèle LLM ne parvient pas à trouver d'informations dans le dataset. Cela est particulièrement important pour garantir une bonne expérience utilisateur et éviter les réponses inexactes.

#### Fonctionnement du mécanisme de "fallback" : 

###### Extraction des contextes :
Lors de la récupération des contextes pertinents depuis la base de données (Qdrant), si aucun contexte n'est trouvé, la variable contexts sera vide.
###### Prompt conditionnel : 
Dans le prompt, j'indique clairement que si le modèle ne peut pas trouver d'informations précises, il doit donner une réponse standardisée : "Je ne sais pas". Cela évite des réponses inutiles ou déroutantes.
###### Gestion des réponses : 
Si les contextes récupérés sont vides, je vérifie cette condition avant de passer la question au modèle. Dans ce cas, je renvoie immédiatement "Je ne sais pas" pour garantir que l'utilisateur reçoit une réponse appropriée.

![image](https://github.com/user-attachments/assets/e596a65d-fcf9-4acb-b580-7d97f941860c)

### 2) Détection de silence : 

###### Amélioration de la détection de silence
Vérification du contenu du transcript : Assurer que le transcript n'est pas seulement vide ou rempli d'espaces.

###### Utilisation d'un seuil de silence : 

Implémentation une logique pour compter la durée de silence, en vérifiant si le temps écoulé dépasse le seuil défini.

## Observation et Remarques : 

Lors de mes tests de détection du son, j'ai rencontré certaines difficultés, notamment en ce qui concerne la précision de la reconnaissance des questions. En effet, lorsque je pose une question, le système ne parvient pas toujours à détecter correctement le contenu de la question, ce qui entraîne des interprétations erronées.

## Structure des fichiers : 

`- main.py` : Point d'entrée pour exécuter l'application.
  
`- voice_assistant.py` : Contient la logique principale pour gérer l'entrée audio, le traitement et la sortie.
  
`- text_to_speech.py` : Contient la fonction pour convertir le texte en parole.
  
`- ingest.py` : Pour ingérer des embeddings dans la base de données Qdrant.
  
`- rag.py` : Contient la logique pour le modèle RAG (Retrieval-Augmented Generation).

## Instruction d’utilisation : 

#### Prérequis
Assurez-vous d'avoir les outils et bibliothèques suivants installés :

Python 3.7 ou supérieur

Clé API Deepgram

Clé API Groq 

Packages Python requis : pyaudio, websockets, pyttsx3, dotenv, openai, ffmpeg-python

#####Installation

1. Clonez le dépôt :

bash

`cd voice-assistant`

2. Installez les packages requis :

bash

`pip install -r requirements.txt`

3. Configurez les variables d'environnement : Créez un fichier .env dans le répertoire racine avec le contenu suivant :

makefile

DEEPGRAM_API_KEY=""
GROQ_API_KEY=""

4.Installez FFmpeg : Assurez-vous que FFmpeg est installé et ajouté au PATH de votre système. Vous pouvez le télécharger à partir de FFmpeg Download.

5.Configuration de Qdrant

Exécutez Qdrant avec Docker : Assurez-vous que Docker est installé et en cours d'exécution. Lancez la commande suivante pour exécuter Qdrant :

bash

`docker run -p 6333:6333 qdrant/qdrant`

Accédez au tableau de bord de Qdrant : Ouvrez votre navigateur et accédez au lien suivant : http://localhost:6333/dashboard#/collections.

Ingestion des embeddings : Lancez le script d'ingestion pour commencer à ajouter des embeddings à la base de données :

bash

`python ingest.py`

5.Lancer l'application 
