# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


data_path = "data/"

input_files=[ "train.csv", "test.csv" ] # 13765202 lines

for input_file in input_files:
    print "Reading %s" % input_file
    time0 = dt.datetime.now()
    df = pd.read_csv(data_path+input_files)
    time1 = dt.datetime.now()
    print('Read in %i sec' % (time1-time0).seconds)

    print """Drop minutes_past columns"""
    df = df.drop('minutes_past', axis=1)

    print """Create sample_weights feature"""
    max_km = df["radardist_km"].max()
    df['sample_weights'] = df['radardist_km'].apply( lambda x:1-x/max_km )

    print """Drop radardist_km columns"""
    df = df.drop('radardist_km', axis=1)

    print """Create missing_values feature"""
    nb_extra_cols = 1
    if ( input_file == "train.csv"):
        nb_extra_cols = 2
    nb_columns = len(df.columns) - nb_extra_cols # without Expected and Id
    df['missing_values'] = df.isnull().sum(axis=1) / nb_columns

    grouped = df.groupby('Id')

    value_cols = [ 'Ref','Ref_5x5_10th','Ref_5x5_50th','Ref_5x5_90th',
    'RefComposite','RefComposite_5x5_10th','RefComposite_5x5_50th','RefComposite_5x5_90th',
    'RhoHV','RhoHV_5x5_10th','RhoHV_5x5_50th','RhoHV_5x5_90th',
    'Zdr','Zdr_5x5_10th','Zdr_5x5_50th','Zdr_5x5_90th',
    'Kdp','Kdp_5x5_10th','Kdp_5x5_50th','Kdp_5x5_90th' ]

    agg_cols = lambda col: {col+'_max' : np.max, col+'_median' : np.median}

    print """Agg by mean"""
    agg_df = grouped.agg(np.mean) 

    print """Create median, max aggregations""" 
    for col in value_cols:
        agg_df = pd.concat( [agg_df, grouped[col].agg(agg_cols(col))], axis=1 )


    print """Fill left NaN with median"""
    agg_df = agg_df.fillna(agg_df.median())


    if ( input_file == "train.csv"):
        print """Clean Expected column"""
        agg_df = agg_df[agg_df['Expected'] <= 100]


    clean_name = "clean_"+input_file
    print """Saving %s\n\n""" % clean_name
    agg_df.to_csv(data_path+clean_name)
