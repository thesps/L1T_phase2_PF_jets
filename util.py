import pandas as pd
import uproot
import numpy as np

def loadFromFile(filename):
    f = uproot.open(filename)
    puppi_tree = 'Events/l1tPFCandidates_l1pfCandidates_Puppi_RESP./l1tPFCandidates_l1pfCandidates_Puppi_RESP.obj/'
    p4_tree = puppi_tree + 'l1tPFCandidates_l1pfCandidates_Puppi_RESP.obj.m_state.p4Polar_.fCoordinates'
    pt = f[p4_tree + '.fPt'].array()
    eta = f[p4_tree + '.fEta'].array()
    phi = f[p4_tree + '.fPhi'].array()

    index = np.array([i for i, ev in enumerate(pt) for j in range(len(ev))]).flatten()
    events = pd.DataFrame({'i' : index, 'pt' : pt.flatten(), 'eta' : eta.flatten(), 'phi' : phi.flatten()})
    events.set_index('i', inplace=True, drop=True)

    ak4_tree = 'Events/recoPFJets_ak4PFL1Puppi__RESP./recoPFJets_ak4PFL1Puppi__RESP.obj'
    p4_tree = ak4_tree + '/recoPFJets_ak4PFL1Puppi__RESP.obj.m_state.p4Polar_.fCoordinates'
    pt = f[p4_tree + '.fPt'].array()
    eta = f[p4_tree + '.fEta'].array()
    phi = f[p4_tree + '.fPhi'].array()
    index = np.array([i for i, ev in enumerate(pt) for j in range(len(ev))]).flatten()
    jets = pd.DataFrame({'i' : index, 'pt' : pt.flatten(), 'eta' : eta.flatten(),      'phi' : phi.flatten()})
    jets.set_index('i', inplace=True, drop=True)
    return events, jets
