import numpy as np
from scipy import interpolate

def make_source(shape):
    # source: Source_Performix.m in Shared/VCT/focal_spot
    if shape=='performix':
        profile_x = [0.0089117074, 0.0094849812, 0.010956097, 0.010845736, 0.012205287, 0.013411788, 0.013987588, 0.016754877, 0.017287152, 0.018434431, 0.021081094, 0.022178752, 0.023765393, 0.024324181, 0.024199357, 0.026971802, 0.027732590, 0.030677397, 0.033098165, 0.034352586, 0.037708543, 0.040863063, 0.044080034, 0.048601191, 0.057216480, 0.081618488, 0.19156136, 0.50982714, 1.0152169, 1.4892660, 1.7459514, 1.7660810, 1.6156573, 1.4200139, 1.2736123, 1.1803527, 1.124194, 1.0848699, 1.0647312, 1.0552623, 1.0573552, 1.0673612, 1.0904037, 1.1233054, 1.1775253, 1.2699144, 1.4169333, 1.6048678, 1.7323492, 1.6266391, 1.2099488, 0.68120301, 0.31258500, 0.13684797, 0.076048240, 0.054243747, 0.048846766, 0.043879174, 0.039178062, 0.038409978, 0.036757737, 0.035916030, 0.032792993, 0.033051010, 0.032806009, 0.030115416, 0.029396320, 0.028707152, 0.026915371, 0.026284197, 0.025051109, 0.023844510, 0.022237135, 0.020905763, 0.019840322, 0.017934531, 0.016216217, 0.014178540, 0.013444251, 0.012099653, 0.011536123];
        pixsize_x = 0.04;
        #spotsize_x = 0.92; # at 50% max intensity
        
        profile_z = [0.0093995091, 0.0095077194, 0.0089256987, 0.010287303, 0.010336699, 0.010936775, 0.011290736, 0.012208968, 0.013377126, 0.014498876, 0.016150571, 0.017091859, 0.018505901, 0.020504182, 0.021285400, 0.023606740, 0.025583502, 0.026207311, 0.028430954, 0.030482417, 0.031823732, 0.034108926, 0.036122758, 0.039115001, 0.043394867, 0.048032623, 0.059101496, 0.079253219, 0.11440843, 0.18443686, 0.32266757, 0.55782247, 0.86730444, 1.2029779, 1.5474168, 1.8872423, 2.1608834, 2.3139000, 2.3477457, 2.3287232, 2.2959089, 2.2494311, 2.1655865, 2.0284476, 1.8279976, 1.5760206, 1.2920654, 0.99986392, 0.71913159, 0.47511706, 0.29815087, 0.18768285, 0.11574699, 0.073704563, 0.053027507, 0.044716470, 0.041182544, 0.039208446, 0.037241697, 0.036358818, 0.034279484, 0.033669647, 0.031936668, 0.029990802, 0.029815603, 0.028472608, 0.027118715, 0.025909251, 0.024623437, 0.023542469, 0.022042744, 0.021060884, 0.019131450, 0.017695857, 0.016780471, 0.015473038, 0.014326439, 0.013353137, 0.012362288, 0.011399004, 0.010547391];
        pixsize_z = 0.04;
        #spotsize_z = 0.76;
        
    # source: https://github.com/CatSim/Revolution/blob/master/focal_spot/Source_Profiles_PharosSmallFS.m
    elif shape=='pharos_small':
        profile_x = [0.018213105,0.077680773,0.112716701,0.158330545,0.194507941,0.219002249,0.253814441,0.301369037,0.342192697,0.375762733,0.408522729,0.432195733,0.465529641,0.510540237,0.540337517,0.568322021,0.586475025,0.603610869,0.634682997,0.664176801,0.698188981,0.728834009,0.763546713,0.805633937,0.849019937,0.889189273,0.920842721,0.949381685,0.992051685,1.056570041,1.138836985,1.221719089,1.322366849,1.459131797,1.647537613,1.920287717,2.285372501,2.750811369,3.317248489,4.020620905,4.833105161,5.764354449,6.776591257,7.895854661,9.164582229,10.54263776,12.00235644,13.44518945,14.7603935,15.97330507,17.14684381,18.18189302,19.14000922,19.89982195,20.3734481,20.79602857,21.09450263,21.31646279,21.26637627,20.97167882,20.53558326,19.88169605,19.27310652,18.5932863,17.6770856,16.69185232,15.53691507,14.15357138,12.71405236,11.21619598,9.743250253,8.395196813,7.174701349,6.009740165,5.004353377,4.119082045,3.329824849,2.720810889,2.243256377,1.878960921,1.634005157,1.450390041,1.313561437,1.236878341,1.181673201,1.134116457,1.095998161,1.033288877,0.971852785,0.932894169,0.904115657,0.880539033,0.878479665,0.857934689,0.824333353,0.799435485,0.759242293,0.725838085,0.699210213,0.669700521,0.633940381,0.607568241,0.581444021,0.554576169,0.537009893,0.513085821,0.487679249,0.456507025,0.406132025,0.361280333,0.317318037,0.269158609,0.241050585,0.201073609,0.158754709,0.120723765,0.074263497,0.036895573];
        pixsize_x = 0.0305;
    
        profile_z = [0.002293612,0.009484464,0.02877532,0.049683284,0.066281476,0.099947924,0.128342608,0.155852408,0.191461228,0.218877516,0.254395836,0.308018796,0.37688156,0.496676928,0.66115326,0.925396568,1.370593372,2.033234012,2.998588964,4.298378932,5.918377684,7.835203616,9.91305084,11.99063838,14.0066813,15.91959538,17.85381184,19.78221693,21.64656048,23.41935125,24.89570629,26.06524229,26.77541069,27.02498465,27.02735889,26.87521097,26.64539745,26.27007961,25.43444841,24.13504053,22.51336652,20.68710089,18.80572142,16.93127111,15.09398656,13.28654444,11.56703376,9.898375244,8.260504004,6.618920044,5.062736328,3.662534208,2.501281524,1.652269904,1.0874676,0.773992708,0.566628992,0.440153388,0.358468264,0.283490336,0.234956048,0.193413728,0.157754968,0.114557228,0.084592936,0.057213048,0.019930952,0.00186316];
        pixsize_z = 0.0305;
    
    # source: https://github.com/CatSim/Revolution/blob/master/focal_spot/Source_Profiles_PharosLargeFS.m
    elif shape=='pharos_large':
        profile_x = [0.006207304,0.009545114,0.024219586,0.020053882,0.043822482,0.066941496,0.087138371,0.090719468,0.08855892,0.104552953,0.120571183,0.143783414,0.168335778,0.206335036,0.259743325,0.336307149,0.396722101,0.45065909,0.517365673,0.613222075,0.732449356,0.831335361,0.896059616,0.984146534,1.091055761,1.188997977,1.281763195,1.431880621,1.693155242,2.075234002,2.669666244,3.498274312,4.620776804,6.020375193,7.715137116,9.562609229,11.40677779,13.12010824,14.55265668,15.84607638,16.90068138,17.56013046,17.68323516,17.55136167,17.37880314,17.15667664,17.01230928,16.97772278,16.9275685,16.94687682,17.14312426,17.66526702,18.20779641,18.50768614,18.13003273,17.17756944,15.74831901,13.92537538,11.82513702,9.665197467,7.616732832,5.82224028,4.378253919,3.295467114,2.552440766,2.0712499,1.795785599,1.635092835,1.496313473,1.371393113,1.275291417,1.182717574,1.112275863,1.00235083,0.896081083,0.795815265,0.7095588,0.618284456,0.518327258,0.412056922,0.342535817,0.299748884,0.280058745,0.260163597,0.234506618,0.195113432,0.180213472,0.178972317,0.168594768,0.142986051,0.104912272,0.084512373,0.072979018,0.068427398,0.054899253,0.036343012,0.027856356,0.020844812,0.003115837];
        pixsize_x = 0.0488;
    
        profile_z = [0.01122151,0.037043457,0.055905633,0.067476145,0.101606075,0.147395981,0.160645832,0.152304632,0.159424751,0.163896763,0.169680363,0.196223639,0.214644998,0.225082251,0.232238077,0.254297234,0.278732259,0.292217258,0.335025516,0.379584586,0.410853489,0.463471536,0.507292327,0.536697977,0.527816242,0.552747422,0.628048892,0.723337985,0.807450928,0.956416871,1.352841614,2.199171228,3.722665246,5.941428727,8.531521939,10.91177728,12.93052832,14.96653634,17.24566844,19.27696456,20.7731072,21.7132782,22.13825704,22.18586875,21.89919803,21.46488533,21.20696144,21.0957868,20.64726507,19.97215536,19.38971607,18.89876385,18.26037989,17.26777141,15.7770187,13.89955935,11.92919289,10.06077452,8.179242257,6.173345558,4.167567658,2.588757424,1.577823161,1.060139575,0.812361896,0.682799327,0.598371122,0.56108859,0.523283668,0.491845792,0.474818283,0.462280161,0.441798255,0.39815787,0.356459313,0.349337371,0.335332333,0.290866174,0.242051141,0.219375094,0.196281315,0.17916923,0.178452663,0.149048045,0.10430868,0.094567442,0.106447417,0.109838232,0.084505591,0.060842127];
        pixsize_z = 0.0488;
    
    # source https://github.com/CatSim/Shared/blob/master/LS16/focal_spot/Source_Profiles_GeminiSmallFS.m
    elif shape=='gemini_small':
        profile_x = [0.012893,0.026121,0.043449,0.070592,0.108774,0.173457,0.294290,0.531028,0.993369,1.741329,2.743087,3.950925,5.423170,7.053802,8.649088,9.955457,10.848483,11.206896,11.134795,10.738778,10.243423,9.873508,9.676655,9.530696,9.603707,10.002857,10.612582,11.110688,11.244208,10.852363,9.888867,8.405638,6.675894,5.046239,3.663394,2.530140,1.685539,1.107227,0.717903,0.446146,0.261154,0.153702,0.103925,0.067941,0.047467,0.021803,0.003971];
        pixsize_x = 0.0464;
    
        profile_z = [0.011816,0.023066,0.038196,0.052838,0.071710,0.100934,0.139907,0.193850,0.296586,0.474521,0.792443,1.336304,2.236065,3.543733,5.280515,7.368869,9.695811,11.994932,14.201917,16.089695,17.509026,18.390196,18.677665,18.309601,17.260781,15.665527,13.577794,11.167616,8.663415,6.338861,4.386284,2.867262,1.798276,1.080994,0.654836,0.409593,0.265624,0.172353,0.102244,0.056931,0.032456];
        pixsize_z = 0.0464;
    
    # source https://github.com/CatSim/Shared/blob/master/LS16/focal_spot/Source_Profiles_GeminiLargeFS.m
    elif shape=='gemini_large':
        profile_x = [0.001217,0.011534,0.023534,0.036320,0.044153,0.053756,0.055490,0.043085,0.052445,0.069958,0.094850,0.108546,0.115268,0.124917,0.123284,0.141291,0.155781,0.166018,0.169871,0.192366,0.221780,0.249419,0.274564,0.313533,0.367612,0.462818,0.610051,0.781937,0.979068,1.248106,1.588449,2.025820,2.660474,3.553795,4.884528,6.713625,9.158815,12.154306,15.119354,17.196880,18.305646,18.629618,18.328303,17.427549,16.374478,15.472189,14.831895,14.443021,14.292207,14.339465,14.384918,14.599977,15.117909,15.783555,16.697157,17.841069,19.074905,19.848045,19.823042,18.770598,16.741811,13.803715,10.466912,7.327921,4.742165,2.863951,1.703527,1.075854,0.755858,0.587312,0.501951,0.439695,0.390880,0.359000,0.328622,0.304260,0.259487,0.228507,0.201676,0.177736,0.168137,0.162674,0.158720,0.137634,0.113236,0.098851,0.099202,0.101864,0.086036,0.058063,0.048352,0.036976,0.021329,0.013369,0.011736,0.000000,0.000000,0.001387,0.014721];
        pixsize_x = 0.0464;
    
        profile_z = [0.007763,0.005397,0.024240,0.025931,0.022500,0.030876,0.045116,0.057306,0.041716,0.031764,0.025039,0.042830,0.060536,0.076128,0.081091,0.104786,0.113694,0.113882,0.119821,0.139860,0.147634,0.151967,0.172218,0.193535,0.228361,0.256808,0.274696,0.302391,0.322266,0.331279,0.372759,0.421103,0.455344,0.492866,0.583136,0.715937,1.013979,1.717099,3.039887,5.001790,7.423972,10.008004,12.657330,15.041187,16.942861,18.296304,19.259478,19.823035,20.168685,20.468425,20.715723,20.905262,21.059482,21.136368,20.995710,20.812532,20.611677,20.372728,19.873433,19.156901,18.235254,16.951088,15.073650,12.651004,10.005053,7.454994,5.166482,3.317686,2.019112,1.243938,0.823856,0.593923,0.464257,0.393779,0.333818,0.275932,0.232665,0.198768,0.179056,0.174810,0.173145,0.179278,0.150423,0.117226,0.083614,0.083906,0.077572,0.075947,0.064407,0.056382,0.035193,0.017030,0.003477];
        pixsize_z = 0.0464;
    
    intensity_x = np.array(profile_x);
    intensity_z = np.array(profile_z);
    int2d = intensity_x[:, None]@intensity_z[None, :]
    
    return int2d, pixsize_x, pixsize_z

if __name__=="__main__":
    for shape in ['performix', 'pharos_large', 'pharos_small', 'gemini_large', 'gemini_small']:
        int2d, pixsize_x, pixsize_z = make_source(shape)
        with open("{}.npz".format(shape), 'wb') as f:
            np.savez(f, data=int2d, pixsize_x=pixsize_x, pixsize_z=pixsize_z, xstart=0, ystart=0)
