
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
from sklearn import cross_validation, metrics
from sklearn.neighbors import KNeighborsClassifier


# # label

# In[2]:

labels = {
    '0':'file', '1':'network', '2':'service', '3':'database', '4':'communication', '5':'memory', '6':'driver', 
    '7':'system', '8':'application', '9':'io', '10':'others', '11':'security', '12':'disk', '13':'processor'}

fault_label = {
    '0':'file', '1':'network', '2':'service', '3':'database', '5':'memory', 
    '10':'others', '11':'security', '12':'disk', '13':'processor'}


# # load dataset

# In[3]:

X = []
y = []

print("loading data...")
try:
    with open("data_msg_type/x.txt", 'rU') as f:
        res = list(f)
        for line in res:
            line.strip("\n")
            features = line.split("\t")
            while features.__contains__(""):
                features.remove("")
            for i in range(len(features)):
                features[i] = float(features[i])
            X.append(features)
         
    #read the classes from file and put them in list.      
    with open("data_msg_type/y.txt", 'rU') as f:
        res = list(f)
        for line in res:
            y.append(int(line.strip("\n")[0]))
            
except:
    print("Error in reading the train set file.")
    exit()

print("Dataset loaded.")


# # split dataset

# In[4]:

X = np.array(X) #change to matrix
y = np.array(y) #change to matrix (sklearn models only accept matrices)

print("Separating data into 80% training set & 20% test set...")
X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    X, y, test_size=0.2, random_state=33) # add random state here...
print("Dataset separated.\n")


# # knn train

# In[5]:

print("---------------K Nearest Neighbors----------------")
n_neighbors_list = range(1, 2, 1)
result_n_neighbors = []
max_score_knn = float("-inf")
best_param_knn = None

for n_neighbors in n_neighbors_list:
    print("Testing %d nearest neighbors" % n_neighbors)
    knn_clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    scores = cross_validation.cross_val_score(
             knn_clf, X_train, y_train, scoring="accuracy", cv=9)
    result_n_neighbors.append(scores.mean())
    if scores.mean() > max_score_knn:
        max_score_knn = scores.mean()
        best_param_knn = {"n_neighbors": n_neighbors}


# # test and evaluation

# In[6]:

knn_clf = KNeighborsClassifier(best_param_knn.get("n_neighbors")).fit(X_train, y_train)
knn_clf_test_score = knn_clf.score(X_test, y_test)

count1 = 0
count2 = 0
actualist = []
predlist = []

for i in range(len(X_test)):
    count2 += 1
    classinrow = X_test[i]
    classinrow = np.array(X_test[i]).reshape(1,-1)
    predicted = knn_clf.predict(classinrow)
    actual = y_test[i]
    actualist.append(actual)
    predlist.append(predicted[0])
    if predicted == actual:
        count1 += 1

print("Number of neighbors: ", len(n_neighbors_list))
print("Train Results: ", result_n_neighbors)
print("Best accuracy: ", max_score_knn)
print("Best parameter: ", best_param_knn)
print("Test set accuracy: ", knn_clf_test_score)

print("Total cases: ", count2)
print("Correct Prediction: ", count1)
print("Correct prediction rate: ", float(count1) / count2)


# # plot

# In[7]:

def plot_CM(cm, title="Normalized Confusion Matrix", cmap=plt.cm.Greens):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(fault_label))
    plt.xticks(tick_marks, fault_label.values(), rotation=90)
    plt.yticks(tick_marks, fault_label.values())
    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.show()
    
print(metrics.classification_report(actualist, predlist,
      target_names = list(fault_label.values())))
cm = metrics.confusion_matrix(actualist, predlist)
print(cm)

# visualization
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
plt.figure()
plot_CM(cm_normalized)

