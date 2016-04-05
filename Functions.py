import numpy as np
import json
import matplotlib as mpl
from matplotlib import pyplot as plt
import sklearn as sk
import os
from collections import Counter

os.chdir('C:\Users\Simas\Desktop')

with open("LunyaApril2.json") as data_file:    
    dataFull = json.load(data_file)

data = dataFull['results']

del data[337]
fullI = list()
fullO = list()
for i in data:
    oI,oO = orderItems(i)
    fullI.append(oI)
    fullO.append(oO)

#Trim bullshit responses
def removeGarbage(data):
    hold = list(data)
    count = 0
    for i in data:
        if i['remainingBudget']==1000:
            del hold[count]
        else:
            count += 1
    return hold

#Takes results and reorders the chosen items and their picking order    
def orderItems(dataClip):
    l = len(dataClip['itemOrder'])
    outItems = np.zeros(l)
    outOrder = np.zeros(l)
    count = 0
    for i in dataClip['itemOrder']:
        outItems[i] = dataClip['itemsPicked'][count]
        outOrder[i] = dataClip['orderPicked'][count]
        count += 1
    return outItems,outOrder




#Goes through order picked and counts each order place, 
#returns an array of out[rank][item number], 
#rank 0 is all 0
#Takes in ordered array of orders, ie. fullO
def top10Pick(orderedOrder):
    topHold = np.zeros([11,len(orderedOrder[0])])
    for i in range(len(orderedOrder)):
        for j in range(len(orderedOrder[0])):
            val = orderedOrder[i][j]
            if val > 0 and val<11:
                topHold[val,j]+=1
    return topHold

#Organizes data based on purchase history,
#0:0, 1:1-2. 2:3-4, 3:5+    
def previousPurchase(data):
    holdI = np.zeros([4,len(data[0]['itemOrder'])])
    holdO = np.zeros([4,len(data[0]['itemOrder'])])
    for i in data:
        if i.has_key('userPieces'):
            name = i['userPieces']
            oI, oO = orderItems(i)
            if name == ' 0':
                holdI[0] = [sum(x) for x in zip(holdI[0],oI)]
                holdO[0] = [sum(x) for x in zip(holdO[0],oO)]
            elif name == '1-2':
                holdI[1] = [sum(x) for x in zip(holdI[1],oI)]
                holdO[1] = [sum(x) for x in zip(holdO[1],oO)]
            elif name == '3-4':
                holdI[2] = [sum(x) for x in zip(holdI[2],oI)]
                holdO[2] = [sum(x) for x in zip(holdO[2],oO)]
            elif name == '5+':
                holdI[3] = [sum(x) for x in zip(holdI[3],oI)]
                holdO[3] = [sum(x) for x in zip(holdO[3],oO)]
            else:
                pass
    return holdI,holdO
  
#Takes input of an item number and returns a ranked list of correlated item numbers  
def findCorrelations(data,itemnumber):
    fullI = list()
    for i in data:
        oI,oO = orderItems(i)
        fullI.append(oI)
    hold = np.zeros(len(fullI[0]))
    for i in fullI:
        if i[itemnumber]==1:
            hold = [sum(x) for x in zip(hold,i)]
    hold = sorted(range(len(hold)), key=lambda k: hold[k])
    hold = hold[::-1]
    del hold[0]
    return hold

#Runes through the whole data and returns the top n correlations for all the data
#Use a histogram to plot the counts        
def topCorrelations(data,n=15):
    hold = list()
    for i in range(len(data[0]['itemOrder'])):
        hold.append(findCorrelations(data,i)[0:n])
    hold = [item for sublist in hold for item in sublist] 
    return hold

def bestItems(data,n=15):
    tC = topCorrelations(data,n)
    count = Counter(tC).most_common()
    minCount = count[0][1]*0.30
    out = list()
    for i in count:
        if i[1]>minCount:
            out.append(i[0])
    return out
           
def itemOrder(orderedOrder,n):
    out = list()
    for i in orderedOrder:
        if i[n] >=0:
            out.append(i[n])
    return out
    