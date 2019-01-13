from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from NLPModel import build_model
from NLPModel import read_and_preprocess

Xx, yy, Xt, yt, model_PVDBOW = build_model(additional_stop_words={'sbquo', 'www', 'http', 'com'}, vector_size=300,
                                           window=10, min_count=2, epochs=100, alpha=0.025, min_alpha=0.01)

logistic_regression = LogisticRegression().fit(Xx, yy)
y_pred_lr = logistic_regression.predict(Xt)

svm_model = svm.SVC(kernel='linear').fit(Xx, yy)
y_pred_svm = svm_model.predict(Xt)

print('logistic regression accuracy = {} | svm accuracy = {}\n'
      'logistic regression f1_score = {} | svm f1_score = {}'
      .format(accuracy_score(yt, y_pred_lr),
              accuracy_score(yt, y_pred_svm),
              f1_score(yt, y_pred_lr, average="macro"),
              f1_score(yt, y_pred_svm, average="macro")))

# print(read_and_preprocess(is_training=False, additional_stop_words={'sbquo', 'www', 'http', 'com'}))