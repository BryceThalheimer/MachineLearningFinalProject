#Logistic Regression Model. 10-fold Cross Validation

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt

import numpy as np
import utils
from ReadData import read_data2

def logistic_regression_train(dataset, dataset_type):
	X_train, X_dev, _, y_train, y_dev, _ = dataset

	num_folds = KFold(n_splits=10, shuffle=True)
	lr_model = LogisticRegression(penalty='l2')
	cval_score = cross_val_score(lr_model, X_train, y_train, cv=num_folds).mean()
	lr_model.fit(X_train, y_train)

	y_pred_probs = lr_model.predict_proba(X_dev)
	roc_auc_score = utils.plot_roc(y_pred_probs[:, 1], y_dev, 'Logistic Regression Train', dataset_type, './graphs/lr_roc_train')
	# print(roc_auc_score)

	y_pred = np.argmax(y_pred_probs, axis=1)
	accuracy, specificity, sensitivity = utils.acc_spec_sens(y_pred, y_dev)
	# print(accuracy, specificity, sensitivity)

	return lr_model

def logistic_regression_test(dataset, dataset_type, lr_model):
	_, _, X_test, _, _, y_test = dataset
	y_pred_probs = lr_model.predict_proba(X_test)
	roc_auc_score = utils.plot_roc(y_pred_probs[:, 1], y_test, 'Logistic Regression Test', dataset_type, './graphs/lr_roc_test')
	# print(roc_auc_score)

	y_pred = np.argmax(y_pred_probs, axis=1)
	test_accuracy, _, _ = utils.acc_spec_sens(y_pred, y_test)
	# print(accuracy, specificity, sensitivity)

if __name__ == "__main__":
	demographic_biomarker_data, biomarker_data, replicated_biomarker_data, colorectum_data = read_data2()
	biomarker_model = logistic_regression_train(biomarker_data, 'Biomarker')
	replicated_model = logistic_regression_train(replicated_biomarker_data, 'Replicated')
	demographic_biomarker_model = logistic_regression_train(demographic_biomarker_data, 'Demographic Biomarker')
	colorectum_model = logistic_regression_train(colorectum_data, 'Colorectum')
	plt.figure()
	biomarker_score_test = logistic_regression_test(biomarker_data, 'Biomarker', biomarker_model)
	replicated_score = logistic_regression_test(replicated_biomarker_data, 'Replicated', replicated_model)
	demographic_biomarker_data_score = logistic_regression_test(demographic_biomarker_data, 'Demographic Biomarker', demographic_biomarker_model)
	colorectum_data_score = logistic_regression_test(colorectum_data, 'Colorectum', colorectum_model)

	# print(biomarker_score)
	# print(replicated_score)
	# print(demographic_biomarker_data_score)
