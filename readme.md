Prerequisites: uproot, pandas, pytables, scipy, matplotlib, numpy


Import the PF candidates and AK4 jets, and run the simple 'seeded cone' reconstruction.
```
import util, algos
events, ak4jets = util.loadFromFile('debugPF.root')
jets = algos.seedConeJetsAllEvents(events)
```

Compare kinematic quantities of the newly created jet collection and the base AK4 jets:
```
import tests
compareCollections(ak4jets,jets)
```

The script *cluster.py* contains an example of loading from file, clustering a new jet collectinon and testing its performance.


Coming soon: more algos, performance analysis utilities...
