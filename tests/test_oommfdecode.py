import sys, os
import StringIO
import tempfile
import numpy as np
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)

import unittest
from oommftools import oommfdecode


import StringIO
from oommftools.fnameutil import filterOnExtensions
import scipy.io as spio
import cPickle as pickle

class Test_oommfdecode_text(unittest.TestCase):
    def setUp(self):
        self.test_files_folder = 'testfiles'
        self.vector_file_text = os.path.join(TEST_DIR, 
                                        self.test_files_folder,
                                        'dw_edgefield_cut_cell4_160.ohf')
        self.headers_test = {'ystepsize': 4e-09, 'xnodes': 1250.0, 'valuemultiplier': 258967.81743932367, 'xbase': 2e-09, 'zstepsize': 8e-09, 'znodes': 1.0, 'zbase': 4e-09, 'ynodes': 40.0, 'ybase': 2e-09, 'xstepsize': 4e-09}
        self.extraCaptures_test =  {'MIFSource': 'C:/programs/oommf_old/simus/DW-150-8-transverse/DW_edgefield/dw_edgefield.mif', 'Iteration': 0.0, 'SimTime': 0.0, 'Stage': 0.0}
        self.vector_file_binary = os.path.join(TEST_DIR, 
                                        self.test_files_folder,
                                        'h2h_leftedge_40x4.ohf')

        self.targetarray_pickle = os.path.join(TEST_DIR, 
                                        self.test_files_folder,
                                        'targetarray_text.npy')
    def test_unpackFile_text_targetarray(self):
        (targetarray, headers, extraCaptures) = oommfdecode.unpackFile(self.vector_file_text)
        #np.save(self.targetarray_pickle, targetarray)
        self.assertEqual(targetarray.all(), np.load(self.targetarray_pickle).all())
        
    def test_unpackFile_text_headers(self):
        (targetarray, headers, extraCaptures) = oommfdecode.unpackFile(self.vector_file_text)
        self.assertEqual(headers, self.headers_test)
        
    def test_unpackFile_text_extracaptures(self):
        (targetarray, headers, extraCaptures) = oommfdecode.unpackFile(self.vector_file_text)
        self.assertEqual(extraCaptures, self.extraCaptures_test)

class Test_oommfdecode_binary(unittest.TestCase):
    def setUp(self):
        self.test_files_folder = 'testfiles'
        self.vector_file_binary = os.path.join(TEST_DIR, 
                                        self.test_files_folder,
                                        'h2h_leftedge_40x4.ohf')
        self.headers_test = {'ystepsize': 1e-08, 'xnodes': 160.0, 'valuemultiplier': 1.0, 'xbase': 5e-09, 'zstepsize': 1e-08, 'znodes': 4.0, 'zbase': 5e-09, 'ynodes': 40.0, 'ybase': 5e-09, 'xstepsize': 1e-08}
        
        self.extraCaptures_test =  {'MIFSource': '/local/home/donahue/oommf/app/oxs/examples/h2h_edgefield.mif', 'Iteration': 0.0, 'SimTime': 0.0, 'Stage': 0.0}
                                        
        self.targetarray_pickle = os.path.join(TEST_DIR, 
                                        self.test_files_folder,
                                        'targetarray_binary.npy')                                        
    def test_unpackFile_binary_targetarray(self):
        (targetarray, headers, extraCaptures) = oommfdecode.unpackFile(self.vector_file_binary)
        #np.save(self.targetarray_pickle, targetarray)
        self.assertEqual(targetarray.all(), np.load(self.targetarray_pickle).all())
        
    def test_unpackFile_binary_headers(self):
        (targetarray, headers, extraCaptures) = oommfdecode.unpackFile(self.vector_file_binary)
        self.assertEqual(headers, self.headers_test)
        
    def test_unpackFile_binary_extraCaptures(self):
        (targetarray, headers, extraCaptures) = oommfdecode.unpackFile(self.vector_file_binary)
        self.assertEqual(extraCaptures, self.extraCaptures_test)
        
class Test_pickleArray(unittest.TestCase):
    def setUp(self):
        self.array = np.array([1., 2., 3.])
        self.headers = {'Name': 'Headers', 'Value': 1}
        self.extraCaptures = {'Capture1': 1, 'Capture2': 'two'}
        self.filename = os.path.join(tempfile.gettempdir(),
                                        'test.npy')
        
    def test_pickle_array(self):
        oommfdecode.pickleArray(self.array, self.headers, self.extraCaptures, self.filename)
        with open(self.filename, "r") as input_file:
            e = pickle.load(input_file)
        self.assertEqual(e[0].all(), np.array([1., 2., 3.]).all())
        self.assertEqual(e[1], dict(self.headers.items() + self.extraCaptures.items()))
 
class Test_matlabifyArray(unittest.TestCase):
    def setUp(self):
        self.array = np.array([1., 2., 3.])
        self.headers = {'xstepsize': 1, 'ystepsize': 2, 'zstepsize': 3}
        self.extraCaptures = {'Capture1': 1, 'Capture2': 'two'}
        self.filename = os.path.join(tempfile.gettempdir(),
                                        'test.mat')
        
    def test_matlabify_array(self):
        oommfdecode.matlabifyArray(self.array, self.headers, self.extraCaptures, self.filename)
        e = spio.loadmat(self.filename)
        self.assertEqual(e['OOMMFData'].all(), np.array([[1., 2., 3.]]).all())
        self.assertEqual(e['Capture2'], np.array([u'two']))
        self.assertEqual(e['Capture1'], np.array([[1]]))
        self.assertEqual(e['GridSize'].all(), np.array([[1., 2., 3.]]).all())
        
class Test_textDecode(unittest.TestCase):
    def setUp(self):
        self.output = StringIO.StringIO()
        self.output.write('First line.\n')
        self.outArray = np.zeros((3, 3, 3), 3)
        self.headers = ['one', 'two', 'three']
        self.extraCaptures = {'a': 1, 'b': 2, 'c': 3}
    def test_textDecode(self):
        oommfdecode._textDecode(output, self.outArray, self.extraCaptures)
        
        
        
        