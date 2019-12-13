import util, algos
from tests import compareCollections
import argparse
import pandas as pd
import sys


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
  residual_Nreconstructed = compareCollections(ak4jets,jets)
  print("On average, number of reconstructed jets 1 - N_new/N_ref = %f" %residual_Nreconstructed)
  if residual_Nreconstructed<0.:
      print("Reconstruct too many jets with new algorithm! Please find out why.")
  elif residual_Nreconstructed>0:
      print("Reconstruct too few jets with new algorithm! Please find out why.")
  else:
      print("You're cheating! Nothing is this good. Go back.")
  
  
