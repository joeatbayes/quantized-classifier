from __future__ import print_function

import numpy as np
import tflearn



# Load CSV file, indicate that the first column represents labels
from tflearn.data_utils import load_csv
data, labels = load_csv('../data/train/gest_train_ratio2.csv', target_column=0,
                        categorical_labels=True, n_classes=7)

print("data=", data)

print ("labels=", labels)

data = np.array(data, dtype=np.float32)

print("data as float array=", data)
print("labels=", labels)
numCol = len(data[0])
numRow = len(data)
numClass = 7

print("numCol=",numCol, "numRow=", numRow, " numClass=", numClass)

# Build neural network
net = tflearn.input_data(shape=[None, numCol])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, numClass, activation='softmax')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=10, batch_size=4, show_metric=True)

# Let's create some data for DiCaprio and Winslet

3,

hSamp = [0.080,0.000,0.964,1.000,0.632,0.825]
yesSamp = [0.040,0.000,0.144,0.205,0.750,0.725]

# Convert our sample data we are trying to classify
# into a the Numeric array format required by tensorFlow
hDta = np.array(hSamp, dtype=np.float32)
yesDta = np.array(yesSamp, dtype=np.float32)


# Predict surviving chances (class 1 results)
pred = model.predict([hDta, yesDta])
print("Prob of H by class:", pred[0])
print("Prob of Yes: by class:", pred[1])