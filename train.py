# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import cPickle as cpk

import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn import cross_validation
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

cleantrain_file="data/clean_train.csv" # 12786237 lines

print "Lecture clean csv..."
time0 = dt.datetime.now()

cols = [ 'Id', 'Expected', 'missing_values',
'Ref_5x5_10th_max','Ref_5x5_50th_max','sample_weights',
'Ref_5x5_90th','RefComposite_5x5_90th','Ref_5x5_90th_max',
'RefComposite_5x5_90th_median','RefComposite_5x5_90th_max',
'Zdr_5x5_90th','Zdr_5x5_90th_max','Ref_5x5_90th_median','Zdr_5x5_90th_median']

df = pd.read_csv(cleantrain_file, usecols=cols, nrows=100000)

time1 = dt.datetime.now()
print('lecture en: %i sec' % (time1-time0).seconds)
print "Nb lignes: %d ",  df.shape[0]

print "Prepare data, labels"
data = df.as_matrix()
label = df[['Expected']].as_matrix().ravel()
df = df.drop(['Expected', 'Id'], axis=1)

# print "Prepare folds for cross validation"
x_train, x_test, y_train, y_test = cross_validation.train_test_split(data, label, test_size=0.8, random_state=23435)


# conf = sklearn.metrics.confusion_matrix(df['missing_values'], df['sample_weights'])
# plt.imshow(conf, cmap='binary', interploation='None')

print "RandomForestRegressor..."
clf = sklearn.ensemble.RandomForestRegressor(verbose=2, n_jobs=2)
clf.fit(x_train, y_train)
print mean_squared_error( clf.predict(x_test), y_test )
# with open('models/RandomForestRegressor.pkl', 'wb') as fid:
#     cpk.dump(clf, fid)

print "GradientBoostingRegressor..."
clf = sklearn.ensemble.GradientBoostingRegressor(verbose=2)
clf.fit(x_train, y_train)
print mean_squared_error( clf.predict(x_test), y_test )
# with open('models/GradientBoostingRegressor.pkl', 'wb') as fid:
#     cpk.dump(clf, fid)

print "ExtraTreesRegressor..."


clf = ExtraTreesRegressor(n_estimators=20, verbose=2, n_jobs=-1)
clf.fit(x_train, y_train)
print mean_squared_error( clf.predict(x_test), y_test )
# with open('models/ExtraTreesRegressor.pkl', 'wb') as fid:
#     cpk.dump(clf, fid)


