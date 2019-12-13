import pandas as pd
import numpy as np

def compareCollections(refCollection,newCollection):
    hists = []
    refCollection_event = refCollection.groupby(refCollection.index)
    newCollection_event = newCollection.groupby(newCollection.index)
    nevents = len(refCollection_event)
    print "For a total of %i events: "%nevents
    for ev in range(0,nevents):
        ref = refCollection_event.get_group(ev)
        new = newCollection_event.get_group(ev)
        sigmaN   = float((len(ref)-len(new))/len(ref))
        sigmaPt   = (ref['pt'].head() -new['pt'].head()) /ref['pt'].head()
        sigmaEta  = (ref['eta'].head()-new['eta'].head())/ref['eta'].head()
        sigmaPhi  = (ref['phi'].head()-new['phi'].head())/ref['phi'].head()
        hist = sigmaPt.hist(bins=10)
        #sigmaEta = 
        #sigmaPhi = 

  
   