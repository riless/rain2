import cPickle as cpk
import pandas as pd
import datetime as dt
import numpy as np

model_path = "models/"
data_path = "data/"
cleantest_file="clean_test.csv"
models_files = ['GradientBoostingRegressor.pkl', 'RandomForestRegressor.pkl', 'ExtraTreesRegressor.pkl']


cols = [ 'Id', 'missing_values',
'Ref_5x5_10th_max','Ref_5x5_50th_max','sample_weights',
'Ref_5x5_90th','RefComposite_5x5_90th','Ref_5x5_90th_max',
'RefComposite_5x5_90th_median','RefComposite_5x5_90th_max',
'Zdr_5x5_90th','Zdr_5x5_90th_max','Ref_5x5_90th_median','Zdr_5x5_90th_median']

time0 = dt.datetime.now()
df = pd.read_csv(data_path+cleantest_file, usecols=cols)
time1 = dt.datetime.now()
print('lecture en: %i sec' % (time1-time0).seconds)
print "Nb lignes: %d ",  df.shape[0]

print "preparing data"
ids = df['Id']
df = df.drop(['Id'], axis=1)
data = df.as_matrix()


pred_exp = [pd.read_csv("data/marshall-palmer.csv")]

for model_file in models_files:
    with open(model_path+model_file, 'rb') as fid:
        print "Load classifier %s" % model_file
        clf = cpk.load(fid)

        print "Prediction..."
        pred = clf.predict(data)

        print "Saving csv..."
        df_pred = pd.DataFrame({'Expected': pred, 'Id': ids})
        pred_exp.append( pred )

        df_pred.to_csv(data_path+model_file+'_sol.csv', index=False)

sol = pd.DataFrame({'Id': ids, 'Expected': np.mean( pred_exp, axis=0) }) 
solution_file="solution.csv"
sol.to_csv(data_path+solution_file, header=True, cols=["Id","Expected"], index=False)
