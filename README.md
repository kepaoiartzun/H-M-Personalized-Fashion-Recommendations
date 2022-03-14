# H & M Personalized Fashion Recommendations

The objective of this project is to create a personalized article recommender to each customer, based on the kaggle competition *H&M Personalized Fashion Recommendations* data (https://www.kaggle.com/c/h-and-m-personalized-fashion-recommendations).

## Resolution of the problem

There are a lot of recommendation models, but this system will use a simple procedure to get the personalized recomendations:
- Firstly, the 2019 autumn transactions are going to be analyzed, and a dataset created with the similarity between customers.
- In autumn 2020, each customer is going to be recommended with the articles that similar customers bought in autumn 2020, but they did not.

**Procedure:** 
- The transactions will be saved in a neo4j graph: each customer or article is going to be a node, and a customer and an article node will be related if the customer bought the article (there will be a relationship for each time a cutomer bought an article).
- Using the *Node Similarity* algorithm from the *neo4j Graph Data Science* libray (https://neo4j.com/docs/graph-data-science/current/algorithms/node-similarity/), the similarity between each customer node is going to be saved. The algorithm only compares each node that has outgoing relationships with each other such node, and all the relationships between nodes are going from a customer to an article node, so the algorithm will only compute the similarity values for customer pairs.
- Once saved the similarity data, another graph is going to be created in the same way, but with the transactions with the first 22 days of 2020 autumn. 
- Each customer is going to be recommended with the articles that similar customers bought in autumn 2020, but they did not.

## Notes
- Obviouly, the customers that did not bought any article in autumn 2019 will not have personalized recommendations with this system.
- I worked in this proyect locally and the dataset was huge, so I had to reduce the dataset keeping the most sold articles to recommend, and the customers who bought the most to be recommended.
- The project contains three files: The tables to work with are created in *preprocessing.ipnb*, the *auxiliars.py* script contains a class that is going to be used as the driver to manage the neo4j graph database, and the *recommendations.ipynb* file contains the procedure to get the recommendations.