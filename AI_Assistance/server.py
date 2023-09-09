from flask import Flask, jsonify, request
import os
import openai
from jproperties import Properties
import json
import random
from pymongo import MongoClient
app = Flask(__name__)
import constants
import os
import sys
from bson.json_util import dumps, loads
from bson import json_util
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
import matplotlib.pyplot as plt
import pandas as pd
import pymongo

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False
chat_history = []

@app.route('/showAnalysis/<query>')
def showAnalysis(query):
    lst_power_production = list(collection.find(filter={}, projection={"_id": 0, "ccy": 1, query: 1}))
    df_mongo = pd.DataFrame(lst_power_production)
    # Create DataFrame
    #df = pd.DataFrame(data)
    # Count the occurrences of each trade status
    status_counts = df_mongo[query].value_counts()
    print(status_counts)
    # Create bar chart
    plt.bar(status_counts.index, status_counts.values)
    # Add labels and title
    plt.xlabel(query)
    plt.ylabel('Count')
    plt.title('Distribution of '+ query)
    # Display the chart
    plt.show()

@app.route('/getTradeDetails/<query>')
def getTradeDetails(query):          
    myquery = {'tradeId': int(query)}    
    print(myquery)
    mydoc = collection.find(myquery)
    for trade in mydoc:
        print(trade)
        # list_cur = list(trade)
        # Converting to the JSON
        json_data = parse_json(trade) 
        print(json_data)
        return json_data
    return "Trade id "+query+" not found"

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/bookTrade/', methods=['POST'])
def bookTrade():
    print(request.get_json())
    data = json.loads(request.get_json())
    cmrName = data['cmrName']
    buySellIndicator = "Buy" if data['buySellIndicator'] == 1 else "Sell"
    ccy = data['ccy']
    ctr = data['ctr']      
    allInRate = data['allInRate']
    isInverted = data['isInverted']
    valueDate = data['valueDate']    

    ccyAmount = data['ccyAmount']
    ctrAmount = data['ctrAmount']
    notes = data['notes']
    typeOfTrade = "SPOT" if data['typeOfTrade'] == 1 else "FWD"

    tradeId = random.randint(6193279, 6977864)
    data['tradeId'] = tradeId
    updatePropertiesValues(data)
    return 'TradeId : '+ str(tradeId) +' is booked for currency pair '+ccy+"/"+ctr + " for customer "+cmrName+ " "

def updatePropertiesValues(data):    
    configs = Properties()
    configs["cmrName"] = data['cmrName']
    configs["buySellIndicator"] = "Buy" if data['buySellIndicator'] == 1 else "Sell"
    configs["ccy"] = data['ccy']
    configs["ctr"] = data['ctr']
    configs["allInRate"] = data['allInRate']
    configs["isInverted"] = "true" if data['isInverted'] == True else "False"
    configs["valueDate"] = data['valueDate']
     
    configs["ccyAmount"] = data['ccyAmount']
    configs["ctrAmount"] = data['ctrAmount']
    configs["notes"] = data['notes']
    configs["typeOfTrade"] = "SPOT" if data['typeOfTrade'] == 1 else "FWD"
   
    with open("./Client/tradeData.properties", "wb") as f:
        configs.store(f, encoding="utf-8")
    collection.insert_one(data)


@app.route('/getLiveRate/<query>')
def getLiveRate(query):
    result = chain({"question": query, "chat_history": chat_history})
    return result['answer']

@app.route('/getInfo/<query>')
def getInfo(query):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the GPT-3 model variant
        prompt=query,
        max_tokens=20  # Set the desired length of the generated text
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
    
