from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from NLPModel import build_model

seed = 1648

Xx, yy, Xt, yt, model_PVDBOW = build_model(seed=seed)

logistic_regression = LogisticRegression(random_state=seed).fit(Xx, yy)
y_pred_lr = logistic_regression.predict(Xt)

svm_model = svm.SVC(kernel='linear', random_state=seed).fit(Xx, yy)
y_pred_svm = svm_model.predict(Xt)

print('logistic regression accuracy = {} | svm accuracy = {}\n'
      'logistic regression f1_score = {} | svm f1_score = {}'
      .format(accuracy_score(yt, y_pred_lr),
              accuracy_score(yt, y_pred_svm),
              f1_score(yt, y_pred_lr, average="macro"),
              f1_score(yt, y_pred_svm, average="macro")))