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



