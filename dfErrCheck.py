import uproot4 as up4
import uproot as up3
import pandas as pd
import numpy as np
import glob
from histbook import *

if __name__=='__main__':
    inputfiles = glob.glob('samp*.root')
    
    branches = [b'ZCandidate_*',
                b'event_weight',
    ]

    #outFile  = up3.recreate('test_holder.root',compression = None)
    events = up3.pandas.iterate(inputfiles[:1],'PreSelection;1',branches=branches)
    
    for b in events:
        zptdf  = b[b['ZCandidate_pt'] > 250.0]
        fdf = zptdf
        print("number of passing events ",len(fdf))

    #lets make some histograms.
    hbooktest = Hist(bin("zptest",55,250,800),weight="w")
    hbooktest.fill(zptest=fdf['ZCandidate_pt'],w=fdf['event_weight'])
    print(hbooktest.pandas())

    #Saving histbook hists to root files does not work.
    

