# Copyright 2020, General Electric Company. All rights reserved. See https://github.com/xcist/code/blob/master/LICENSE
import ctypes

import json
import os
import struct

import numpy as np

'''
Common tool functions.
Mingye Wu, GE Research
'''


def check_value(a):
    #return
    print(type(a).__name__)
    if type(a) is np.ndarray:
        print(a.shape, a.dtype)
    print(a,'\n')


def make_col(a):
    a = a.reshape(a.size, 1)
    return a


def feval(funcName, *args):
    try:
        md = __import__(funcName)
    except:
        md = __import__("catsim.pyfiles."+funcName, fromlist=[funcName])  # equal to: from catsim.foo import foo
    strip_leading_module = '.'.join(funcName.split('.')[1:])
    func_name_only = funcName.split('.')[-1]

    if len(strip_leading_module) > 0:
        eval_name = f"md.{strip_leading_module}.{func_name_only}"
    else:
        eval_name = f"md.{func_name_only}"
    return eval(eval_name)(*args)


def load_C_lib():
    lib_path = my_path.paths["lib"]
    my_path.add_dir_to_path(lib_path)

    # load C/C++ lib
    ll = ctypes.cdll.LoadLibrary
    if os.name == "nt":
        libFile = "libcatsim64.dll"
    else:
        libFile = "libcatsim.so"
    clib = ll(os.path.join(lib_path, libFile))
    
    return clib


class emptyCFG:
    pass


class PathHelper:
    def __init__(self):
        self._base_dir = os.getcwd()
        # Locate paths of lib and data.
        self.paths = {}
        self.paths["main"] = os.path.dirname(os.path.abspath(__file__))
        self.paths["top"] = os.path.split(self.paths["main"])[0]
        self.paths["cfg"] = os.path.join(self.paths["top"], 'cfg')
        self.paths["lib"] = os.path.join(self.paths["top"], 'lib')
        self.paths["bowtie"] = os.path.join(self.paths["top"], 'bowtie')
        self.paths["material"] = os.path.join(self.paths["top"], 'material')
        self.paths["phantom"] = os.path.join(self.paths["top"], 'phantom')
        self.paths["scatter"] = os.path.join(self.paths["top"], 'scatter')
        self.paths["spectrum"] = os.path.join(self.paths["top"], 'spectrum')
        self.extra_search_paths = []
        self.read_catsim_init()

    def base(self, *args):
        return os.path.join(self._base_dir, *args)

    def add_search_path(self, path):
        if not os.path.isdir(path):
            print(f"***WARNING: {path} does not exist.")
        if path not in self.extra_search_paths:
            self.extra_search_paths.append(path)

    def find(self, key, filename, extension):
        path = self.paths[key]

        # check fully-qualified path and/or current directory first
        if os.path.isfile(filename):
            return filename

        if os.path.isfile(f"{filename}{extension}"):
            return f"{filename}{extension}"

        # check user-defined search paths BEFORE default paths
        for p in self.extra_search_paths:
            # if we want to limit the depth at some point, then we might want to use the walkDir module
            # https://walkdir.readthedocs.io/en/stable/
            for p2, dirs, files in os.walk(p):
                if os.path.isfile(os.path.join(p2, filename)):
                    return os.path.join(p2, filename)
                elif os.path.isfile(os.path.join(p2, f"{filename}{extension}")):
                    return os.path.join(p2, f"{filename}{extension}")
                elif os.path.isfile(os.path.join(p2, key, filename)):
                    return os.path.join(p2, key, filename)
                elif os.path.isfile(os.path.join(p2, key, f"{filename}{extension}")):
                    return os.path.join(p2, key, f"{filename}{extension}")

        # check path and its subdirectories
        for p2, dirs, files in os.walk(path):
            if os.path.isfile(os.path.join(p2, filename)):
                return os.path.join(p2, filename)
            elif os.path.isfile(os.path.join(p2, f"{filename}{extension}")):
                return os.path.join(p2, f"{filename}{extension}")

        # exhausted all the paths to search and could not find the file
        raise Exception("Cannot find %s or %s%s" %(filename, filename, extension))

    def find_dir(self, key, dir_name):
        path = self.paths[key]

        # check fully-qualified path and/or current directory first
        if os.path.isdir(dir_name):
            return dir_name

        # check user-defined search paths BEFORE default paths
        for p in self.extra_search_paths:
            if os.path.isdir(os.path.join(p, dir_name)):
                return os.path.join(p, dir_name)
            elif os.path.isdir(os.path.join(p, key, dir_name)):
                return os.path.join(p, key, dir_name)

        if os.path.isdir(os.path.join(path, dir_name)):
            return os.path.join(path, dir_name)
        # exhausted all the paths to search and could not find the file
        raise Exception("Cannot find directory %s" % (dir_name))

    def read_catsim_init(self):
        cwd_init_file = os.path.join(self._base_dir, ".catsim")
        self.read_catsim_file(cwd_init_file)

        if os.name == "nt":
            # on my PC with a C: and D: drive
            # HOMEDIR=D:\Users\USERNAME
            # USERPROFILE=c:\Users\USERNAME
            if "HOMEDIR" in os.environ:
                user_home = os.environ.get("HOMEDIR")
                root_init_file = os.path.join(user_home, ".catsim")
                self.read_catsim_file(root_init_file)

            if "USERPROFILE" in os.environ:
                user_home = os.environ.get("USERPROFILE")
                root_init_file = os.path.join(user_home, ".catsim")
                self.read_catsim_file(root_init_file)
        else:
            # on Linux & Mac, HOME is home directory of the user
            if "HOME" in os.environ:
                user_home = os.environ.get("HOME")
                root_init_file = os.path.join(user_home, ".catsim")
                self.read_catsim_file(root_init_file)

    def read_catsim_file(self, filename):
        if os.path.isfile(filename):
            try:
                with open(filename, "r") as f:
                    init = json.load(f)
            except BaseException as err:
                print(f"***WARNING: Unable to read file: {filename} as json: {err=}, {type(err)=}")
            else:
                if "search_paths" in init:
                    for p in init["search_paths"]:
                        self.add_search_path(p)
                else:
                    print(f"***WARNING: search_paths entry not found in {filename}")

    @staticmethod
    def add_dir_to_path(dir_name):
        if dir_name not in os.environ["PATH"]:
            os.environ["PATH"] = f'{dir_name};{os.environ["PATH"]}'

    @staticmethod
    def linux_style_path(filename):
        return filename.replace("\\", "/")


class CFG:
    def __init__(self, *para):
        # initialize cfg: defaults, paths, and C lib
        cfg = source_cfg("Phantom_Default")
        cfg = source_cfg("Scanner_Default", cfg)
        cfg = source_cfg("Protocol_Default", cfg)
        cfg = source_cfg("Physics_Default", cfg)
        cfg = source_cfg("Recon_Default", cfg)
        cfg.resultsName = "simulation_test"

        if not hasattr(cfg, 'clib'):
            cfg.clib = load_C_lib()
        
        # source cfgFiles if para are defined
        # note: the later cfgFile overrides the former ones
        for cfgFile in para:
            cfg = source_cfg(cfgFile, cfg)
        
        self.pass_cfg_to_self(cfg)

    def pass_cfg_to_self(self, cfg):
        # add or override cfg attributes to self
        for name1, value1 in vars(cfg).items():
            if not hasattr(self, name1):
                setattr(self, name1, value1)
            else:
                for name2, value2 in eval("vars(cfg.%s).items()" % name1):
                    setattr(getattr(self, name1), name2, value2)
            
    def load(self, cfgFile):
        cfg = source_cfg(cfgFile)
        self.pass_cfg_to_self(cfg)


def source_cfg(*para):
    '''
    First para must be cfg filename.
    Second para is optional, if defined and is cfg, attr will be added to cfg.
    Calling source_cfg(cfg_file, cfg) will add or override attributes to cfg.
    '''
    # find cfg file
    cfg_file = my_path.find("cfg", para[0], ".cfg")

    # cfg is initialized before sourcing cfg_file
    if len(para)<2:
        cfg = emptyCFG()
    else:
        cfg = para[1]
        
    # initialize structs in cfg and structs
    attrList = ['sim', 'det', 'detNew', 'src', 'srcNew', 'spec', 'protocol', 'scanner', 'phantom', 'physics', 'recon']
    for attr in attrList:
        if not hasattr(cfg, attr):
            setattr(cfg, attr, emptyCFG())
        if not attr in dir():
            exec("%s = emptyCFG()" % attr)
        
    # execute scripts in cfg file
    exec(open(cfg_file).read())
    
    # add or override the attributes in the original cfg
    for attr in attrList:
        for name, value in eval("vars(%s).items()" % attr):
            setattr(getattr(cfg, attr), name, value)
    
    return cfg
    
def vectornorm(xyz):
    if xyz.shape[0]!=3:
        print('ERROR : argument of vectornorm has to be of size 3 x n');
        return
    else:
        norms = np.sqrt(np.square(xyz).sum(axis=0))
        norms = make_col(norms)
        return norms


def overlap(x0, y0, x1):
    # length
    n0 = len(x0)
    n1 = len(x1)
    
    # boundaries
    b0 = get_vector_boundaries(x0)
    b1 = get_vector_boundaries(x1)
    
    # default
    y1 = np.zeros(x1.shape)
    
    # pre-loop, find the start boundaries
    i = 0
    j = 0
    previous = b1[j]
    while b0[i] < previous:
        i += 1
        if i>=n0:
            return y1
    if i == 0:
        previous = b0[0]
        while b1[j] < previous:
            j += 1
            if j >= n1:
                return y1    
    
    # main loop
    while j < n1:
        if b0[i+1] < b1[j+1]:
            y1[j] += y0[i]*(b0[i+1]-previous)/(b1[j+1]-b1[j])
            previous = b0[i+1]
            i += 1
            if i >= n0:
                return y1
        else:
            y1[j] += y0[i]*(b1[j+1]-previous)/(b1[j+1]-b1[j])
            previous = b1[j+1]
            j += 1  
    
    return y1


def get_vector_boundaries(x):
    # x can be scalar, vector, or [n, 1] array
    
    if len(x) == 1:
        b = np.array([x*(1-1e-6), x*(1+1e-6)])
    else:
        b = (x[0:-1]+x[1:])/2
        b = np.concatenate(([x[0]-0.5*(x[1]-x[0])], b, [x[-1]+0.5*(x[-1]-x[-2])]))
    return b


def rawread(fname, dataShape, dataType):
    # dataType is for numpy, ONLY allows: 'float'/'single', 'double', 'int'/'int32', 'uint'/'uint32', 'int8', 'int16' 
    #          they are single, double, int32, uin32, int8, int16
    with open(fname, 'rb') as fin:
        data = fin.read()
    
    # https://docs.python.org/3/library/struct.html
    switcher = {'float': ['f', 4, np.single], 
                'single': ['f', 4, np.single], 
                'double': ['d', 8, np.double], 
                'int': ['i', 4, np.int32], 
                'uint': ['I', 4, np.uint32],  
                'int32': ['i', 4, np.int32], 
                'uint32': ['I', 4, np.uint32], 
                'int8': ['b', 1, np.int8], 
                'int16': ['h', 2, np.int16]}
    fmt = switcher[dataType]
    data = struct.unpack("%d%s" % (len(data)/fmt[1], fmt[0]), data)
    
    data = np.array(data, dtype=fmt[2])
    if dataShape:
        data = data.reshape(dataShape)
    
    return data

def rawwrite(fname, data):
    with open(fname, 'wb') as fout:
        fout.write(data)


def conv2(img, h, mode='same'):
    h = np.rot90(h, 2) # rotate 180 degree
    img_row, img_col = img.shape
    h_row, h_col = h.shape
    if mode == 'full':
        zeroPad = np.zeros((h_row-1, img_col))
        extImg = np.vstack((zeroPad, img, zeroPad))
        zeroPad = np.zeros((extImg.shape[0], h_col-1))
        extImg = np.column_stack((zeroPad, extImg, zeroPad))
    elif mode == 'same':
        zeroPad = np.zeros((int(h_row/2), img_col))
        extImg = np.vstack((zeroPad, img, zeroPad))
        zeroPad = np.zeros((extImg.shape[0], int(h_col/2)))
        extImg = np.column_stack((zeroPad, extImg, zeroPad))
    else:
        extImg = img
    
    row_start, row_end = 0, extImg.shape[0]-h.shape[0]+1
    col_start, col_end = 0, extImg.shape[1]-h.shape[1]+1
    img_conv = np.zeros((row_end, col_end))
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            cur_region = extImg[r:r+h_row, c:c+h_col]
            img_conv[r, c] = np.sum(cur_region * h)
    
    if mode == 'same':
        if h_row%2 == 0:
            img_conv = img_conv[1:,:]
        if h_col%2 == 0:
            img_conv = img_conv[:,1:]
    
    return img_conv


my_path = PathHelper()
