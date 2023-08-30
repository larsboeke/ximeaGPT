from pydantic import BaseModel, Field

import openai
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from data_package.SQL_Connection_Provider.SQLConnectionProvider import SQLConnectionProvider
import data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider as MongoDBConnectionProvider
import html
import json
from data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider import MongoDBConnectionProvider
from data_package.Pinecone_Connection_Provider.PineconeConnectionProvider import PineconeConnectionProvider
from data_package.Token_Counter.TokenCounter import TokenCounter
load_dotenv()


def get_sources(self, query, namespaces):
    index = PineconeConnectionProvider().initPinecone() #
    #initialize mongoDB                 
    col = MongoDBConnectionProvider().initMongoDB()
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
    used_tokens = query_embedding["usage"]["total_tokens"]

    filtered_query_embedding = query_embedding['data'][0]['embedding']
    #queries pinecone in namespace "manuals"
    
    matches_content = []
    matches_sources = []
    
    for namespace, num_sources in namespaces:

        pinecone_results = index.query([filtered_query_embedding], top_k=num_sources, include_metadata=True, namespace=namespace)
        unique_pinecone_results = pinecone_results['matches']
        
        #get matches from mongoDB for IDs
        for id in unique_pinecone_results:
            idToFind = ObjectId(id['id'])
            match = col.find_one({'_id' : idToFind})
            matches_content.append(match['content'])
            source = {'id': str(match['_id']), 'content': match['content'], 'metadata': match['metadata']}
            matches_sources.append(source)

    return matches_content, matches_sources, used_tokens


def get_extra_sources(self, source):
    result = []
    if source["metadata"]["type"] == 'email' or source["metadata"]["type"] == 'ticket':
        mongodb_connection = MongoDBConnectionProvider().initMongoDB()
        source_id = source["metadata"]["source_id"]
        order_id = source["metadata"]["order_id"]
        query = {
            "metadata.source_id": source_id,
            "metadata.order_id": order_id + 1
        }
        source_extra = mongodb_connection.find(query)
        result = list(source_extra)
        if result:
            result = result[0]
            result["id"] = result.pop("_id")
            result["id"] = str(result["id"])
    return result


class QueryEmailsAndTickets(BaseModel):
    name = "Query Emails and Tickets"
    description = "This function answers the users query only with information of from the support eamils and tickets of XIMEA. Therefore use cases for this tool are when the user asks for the email or ticket history for a case. This tool provides infomation about things that typically get negotiated in emails or tickets, like contract datails ... Keep in mind that data from technical manuals is not included!"

    def _run(self, query: str) -> str:
        namespaces = [("tickets", 1), ("emails", 1)]
        function_response, sources, tokens = get_sources(
            query, 
            namespaces=namespaces
        )
        return function_response

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
    


class QueryManuals(BaseModel):
    name = "Query Technical Manuals"
    description = "This function will give you informations from XIMEA's technical manuals. The manuals contain information about camera/camera families including hardware specification, system requirements, instalation of related software drivers."

    def _run(self, query: str) -> str:
        namespaces = [("manuals", 2)]
        function_response, sources, tokens = get_sources(query = query, namespaces = namespaces)
        return function_response

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
