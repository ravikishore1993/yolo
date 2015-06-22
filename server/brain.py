from pybrain.datasets            import SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
import numpy as np
import pickle
from pybrain.structure           import TanhLayer
from pybrain.structure           import SigmoidLayer
import os
from sklearn                     import decomposition
import csv
from pandas                      import DataFrame
import pandas                    
# TODO: Remove the hardcoded part once synced up
pca = decomposition.PCA(n_components=40)

dataModel = []
filepath = '/tmp/data/'
'''
To be called once into a global variable, dataModel.
'''
def data_populater(result, pca):
    data = np.genfromtxt(filepath+'data.csv', delimiter=',')
    print data.shape
    print "This is important"
    feat = []
    if result=="true" or result=="false":
        data_tx = pca.transform(data[:,0:-1])
        for x in range(0, data_tx.shape[0]):
            feat.append([(data_tx[x,:]), (data[x,-1],)])
    else:
        data_tx = pca.transform(data)
        for x in range(0, data.shape[0]):
            feat.append(list(data_tx[x,:]))
        if data_tx.shape[0]==1:
            feat.append(list(data_tx))
    print data_tx.shape
    return feat
# New function
def NN_train_master():
    data = np.genfromtxt('../data.csv', delimiter = ',')
    print data.shape
    pca = decomposition.PCA(n_components=40)
    pca.fit(data[:,0:-1])
    data_tx = pca.transform(data[:,0:-1])
    print data_tx.shape
    for x in range(0, data_tx.shape[0]):
        dataModel.append([(data_tx[x,:]), (data[x,-1],)])
    training_set = SupervisedDataSet(len(dataModel[0][0]), 1)
    print training_set
    i = 1
    print dataModel
    count = 0
    for i, e in dataModel: 
        print "count is ", count
        if(count==62):
            break
        count += 1
        training_set.addSample(i, e)
        print training_set
    hidden_nodes_1 = 10 
    hidden_nodes_2 = 10
    
    net = buildNetwork(40, hidden_nodes_1, hidden_nodes_2, 1, bias=True, hiddenclass = TanhLayer)
    print net
    print training_set
    print "Analyse"
    trainer = BackpropTrainer(net, training_set, learningrate = 0.001, momentum = 0.99)
    error_class = trainer.trainUntilConvergence(verbose=True, validationProportion=0.15, continueEpochs=5, maxEpochs=200)
    error = trainer.train()
    f = open(filepath+'net.dmp', 'w')
    print "Dumping Neural Net"
    print net
    pickle.dump(net, f)
    return pca
    '''
    Any output can be predicted by: net.activate(test_feat)
    '''
    '''
    Not yet complete, just a basic guideline.
    '''

def NN_train(feat):
    print "Loading neural net for training"
    net2 = pickle.load(open(filepath+'net.dmp', 'r'))
    net2.sorted = False
    net2.sortModules()
    training_set = SupervisedDataSet(len(feat[0][0]), 1)
    for i,e in feat:
       training_set.addSample(i, e) 
    trainer = BackpropTrainer(net2, training_set, learningrate = 0.001, momentum = 0.99)
    error = trainer.train()
    print "Training Done"
    print "Dumping Neural Net"
    pickle.dump(net2, open(filepath+'net.dmp', 'w'))
    print net2
    return 50


def NN_test(feat):
    print "Loading neural net for testing"
    net2 = pickle.load(open(filepath+'net.dmp', 'r')) 
    net2.sorted = False
    net2.sortModules()
    print net2
    pred_list = []
    print feat
    print "This was feat"
    for i in feat:
        print net2.activate(i)
        pred_list.append(np.round(abs(net2.activate(i))))
    if sum(pred_list)>len(pred_list)*0.5:
        print "Infected"
        return 1
    else:
        print "Clear"
        return 0

def master_update():
    df1 = DataFrame.from_csv('../data/data.csv', sep=',')
    df2 = DataFrame.from_csv('/tmp/data/data.csv', sep=',')
    frames = [df1, df2]
    df2 = pandas.concat(frames)
    DataFrame.to_csv(df2, '../data/data.csv', sep=',')

'''
To be called once for every .wav file overall
'''
def main(result):
    pca = NN_train_master()
    feat = data_populater(result, pca)    
    if result=="true" or result=="false":
        returnvalue = NN_train(feat)
    if result=="test":
        returnvalue = NN_test(feat)
    master_update()
    os.remove('/tmp/data/data.csv')
    return returnvalue
