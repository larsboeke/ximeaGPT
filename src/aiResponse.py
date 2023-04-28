import openai
import pinecone
import os


api_key_path = "/home/lorenzboke/uni/ailean/src/api_key.txt"
openai.api_key_path = api_key_path

#Initialized Pinecone DB
pinecone.init(
        api_key="ddafaa1a-777c-4f6d-b61d-cc8f962ddf64",  
        environment="us-west4-gcp"  
    )

index = pinecone.Index('pdfreader')


#Get matching namespaces of Query
def getNamespaces(client_msg):
    #client message to embeddings
    client_msg_embedding = openai.Embedding.create(input=client_msg, engine='text-embedding-ada-002')['data'][0]['embedding']
    #query namspaces for top 5 matches
    namespaces = index.query([client_msg_embedding], top_k=5, include_metadata=True, namespace="pdf_names")
    #get actual namespace name from query result
    namespaces_text = [match['metadata']['text'] for match in namespaces['matches']]
    return namespaces_text


#Get matching embeddings and text for corresponding namespaces
def getResponseEmbeddings(client_msg, namespaces):

    #form query to embedding
    query_embedding = openai.Embedding.create(input=client_msg, engine='text-embedding-ada-002')['data'][0]['embedding']

    all_results = []

    #get matching top 5embeddings with text for each machting namespace
    for namespace in namespaces:
        result = index.query([query_embedding], top_k=5, include_metadata=True, namespace=namespace)
        for match in result['matches']:
            all_results.append(match)


    #sort all resulting embeddings by score, descending
    result_sorted= sorted(all_results, key=lambda x: x['score'], reverse=True)
    
    #take top 3 matching embeddings 
    resultsTop3 = result_sorted[:3]

    for context in resultsTop3:
        print(context['metadata']['text'])
    return resultsTop3

def generateResponse(result, client_msg):
    
    print("test")
    #Promt: Context from embeddings and clinet message as question
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": f"You are a helpful assistant that answer this question:'{client_msg}' with the given context: '{result}'."}]
    )
    
    return completion['choices'][0]['message']['content']


#main method for getting response from client message
def getResponse(client_msg):
    namespace = getNamespaces(client_msg)
    response_embeddings = getResponseEmbeddings(client_msg, namespace)
    response = generateResponse(response_embeddings, client_msg)

    return response
