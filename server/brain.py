from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
import numpy as np
import pickle
# TODO: Remove the hardcoded part once synced up

dataModel = []
filepath = '/tmp/data/'

'''
To be called once into a global variable, dataModel.
'''
def data_populater():
    data = np.genfromtxt(filepath+'data.csv', delimiter=',')
    for x in range(0, data.shape(0)):
        dataModel.append([tuple(data[x,0:-2]), tuple(data[x,-1],)])

# New function
def NN():
    train_len = len(dataModel)
    training_set = ClassificationDataSet(train_len, 1 , nb_classes=2)
    
    for input, target in dataModel: 
        training_set.addSample(input, target)
    hidden_layers = 10
    net = buildNetwork(len(Data[0][0]),hidden_layers, 1, bias=True, hiddenclass = TanhLayer)
    trainer = BackpropTrainer(net, training_set, learningrate = 0.001, momentum = 0.99)
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
