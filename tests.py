import pandas as pd
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
import sys
from scipy.spatial.distance import cdist

def deltaR(a, b):
    return np.sqrt((a['eta'] - b['eta'])**2 + (a['phi'] - b['phi'])**2)
    
outpath = "/eos/home-t/thaarres/www/L1T_phase2_PF_jets/"
    
def getPairs(ref,new):
    appended_data = []
    for ev in range(0,len(ref)):
        ref_ev = ref.get_group(ev)
        new_ev = new.get_group(ev)
        distance_array = cdist(ref_ev.iloc[:,:2], new_ev.iloc[:,:2], metric='minkowski', p=2) #returns pairwise distance matrix ( shape=(ref,new), new <= ref)              
        # np.set_printoptions(suppress=True,precision=3)
        # print distance_array
        minInRows = np.array(np.argmin(distance_array, axis=1)) #Finds minimum distance between reference object and each new object
        selectedJets = new_ev.iloc[minInRows,:]
        frames = [ref_ev,selectedJets]
        result = pd.concat(frames,axis=1,sort=False)
        appended_data.append(result)
    appended_data = pd.concat(appended_data)    
    appended_data.columns = ['ref_eta','ref_phi','ref_pt','new_eta','new_phi','new_pt']
    return appended_data

def getResiduals(ref,new):
    return  (ref - new) / ref
    
def drawDataframe(resultPt,outname,xlabel,ylabel='Number of jets',bins=100,range=(-0.05,0.05)):
    resultPt.plot.hist(bins=bins,range=range,color='black',label='$\sigma$ (mean = %.3f)'%np.mean(resultPt),histtype='step', linewidth=2, facecolor='darkseagreen', hatch='/', edgecolor='k',fill=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='upper right')
    plt.savefig(outpath+outname+".png")
    plt.clf()

def drawMultipleDataFrames(dfs,outname,legs,xlabel,ylabel='Number of jets',bins=100,log=False):
    for i,df in enumerate(dfs):
        if i == 0:
            ax = df.plot.hist(bins=bins,color='darkseagreen',label=legs[i]+' $\sigma$ (mean = %.3f)'%np.mean(df),histtype='step', linewidth=2,fill=False,alpha=0.5)
            
        else:
            df.plot.hist(ax=ax,bins=bins,color='orangered',label=legs[i]+' $\sigma$ (mean = %.3f)'%np.mean(df),histtype='step', linewidth=2,fill=False,alpha=0.5)    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if log:
        plt.yscale('log')
    plt.legend(loc='upper right')
    plt.autoscale()
    plt.savefig(outpath+outname+".png")
    plt.clf()
               
def compareCollections(refCollection,newCollection):
    
    refCollection_event = refCollection.groupby(refCollection.index)
    newCollection_event = newCollection.groupby(newCollection.index)
    
    sigmaN = (refCollection_event.size()- newCollection_event.size())/refCollection_event.size()
    
    drawDataframe(sigmaN,'residuals_Njet','$Njets_{ref}-Njets_{new}/Njets_{ref}$')
    drawMultipleDataFrames ([refCollection_event.size(),newCollection_event.size() ],'Njets',['AK4','Seed'],'$N_{jets}$')
    matchedJetPairs = getPairs(refCollection_event,newCollection_event)
    
    columns = refCollection.columns
    fancynames = ['$\eta$','$\phi','$p_T$']
    for col,name in zip(columns,fancynames):
        log = False
        if col == 'pt':
            log == True
        df = getResiduals(matchedJetPairs['ref_'+col],matchedJetPairs['new_'+col])
        drawDataframe(df,'residuals_'+col,'$%s_{ref}-%s_{new}/%s_{ref}$'%(col,col,col))
        drawMultipleDataFrames ([matchedJetPairs['ref_'+col],matchedJetPairs['new_'+col] ],col,['AK4','Seed'],name,log=log)

    print("Inspect histograms at https://thaarres.web.cern.ch/thaarres/L1T_phase2_PF_jets/")    
     
   