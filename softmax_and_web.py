from sklearn import linear_model
import pickle
import web

logistic = linear_model.LogisticRegression()

# the times of training, notice to change
numbers = 1

dir_all = "/home/DL/LP/LAST_result"
f1 = open(dir_all + "/all_labels_predictions1.plk", 'rb')
predictions = pickle.load(f1)
labels = pickle.load(f1)
f1.close()

f2 = open(dir_all + "/all_img_dir1.plk", 'rb')
img_path = pickle.load(f2)
f2.close()

length = len(labels)
steps = length/5
# for ii in range(0, len(labels), len(labels)/5):
predictions_test = predictions[(numbers-1)*steps:numbers*steps]
labels1_test = labels[(numbers-1)*steps:numbers*steps]
predictions_train = []
labels1_train = []
if numbers == 1:
    predictions_train = predictions[numbers*steps:]
    labels1_train = labels[numbers*steps:]
elif numbers > 1 & numbers < 5:
    predictions_train1 = predictions[0:(numbers-1)*steps]
    labels1_train1 = labels[0:(numbers-1)*steps]
    predictions_train2 = predictions[numbers * steps:]
    labels1_train2 = labels[0:numbers * steps]
    predictions_train.append(predictions_train1)
    predictions_train.append(predictions_train2)
else:
    predictions_train = predictions[0:(numbers-1)*steps]
    labels1_train = labels[0:(numbers-1)*steps]

#fit
a = logistic.fit(predictions_train, labels1_train)
