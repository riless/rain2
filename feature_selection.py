# -*- coding: utf-8 -*-
import cPickle as cpk
import pandas as pd

model_path = "models/"
model_file = "RandomForestRegressor.pkl"

cleantrain_file="data/clean_train.csv" # 12786237 lines
df = pd.read_csv(cleantrain_file, nrows=1)
df = df.drop(['Expected', 'Id'], axis=1)
columns = df.columns

with open(model_path+model_file, 'rb') as fid:
	print "Load classifier"
	clf = cpk.load(fid)

	for t in sorted(zip(map(lambda x: round(x, 4), clf.feature_importances_), columns), reverse=True):
		print t