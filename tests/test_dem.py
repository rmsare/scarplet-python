import os, sys
import dem
import unittest
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib.testing.decorators import image_comparison
import numpy as np
import filecmp

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'data/big_basin.tif')


class CalculationMethodsTestCase(unittest.TestCase):
    
    
    def setUp(self):
        
        self.dem = dem.DEMGrid(TESTDATA_FILENAME)

    def test_calculate_slope(self):

        sx, sy = self.dem._calculate_slope()

    def test_calculate_laplacian(self):

        del2z = self.dem._calculate_laplacian()
    
    def test_calculate_directional_laplacian(self):
        
        alpha = np.pi/4
        del2z = self.dem._calculate_directional_laplacian(alpha)

    def test_estimate_curvature_noiselevel(self):

        m, s = self.dem._estimate_curvature_noiselevel()

    def test_pad_boundary(self):
        
        dx = 5
        dy = 5
        grid = self.dem._griddata

        pad_x = np.zeros((self.dem._georef_info.ny, np.round(dx/2)))
        pad_y = np.zeros((np.round(dy/2), self.dem._georef_info.nx + 2*np.round(dx/2)))
        padded_grid = np.vstack([pad_y, np.hstack([pad_x, self.dem._griddata, pad_x]), pad_y])
        
        self.dem._pad_boundary(dx, dy)
        
        self.assertEqual(self.dem._griddata.all(), padded_grid.all(), "Grid padded incorrectly")


class BaseSpatialGridTestCase(unittest.TestCase):


    def setUp(self):

        self.dem = dem.BaseSpatialGrid(TESTDATA_FILENAME)

    #@image_comparison(baseline_images=['plot_gist_earth'], extensions=['png'])
    def test_plot(self):

        self.dem.plot(cmap='gist_earth')

    @unittest.skip("Skipping save test until dtype detect is implemented")
    def test_save(self): # known failure: datatype different in saved test file
        
        this_file = os.path.join(os.path.dirname(__file__), 'data/big_basin_test.tif')
        test_file = TESTDATA_FILENAME
        
        self.dem.save(this_file)

        self.assertTrue(filecmp.cmp(this_file, test_file, shallow=False), "GeoTIFF saved incorrectly")

if __name__ == "__main__":
    unittest.main()
