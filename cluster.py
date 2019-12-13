import util, algos
import tests
import argparse
import pandas as pd
import sys
from tests import compareCollections

def getEvents(input,loadFromh5=False):
    evs, jets = pd.DataFrame(),pd.DataFrame()
    if loadFromh5:
        print("Loading jets and pf candidates from h5")
        assert input.endswith('.h5'), "Wrong file type, need .h5!"
        evs  = pd.read_hdf(input, 'events')
        jets = pd.read_hdf(input, 'jets')
    else:
        print("Loading jets and pf candidates from CMSSW EDM file")
        assert input.endswith('.root'), "Wrong file type, need .root!"
        evs,jets = util.loadFromFile(input,writeToh5=True)   
     
    return evs,jets
        

if __name__ == "__main__":
    
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', dest='input', type=str, default="debugPF.root")
  parser.add_argument('--fromh5', action='store_true')
  args = parser.parse_args()
  
  events, ak4jets = getEvents(args.input,args.fromh5)
  jets = algos.seedConeJetsAllEvents(events,jet_threshold=5.)
  histos = compareCollections(ak4jets,jets)
  
  
