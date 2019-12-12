Import the PF candidates and AK4 jets, and run the simple 'seeded cone' reconstruction.
```
import util, algos
events, ak4jets = util.loadFromFile('debugPF.root')
jets = algos.seedConeJetsAllEvents(events)
```

Coming soon: more algos, performance analysis utilities...
