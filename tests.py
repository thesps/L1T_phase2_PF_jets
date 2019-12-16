import pandas as pd
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

def compareCollections(refCollection,newCollection):
    
    arrays = []
    sigmaN = []
    sigmaEta, sigmaPhi, sigmaPt = ([] for i in range(3))
    arrays.append(sigmaEta)
    arrays.append(sigmaPhi)
    arrays.append(sigmaPt)
    
    columns = refCollection.columns
    
    refCollection_event = refCollection.groupby(refCollection.index)
    newCollection_event = newCollection.groupby(newCollection.index)
    nevents = len(refCollection_event)
    
    print "For a total of %i events: "%nevents
    for ev in range(0,nevents):
        ref = refCollection_event.get_group(ev)
        new = newCollection_event.get_group(ev)
        sigmaN.append(float((len(ref)-len(new))/len(ref)))
        if (ev % 20==0):
            print("For event %i: Number of reconstructed jets: ref = %i   new = %i"%(ev,len(ref),len(new)))
            print("              Leading jet from ref collection: pT = %f"         %(ref['pt'].iloc[[0]]))
            print("              Leading jet from new collection: pT = %f \n \n"   %(new['pt'].iloc[[0]]))
        for array,col in zip(arrays,columns):
            array.append(  (ref[col].head() - new[col].head()) / ref[col].head())
       
    for array,col in zip(arrays,columns):
        resultPt = pd.concat(array)
        resultPt.plot.hist(title=col,bins=400,range=(-1.,1.))
        plt.xlabel('%s_ref-%s_new/ %s_ref'%(col,col,col))
        plt.ylabel('Number of jets')
        plt.savefig(col+".png")
        plt.clf()
    plt.plot(sigmaN)
    plt.xlabel('N_ref-N_new/N_ref')
    plt.ylabel('Number of jets')
    plt.savefig("nJets.png")
    return np.mean(sigmaN)
     
   