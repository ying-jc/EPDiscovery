#!/usr/bin/env python

import os
from multiprocessing import Pool
import datetime
import random
import pandas as pd
import shutil
from joblib import load
import warnings
warnings.filterwarnings("ignore")

def mod_predict(n_proc,seq,conf,cutoff,terminal,out):
    if_p, mod_p = ex_config(conf) 
    mypath = os.getcwd()
    os.chdir(mypath)
    nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rr = random.randint(100000,999999)
    foldern = 'tmp_'+nowtime+'_'+str(rr)
    os.mkdir(foldern)
    os.chdir(foldern)    
    multi_run_iFeature(n_proc,mypath+'/'+seq,if_p)
    ex_features(mod_p)
    fns = ex_filename(mypath+'/'+seq)    
    print('\nPerforming classifier prediction ......')    
    bl_mod_pred(mod_p)    
    comb_prob = pd.read_table('.tmp2',sep='\t',index_col=0)
    clf = load(mod_p+'/'+'MLP_be.joblib')
    probs = clf.predict_proba(comb_prob)
    prob = [g[1] for g in probs]
    pred = [0 if h < cutoff else 1 for h in prob]
    df_prob = pd.DataFrame(prob,columns=['Probability of EP'],index=fns)
    df_prob['Prediction of EP'] = pred    
    if terminal == 'True':
        print('\n'.join(['','Result of prediction:']))
        print(df_prob)    
    if out != None:
        df_prob.to_csv(mypath+'/'+out)
        print('\nThe result of prediction has been saved to '+out+'!')        
    os.chdir(mypath)    
    shutil.rmtree(foldern, ignore_errors=True)
    
def ex_config(cf):
    cfs = open(cf).read().strip().split('\n')
    cfs = [z for z in cfs if not z.startswith('#')]
    if_path = cfs[0].split('=')[-1].strip()
    mod_path = cfs[1].split('=')[-1].strip()
    return if_path, mod_path

def ex_filename(fa):
    fs = open(fa).read().strip().split('\n')
    xs = [x.strip()[1:] for x in fs if x.startswith('>')]
    return xs

def ex_features(mod_p):    
    seq_features = ['AAC','APAAC','CKSAAGP','CTDC','CTDD','CTDT','CTriad','DDE','DPC','GAAC','Geary','GTPC','Moran','NMBroto','PAAC','QSOrder','SOCNumber']    
    t = []
    for fn in seq_features:
        dat = pd.read_table('.'+fn,sep='\t',index_col=0)
        dat.columns = fn+'_'+dat.columns
        t.append(dat)        
    c_dat = pd.concat(t,axis=1)
    c_dat.to_csv('.tmp',sep='\t',index=True)

def run_iFeature(fa, if_p,f_type):
    os.system('python %s --file %s --type %s --out %s'%(if_p+'/iFeature.py',fa,f_type,'.'+f_type))

def multi_run_iFeature(np, fa, if_p):    
    print('\nPerforming feature extraction ......')
    f_types = ['AAC','APAAC','CKSAAGP','CTDC','CTDD','CTDT','CTriad','DDE','DPC','GAAC','Geary','GTPC','Moran','NMBroto','PAAC','QSOrder','SOCNumber']
    p = Pool(np)
    for b in f_types:
        p.apply_async(run_iFeature,args=(fa,if_p,b))
    p.close()
    p.join()

def bl_mod_pred(mod_path):
    clfs = ["D2_RFERF_AB","D2_SFMRF_MLP","D2_SFMXGB_MLP","D3_LASSO_GB","D3_RFERF_LGB","D3_SFMXGB_MLP","D4_RFEET_AB","D4_SFMET_GB","D4_SFMXGB_LGB","D5_RFELR_MLP","D5_SFMXGB_GB","D6_RFEET_MLP","D7_RFERF_SVM","D7_SFMET_MLP","D7_SFMRF_GB"]
    c_prob_coln = ['n'+d[1:] for d in clfs]
    comb_feats = pd.read_table('.tmp',sep='\t',index_col=0)
    t = []
    for clf_n in clfs:
        clf = load(mod_path+'/'+clf_n+'.joblib')        
        probs = clf.predict_proba(comb_feats)
        prob = [e[1] for e in probs]
        t.append(prob)
    
    c_prob = pd.DataFrame(t).T
    c_prob.columns = c_prob_coln
    c_prob.to_csv('.tmp2',sep='\t',index=True)   
    