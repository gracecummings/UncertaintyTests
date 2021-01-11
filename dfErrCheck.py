import uproot4 as up4
import uproot as up3
import pandas as pd
import numpy as np
import boost_histogram as bh
import histbook as hb
#import pickle
import glob
#from histbook import *

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
    nphtest = np.histogram(fdf['ZCandidate_pt'],bins=55,range=(250,800),weights=fdf['event_weight'])
    print("This is the numpy histogram")
    print(nphtest)
    
    hbooktest = hb.Hist(hb.bin("zptest",55,250,800),weight="w")
    hbooktest.fill(zptest=fdf['ZCandidate_pt'],w=fdf['event_weight'])
    print("This is the histbook histogram")
    print(hbooktest.pandas())#the errors calculated are sumw2 errors
    #outFile["histbook"] = hbooktest#Does not write to a root file with uproot
    
    boosthtest = bh.Histogram(bh.axis.Regular(bins=55,start=250,stop=800),storage=bh.storage.Weight())
    boosthtest.fill(fdf['ZCandidate_pt'],weight=fdf['event_weight'])
    npboost = boosthtest.view()
    npboostvar = npboost.variance
    npboosterr = np.sqrt(npboostvar)
    npboostbins,npboostedges = boosthtest.to_numpy()
    print("This is the boost histogram histogram")
    #print(boosthtest)
    print(npboost)
    print(npboosterr)#returns the same errors are histbook
    #outFile["boostdirect"] = boosthtest#Does not write to a root file with uproot
    #outFile["boosttonumpy"] = npboost2#Does not write to a root file with uproot

    #save one array per file
    #f = open('test_arrout.npy','wb')
    #np.save(f,npboosterr)

    #save multiple arrays per file
    f = open('test_arrout.npz','wb')
    np.savez(f,errors=npboosterr,variances=npboostvar)#saves to a zipped numpy files with access as keywords

    #can save the whole histogram as a pickle object if we wanted to

    

