import pandas as pd
import numpy as np
import random

from surprise import Dataset
from surprise import Reader
from surprise import KNNWithMeans

#DATAFRAME CREATION

mergeOrders = pd.read_csv('newdata/mergedOrders.csv')

allProducts = pd.read_csv('newdata/allProducts.csv')

custProdTable = pd.read_csv('newdata/mergedTable.csv')

result2 = pd.read_csv('newdata/preStackTable.csv')
result2 = result2.rename(columns={"0": "Frequency"})

productTable = pd.read_csv('newdata/productMatrix.csv')

# LIST OF ALL ORDERS IN LISTS FOR ITERATION
orderList = []
for i in mergeOrders['Order Number'].unique():
    individualOrder = mergeOrders.loc[mergeOrders['Order Number'] == i, ['Product_ID']]
    orderList.append(individualOrder['Product_ID'].tolist())

allProductList = allProducts['Product_ID'].tolist()

productList1 = productTable['Product_ID1'].tolist()
productList2 = productTable['Product_ID2'].tolist()

#FUNCTIONS AVAILABLE
def custToProdList(customerId):
    return(mergeOrders.loc[mergeOrders['Customer_ID'] == customerId, 'Product_ID'])

def mostFrequent(customerId):
    return custToProdList(customerId).value_counts().idxmax()

def mostRecent(customerId):
    return custToProdList(customerId).iloc[-1]

def randomPurchase(customerId):
    listRange = len(custToProdList(customerId))
    randNum = random.randrange(0,listRange-1)
    return custToProdList(customerId).iloc[randNum]

def custToProd(customerId,choice):
    if choice == 'frequent':
        return mostFrequent(customerId)
    if choice == 'recent':
        return mostRecent(customerId)
    if choice == 'random':
        return randomPurchase(customerId)

#ML Functions 

def custToProdRec(customerID,productID):
    prediction = algo.predict(customerID, productID)
    pred = prediction.est
    return pred

def custReco(customerID):
    recos = {}
    for i in allProductList:
        rating = custToProdRec(customerID,i)
        if rating < 0.99:
            recos[i] = rating
    sortedRecos = {k: v for k, v in sorted(recos.items(), key=lambda item: item[1], reverse=True)}
    return list(sortedRecos)[0:6]

def prodToProdRec(productID1,productID2):
    prediction = algo2.predict(productID1, productID2)
    pred = prediction.est
    return pred

def prodReco(productID):
    recos = {}
    for i in allProductList:
        if productID != i:
            rating = prodToProdRec(productID,i)
            recos[i] = rating
    sortedRecos = {k: v for k, v in sorted(recos.items(), key=lambda item: item[1], reverse=True)}
    return list(sortedRecos)[0:6]

#Machine Learning Training for Customer to Product

def algoCustToProd():
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(result2[["Customer_ID", "Product_ID", "Frequency"]], reader)

    # To use item-based cosine similarity
    sim_options = {
        "name": "cosine",
        "user_based": False,  # Compute  similarities between items
    }

    algo = KNNWithMeans(sim_options=sim_options)

    trainingSet = data.build_full_trainset()

    algo.fit(trainingSet)

    return algo

def algoProdToProd():
    reader2 = Reader(rating_scale=(0, productTable['Frequency'].max()))
    data2 = Dataset.load_from_df(productTable[["Product_ID1", "Product_ID2", "Frequency"]], reader2)

    # To use item-based cosine similarity
    sim_options = {
        "name": "cosine",
        "user_based": False,  # Compute  similarities between items
    }

    algo2 = KNNWithMeans(sim_options=sim_options)

    trainingSet2 = data2.build_full_trainset()

    algo2.fit(trainingSet2)

    return algo2

#Algorithms
algo = algoCustToProd()
algo2 = algoProdToProd()


def test():

    print(mostRecent(9400009))
    print(prodReco(101010201))
    print(custReco(9400009))

test()