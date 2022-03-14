from neo4j import GraphDatabase
import pandas as pd

class graphDriver:
    "This class will contain the methods to manage the neo4j database needed in the system"

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    

    def close(self):
        self.driver.close()
    
    def clear_database(self):
        session = self.driver.session()
        query1 = """
            match (a)-[r]->() delete a, r
        """
        query2 = """
            match (a) delete a
        """
        session.run(query1)
        session.run(query2)
        session.close()
        

    def create_customer_node(self, customer_id):
        session = self.driver.session()
        query = f"""
            CREATE (c:Customer {{customer_id:'{customer_id}'}})
        """ 
        session.run(query)
        session.close()
    
    def create_article_node(self, article_id):
        session = self.driver.session()
        query = f"""
            CREATE (a:Article {{article_id:'{article_id}'}})
        """ 
        session.run(query)
        session.close()
        
    def create_transaction(self, customer_id, article_id, price, t_dat):
        session = self.driver.session()
        query = f"""
            MATCH (c:Customer), (a:Article)
            WHERE c.customer_id = '{customer_id}' and a.article_id = '{article_id}'
            CREATE (c)-[r:Bought {{prince:{price}, t_dat:'{t_dat}'}}]->(a)
        """
        session.run(query)
        session.close()
    
    def get_articles_bought_by(self, customer_id):
        session = self.driver.session()
        query = f"""
            MATCH (c:Customer)-[r:Bought]->(a:Article) 
            WHERE c.customer_id = '{customer_id}' 
            RETURN a
        """
        result = session.run(query).data()
        session.close()
        return list(pd.json_normalize(result)['a.article_id'])
    
    def get_customer_similarity(self):
        session = self.driver.session()
        query1 = """
            CALL gds.graph.create('transactionGraph', ['Customer', 'Article'], 'Bought')
        """
        query2 = """
            CALL gds.nodeSimilarity.stream('transactionGraph') 
            YIELD node1, node2, similarity 
            RETURN node1, node2, similarity
        """
        query3 = """
            CALL gds.graph.drop('transactionGraph') yield graphName
        """
        query4 = """
            MATCH (c:Customer) return ID(c), c.customer_id
        """
        session.run(query1) # Create graph
        result1 = session.run(query2).data() # Node Similarity Algorithm
        session.run(query3) # Drop graph
        result2 = session.run(query4).data() # Get node ID and cutomer_id relations
        session.close()

        df2 = pd.json_normalize(result2) # create df with each node id and customer_id pairs

        return pd.json_normalize(result1).replace(dict(zip(df2['ID(c)'], df2['c.customer_id']))).rename(columns={'node1':'customer_1_id', 'node2':'customer_2_id'})


            
