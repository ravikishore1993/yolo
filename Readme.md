#What?

A set of Python files to act as a server and run NNs on the server for classification.

#Build Instructions

- To test a file or to supply a train case to a file, 
`cd server` and, 
run `python server.py 0.0.0.0 8001` or `python server.py 0.0.0.0 8000`
Keep uploading files in the GUI. 

- In order to re-design the neural network, make the changes accordingly in server/brain.py and
`cd server` and,
run `python
import brain
brain.NN_train_master()`
to seal the changes in a neural net dump file.

#Packages to Install

Install pip and download all the packages mentioned in the .py file headers.
