# Copyright 2020, General Electric Company. All rights reserved. See https://github.com/xcist/code/blob/master/LICENSE

import numpy as np

def Detection_DAS(viewIn, cfg):
    viewOut = viewIn * (1.6*1e-7/cfg.scanner.capacitor
        /cfg.scanner.readoutVolt*cfg.scanner.maxReadout)
    viewOut = viewOut*cfg.scanner.detectionGain
    
    eNoise = np.float32(np.random.randn(viewIn.size)*cfg.sim.eNoise)
    viewOut += eNoise.reshape(viewIn.shape)
    viewOut[viewOut>cfg.scanner.maxReadout] = cfg.scanner.maxReadout
    
    return viewOut
