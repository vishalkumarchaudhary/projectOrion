import sys
import scipy
import numpy
import matplotlib
import pandas
import sklearn
import pandas
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from os import listdir
from os.path import isfile, join
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

def AllModels (file, in_columns, out_columns):		
	data = numpy.genfromtxt(file ,delimiter="," , autostrip = True )
	data = data[2:]
#	numpy.asarray(numpy.random.shuffle(data[:2400]))
	array = data
	X = array[50:-50,in_columns]
#	print X
	X = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0).fit_transform(X)
	Y = array[50:-50,out_columns]
	#print X
	Y = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0).fit_transform(Y)
#	print Y
	
	validation_size = 0.2
	#scoring = 'accuracy'

#	X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state = 0)
	X_train, X_validation, Y_train, Y_validation = X[0:2400], X[2400:], Y[0:2400], Y[2400:]
#	print X_train.pvalues_()
	lr = LogisticRegression()
	lr.fit(X_train, Y_train)
	predictions = lr.predict (X_validation)
	print 'LR : ' + str(accuracy_score(Y_validation, predictions))

	lda = LinearDiscriminantAnalysis()
	lda.fit(X_train, Y_train)
	predictions = lda.predict (X_validation)
	print 'LDA: ' +str(accuracy_score(Y_validation, predictions))

	knn = KNeighborsClassifier()
	knn.fit(X_train, Y_train)
	predictions = knn.predict (X_validation)
	print 'KNN: '+str(accuracy_score(Y_validation, predictions))

	

	rf = DecisionTreeClassifier()
	rf.fit(X_train, Y_train)
	predictions = rf.predict (X_validation)
	print 'DT : ' +str(accuracy_score(Y_validation, predictions))

	nb = GaussianNB()
	nb.fit(X_train, Y_train)
	predictions = nb.predict (X_validation)
	print 'NB : '+str(accuracy_score(Y_validation, predictions))	

	svm = SVC()
	svm.fit(X_train, Y_train)
	predictions = svm.predict (X_validation)
	print 'SVM: '+str(accuracy_score(Y_validation, predictions))	

	print '--------------------'
	rf=RandomForestClassifier(n_estimators=300, criterion='gini', max_depth=None,
		 					min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, 
							 max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, 
		 					min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=1, 
		 					random_state=None, verbose=0, warm_start=False, class_weight=None)
	rf.fit(X_train, Y_train)
	print 'rf: '+str(rf.score(X_validation,Y_validation))
	et=ExtraTreesClassifier(n_estimators=300, criterion='gini', max_depth=None, min_samples_split=2, 
						min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', 
						max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, 
						bootstrap=False, oob_score=False, n_jobs=1, random_state=None, verbose=0, 
						warm_start=False, class_weight=None)
	et.fit(X_train, Y_train)
	print 'et: '+ str(et.score(X_validation,Y_validation))
	#cnf_matrix = confusion_matrix(Y_validation, y_pred)
	#print cnf_matrix


	rf = []

	for i in range(1,5):
		rf.append(ExtraTreesClassifier(n_estimators=300, criterion='gini', max_depth=None,
		 					min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, 
							 max_features=i*6, max_leaf_nodes=None, min_impurity_decrease=0.0, 
		 					min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=1, 
		 					random_state=None, verbose=0, warm_start=False, class_weight=None))
		#cnf_matrix = confusion_matrix(Y_validation, y_pred)
		#print cnf_matrix
	l = []
	for i in range(len(rf)):
		l.append((str(i),rf[i]))
	lda = LinearDiscriminantAnalysis()
#	l.append(('a',lda))
#	l.append(('b',lda))
	l.append(('c',lda))
	l.append(('d',lda))
	ecl = VotingClassifier(estimators = l, voting = 'hard')
#	ecl = AdaBoostClassifier(base_estimator = rf[0])
	ecl.fit(X_train, Y_train)
	y_pred = ecl.predict(X_validation)
	ret = accuracy_score(Y_validation, y_pred)
	print ret
	cnf_matrix = confusion_matrix(Y_validation, y_pred,labels=[-3,-2,-1,0,1,2,3])
	#print cnf_matrix
	s1 = 0.0
	for i in cnf_matrix:
		s1 = s1 + sum(i)
	print '---------------'
	s = 0.0
	for i in cnf_matrix[0:3,0:3]:
		s = s+sum(i)
	for i in cnf_matrix[4:7,4:7]:
		s = s+sum(i)
	print s/s1
	return ret
	


in_columns  = range(8,27)+range(31,44)+range(44,60)+range(114,120)
out_columns = [121]
filename = 'ICICIBANK'
x_address = filename+'_ycc.csv'
s = 0.0
lam = 1
for i in range(lam):
	s = s + AllModels(x_address, in_columns, out_columns)
print 'avg: '+str(s/lam)





