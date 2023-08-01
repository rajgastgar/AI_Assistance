from flask import Flask, jsonify, request
import os
import openai
openai.api_key="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"
from jproperties import Properties
import json
import random
from pymongo import MongoClient
app = Flask(__name__)
import constants
import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False
chat_history = []

@app.route('/bookTrade/', methods=['POST'])
def bookTrade():
    print(request.get_json())
    data = json.loads(request.get_json())
    cmrName = data['cmrName']
    buySellIndicator = "Bye" if data['buySellIndicator'] == 1 else "Sell"
    ccy = data['ccy']
    ctr = data['ctr']      
    allInRate = data['allInRate']
    isInverted = data['isInverted']
    valueDate = data['valueDate']    
    tradeId = random.randint(6193279, 6977864)
    data['tradeId'] = tradeId
    updatePropertiesValues(data)
    return 'TradeId : '+ str(tradeId) +' is booked for currency pair '+ccy+"/"+ctr + " for customer "+cmrName+ " "

def updatePropertiesValues(data):    
    configs = Properties()
    configs["cmrName"] = data['cmrName']
    configs["buySellIndicator"] = data['buySellIndicator'] 
    configs["ccy"] = data['ccy']
    configs["ctr"] = data['ctr']
    configs["allInRate"] = data['allInRate']
    configs["isInverted"] = "true" if data['isInverted'] == True else "False"
    configs["valueDate"] = data['valueDate']
    collection.insert_one(data)
    with open("./Client/tradeData.properties", "wb") as f:
        configs.store(f, encoding="utf-8")

@app.route('/getLiveRate/<query>')
def getLiveRate(query):
    result = chain({"question": query, "chat_history": chat_history})
    return result['answer']

@app.route('/getInfo/<query>')
def getInfo(query):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the GPT-3 model variant
        prompt=query,
        max_tokens=50  # Set the desired length of the generated text
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

if __name__ == "__main__":
    
    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        global index
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
        loader = DirectoryLoader("data/")
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])
    
    chain = ConversationalRetrievalChain.from_llm(
     llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3),
     retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    
    try:
        client = MongoClient('localhost', 27017)
        print("Connected successfully!!!")
    except:  
        print("Could not connect to MongoDB")
    
    # database
    my_db = client['mydb']

    print("List of databases after creating new one")
    print(client.list_database_names())

    # Created or Switched to collection names: my_gfg_collection
    global collection
    collection = my_db.TradeDetails
    app.run(debug=True)
