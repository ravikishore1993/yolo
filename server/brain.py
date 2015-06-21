from pybrain.datasets            import SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
import numpy as np
import pickle
from pybrain.structure           import TanhLayer
import os
# TODO: Remove the hardcoded part once synced up

dataModel = []
filepath = '/tmp/data/'
'''
To be called once into a global variable, dataModel.
'''
def data_populater(result):
    data = np.genfromtxt(filepath+'data.csv', delimiter=',')
    feat = []
    if result=="true" or result=="false":
        for x in range(0, data.shape[0]):
            feat.append([(data[x,0:-1]), (data[x,-1],)])
    else:
        for x in range(0, data.shape[0]):
            feat.append(list(data[x,:]))
        if data.shape[0]==1:
            feat.append(list(data))
    return feat
# New function
def NN_train_master():
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
    hidden_layers = 10
    
    net = buildNetwork(len(dataModel[0][0]),hidden_layers, 1, bias=True, hiddenclass = TanhLayer)
    print net
    print training_set
    print "Analyse"
    trainer = BackpropTrainer(net, training_set, learningrate = 0.001, momentum = 0.99)
    error_class = trainer.trainUntilConvergence()
    error = trainer.train()
    f = open(filepath+'net.dmp', 'w')
    print "Dumping Neural Net"
    print net
    pickle.dump(net, f)
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
    os.remove('/tmp/data/data.csv')


def NN_test(feat):
    print "Loading neural net for testing"
    net2 = pickle.load(open(filepath+'net.dmp', 'r')) 
    net2.sorted = False
    net2.sortModules()
    print net2
    pred_list = []
    for i in feat:
        print net2.activate(i)
        pred_list.append(np.round(net2.activate(i)))
    os.remove('/tmp/data/data.csv')
    if sum(pred_list)>len(pred_list)*0.5:
        print "Infected"
        return 1
    else:
        print "Clear"
        return 0

'''
To be called once for every .wav file overall
'''
def main(result):
    feat = data_populater(result)    
    if result=="true" or result=="false":
        NN_train(feat)
    if result=="test":
        NN_test(feat)
