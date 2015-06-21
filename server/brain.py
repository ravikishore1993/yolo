from pybrain.datasets            import SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
import numpy as np
import pickle
from pybrain.structure           import TanhLayer
# TODO: Remove the hardcoded part once synced up

dataModel = []
filepath = '/tmp/data/'
'''
To be called once into a global variable, dataModel.
'''
def data_populater():
    data = np.genfromtxt(filepath+'data.csv', delimiter=',')
    for x in range(0, data.shape[0]):
        dataModel.append([(data[x,0:-1]), (data[x,-1],)])
    return dataModel    

# New function
def NN_train():
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
    trainer = BackpropTrainer(net, training_set, learningrate = 0.001)#, momentum = 0.99)
    error_class = trainer.trainUntilConvergence()
    error = trainer.train()
    f = open(filepath+'net.dmp', 'w')
    print "Dumping Neural Net"
    pickle.dump(net, f)
    '''
    Any output can be predicted by: net.activate(test_feat)
    '''
    '''
    Not yet complete, just a basic guideline.
    '''
def NN_test():
    print "Loading neural net"
    net = pickle.load(filepath+'net.dmp', 'r') 
    

def main():
    a = data_populater()
    NN_train()
