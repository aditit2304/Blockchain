import hashlib
import json
import numpy as np
from datetime import datetime
from time import time
from uuid import uuid4
from flask import Flask
from flask import jsonify
from pprint import pprint
from merklelib import MerkleTree


class Block():
    def __init__(self,nonce,timestamp,dataList,prevhash='',hash=''):
        self.nonce=nonce
        self.timestamp=timestamp
        self.dataList=dataList # list of dictionary values
        self.prevhash=prevhash
        if hash == '':
            self.hash=self.calcHash()
        else:
             self.hash=hash

    def calcHash(self):
        block_string=json.dumps({"nonce":self.nonce,"timestamp":str(self.timestamp),"data":self.dataList,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def mineBlock(self,diffic):
        while(self.hash[:diffic] != "0"*diffic):
            self.nonce += 1
            self.hash=self.calcHash()
    def toDict(self):
        return {"nonce":self.nonce,"timestamp":str(self.timestamp),"dataList":self.dataList,"prevhash":self.prevhash,"hash":self.hash}


class BlockChain():
    def __init__(self):
        self.chain=[]
        self.pendingdata=[]
        self.mining_reward=100
        self.difficulty=4
        self.generateGenesisBlock()

    def generateGenesisBlock(self):
        dect={"nonce":0,"timestamp":'10/04/2021',"dataList":[{"from_address":None,"to_address":None,"data":0},],"hash":''}
        b=Block(**dect)
        self.chain.append(b.toDict())

    def getLastBlock(self):
        return Block(**self.chain[-1])

    def minePendingdata(self,mining_reward_address):
        block=Block(0,str(datetime.now()),self.pendingdata)
        block.prevhash=self.getLastBlock().hash
        block.mineBlock(self.difficulty)
        print("Block is mined to got reward", self.mining_reward)
        self.chain.append(block.toDict())
        
        self.pendingdata=[{"from_address":None,"to_address":mining_reward_address,"data":self.mining_reward},]

    def createdata(self,from_address,to_address,data):    
                self.pendingdata.append({
                        'from_address': from_address,
                        'to_address': to_address,
                        'data': data,
        })
    
    def isChainValid(self):
        for index in range(1,len(self.chain)):
            currb=Block(**self.chain[index])
            prevb=Block(**self.chain[index-1])
            if currb.hash != currb.calcHash():
                return False
            if currb.prevhash != prevb.hash:
                return False
        return True

    def calcdata(self,address):
        d = 0
        for index in range(len(self.chain)):
            dicList= self.chain[index]["dataList"]
            for dic in dicList:
                if dic["to_address"]==address:
                    d += dic["amount"]
                if dic["from_address"]==address:
                    d -= dic["amount"]
        return d
           


blockchain1=BlockChain()
ins = open( "data.txt", "r" )
array = []
for line in ins:
        line = line.rstrip('\n')
        li = list(line.split(" ")) 
        array.append(li)
ins.close()
l=list(array)     
blockchain1.createdata('add1','add2',l)
blockchain1.createdata('add2','add1',"thanku")
blockchain1.minePendingdata('demo')
#blockchain1.createdata('add1','add2',40)
#blockchain1.createdata('add2','add1',30)
#terblockchain1.minePendingdata('demo')

app=Flask(__name__)

node_id=str(uuid4()).replace('-','')

@app.route("/mine",methods=['GET'])
def mine():
    return "we'll mine a new block"

@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    return "we'll add a new transaction here"

@app.route('/chain',methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain1.chain,
        'length':len(blockchain1.chain),
    }
    return jsonify(response), 200

@app.route("/")
def hello():
    return "Hello, you are in the main page of the node"

if __name__=="__main__":
    app.run()
