#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pykCSD
----------------------------------

Tests for `pykCSD` module.
"""

import unittest
import numpy as np

from pylab import *
from numpy.linalg import norm
from pykCSD.pykCSD import KCSD1D
from pykCSD.pykCSD import KCSD2D
from pykCSD import potentials as pt
from pykCSD import basis_functions as bf


class TestKCSD1D(unittest.TestCase):

    def setUp(self):
        pass

    def test_KCSD1D_int_pot(self):
        """results of int_pot function should be almost equal to kCSD1d (matlab) results"""

        expected_results = np.loadtxt('tests/test_datasets/KCSD1D/expected_pot_intargs.dat', delimiter=',')
        params = np.loadtxt('tests/test_datasets/KCSD1D/intarg_parameters.dat', delimiter=',')
        srcs = params[0]
        args = params[1]
        curr_pos = params[2]
        hs = params[3]
        Rs = params[4]
        sigmas = params[5]

        for i, expected_result in enumerate(expected_results):
            # the parameter names h, R were swapped
            kcsd_result = pt.int_pot_1D(src=srcs[i],
                                        arg=args[i],
                                        curr_pos=curr_pos[i],
                                        R=hs[i],
                                        h=Rs[i],
                                        sigma=sigmas[i],
                                        basis_func=bf.gauss_rescale_lim_1D)
            # print 'ex:', expected_result, ' kcsd:', kcsd_result
            self.assertAlmostEqual(expected_result, kcsd_result, places=3)

    def test_KCSD1D_pot_estimation_two_electrodes(self):
        """pykCSD calculated pots should be almost equal to kCSD1d (matlab) calculated pots"""
        # this is left only to show differences from the matlab version
        """params = {'x_min': 0.0, 'x_max': 1.0,
                    'x': np.array([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]),
                'source_type': 'gauss_lim'}
        k = KCSD1D(elec_pos=np.array([0.2, 0.7]),
                   sampled_pots=np.array([1.0, 0.5]),
                   params=params)
        k.calculate_matrices()
        k.estimate_pots()
        reference_pots = np.loadtxt('tests/test_datasets/KCSD1D/2_elec_pot.dat', skiprows=5)

        for i, expected_pot in enumerate(reference_pots):
            print 'kcsd:', k.estimated_pots[i], 'expected:', expected_pot
        plot(k.space_X, reference_pots)
        plot(k.space_X, k.estimated_pots)
        show()
        for i, expected_pot in enumerate(reference_pots):
            self.assertAlmostEqual(k.estimated_pots[i], expected_pot, places=1)"""
        pass

    def test_KCSD1D_csd_estimation_two_electrodes(self):
        """pykCSD calculated CSD should be almost equal to kCSD1d (matlab) calculated CSD"""
        # this is left only to show differences from the matlab version
        """params = {'x_min': 0.0, 'x_max': 1.0,
                 'x': np.array([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]),
                 'source_type': 'gauss_lim'}
        k = KCSD1D(elec_pos=np.array([0.2, 0.7]),
                   sampled_pots=np.array([1.0, 0.5]),
                   params=params)
        k.calculate_matrices()
        k.estimate_csd()
        reference_csd = np.loadtxt('tests/test_datasets/KCSD1D/2_elec_csd.dat', skiprows=5)
        for i, expected_csd in enumerate(reference_csd):
            print 'csd:', k.estimated_csd[i], 'expected:', expected_csd

        for i, expected_csd in enumerate(reference_csd):
            self.assertAlmostEqual(k.estimated_csd[i], expected_csd, places=0)"""
        pass

    def test_KCSD1D_cross_validation_two_electrodes(self):
        """cross validation should promote high lambdas in this case"""

        params = {'x_min': 0.0, 'x_max': 1.0, 'gdX': 0.1,
                  'source_type': 'gauss_lim'}
        k = KCSD1D(elec_pos=np.array([0.2, 0.7]),
                   sampled_pots=np.array([1.0, 0.5]),
                   params=params)
        k.calculate_matrices()
        k.estimate_pots()
        lambdas = np.array([0.1, 0.5, 1.0])
        k.lambd = k.choose_lambda(lambdas)
        self.assertEquals(k.lambd, 1.0)

    def test_KCSD1D_zero_pot(self):
        """if measured potential is 0, the calculated potential should be 0"""

        params = {'n_sources': 20, 'dist_density': 20,
                  'source_type': 'gauss_lim'}
        k_zero = KCSD1D(elec_pos=np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                        sampled_pots=[0.0, 0.0, 0.0, 0.0, 0.0],
                        params=params)
        k_zero.calculate_matrices()
        k_zero.estimate_pots()
        self.assertAlmostEqual(norm(k_zero.estimated_pots), 0.0, places=10)

    def test_KCSD1D_zero_csd(self):
        """if measured potential is 0, the calculated CSD should be 0"""

        params = {'n_sources': 20, 'dist_density': 20,
                  'source_type': 'gauss_lim'}
        k_zero = KCSD1D(elec_pos=np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                        sampled_pots=[0.0, 0.0, 0.0, 0.0, 0.0],
                        params=params)
        k_zero.calculate_matrices()
        k_zero.estimate_csd()
        self.assertAlmostEqual(norm(k_zero.estimated_csd), 0.0, places=10)

    def test_KCSD1D_incorrect_electrode_number(self):
        """if there are more electrodes than pots, it should raise exception"""
        with self.assertRaises(Exception):
            k = KCSD1D(elec_pos=[0, 1, 2], sampled_pots=[0, 1])

    def test_KCSD1D_duplicated_electrode(self):
        """if two electrodes are at the same spot, it should raise exception"""
        with self.assertRaises(Exception):
            k = KCSD1D(elec_pos=[0, 0], sampled_pots=[0, 0])

    def test_KCSD1D_time_frames(self):
        """given array of dimension (pots, time) it should calculate pots and csd for every time frame"""
        # missing functionality
        pass

    def tearDown(self):
        pass


class TestKCSD1D_full_reconstruction(unittest.TestCase):

    def setUp(self):
        self.sigma = 1.0
        self.xmin = -5.0
        self.xmax = 11.0
        self.x = np.linspace(self.xmin, self.xmax, 100)
        self.true_csd = 1.0 * np.exp(-(self.x - 2.)**2/(2 * np.pi * 0.5))
        self.true_csd += 0.5 * np.exp(-(self.x - 7)**2/(2 * np.pi * 1.0))
        self.h = .3

        def calculate_pot(csd, z, z0):
            pot = np.trapz((np.sqrt((z0 - z)**2 + self.h**2) - np.abs(z0 - z)) * csd, z)
            pot *= 1.0/(2 * self.sigma)
            return pot

        self.elec_pos = np.linspace(self.xmin, self.xmax, 20)
        self.true_pots = [calculate_pot(self.true_csd, self.x, x0) for x0 in self.x]
        self.meas_pot = np.array([calculate_pot(self.true_csd, self.x, x0) for x0 in self.elec_pos])

    def test_KCSD1D_pot_reconstruction(self):
        """reconstructed pots should be similar to model pots"""

        params = {'sigma': self.sigma, 'source_type': 'gauss_lim',
                  'x_min': self.xmin, 'x_max': self.xmax,
                  'h': self.h, 'n_src': 20}
        k = KCSD1D(self.elec_pos, self.meas_pot, params)
        k.calculate_matrices()
        k.estimate_pots()
        """print np.max(k.estimated_pots)
        plot(k.space_X, k.estimated_pots)
        plot(self.x, self.true_pots)
        scatter(k.elec_pos, k.sampled_pots)
        show()"""
        for estimated_pot, true_pot in zip(k.estimated_pots, self.true_pots):
            self.assertAlmostEqual(estimated_pot, true_pot, places=1)

    def test_KCSD1D_csd_reconstruction(self):
        """reconstructed csd should be similar to model csd"""

        params = {'sigma': self.sigma, 'source_type': 'gauss_lim',
                  'x_min': self.xmin, 'x_max': self.xmax, 'h': self.h}
        k = KCSD1D(self.elec_pos, self.meas_pot, params)
        k.calculate_matrices()
        k.estimate_csd()
        """print np.max(k.estimated_csd)
        plot(k.estimated_csd)
        plot(self.true_csd)
        show()
        print k.X_src"""
        for estimated_csd, true_csd in zip(k.estimated_csd, self.true_csd):
            self.assertAlmostEqual(estimated_csd, true_csd, places=1)

    def test_KCSD1D_lambda_choice(self):
        """for potentials calculated from model, lambda < 1.0"""

        params = {'sigma': self.sigma, 'source_type': 'gauss_lim',
                  'x_min': -5.0, 'x_max': 10.0, 'h': self.h}
        k = KCSD1D(self.elec_pos, self.meas_pot, params)
        k.calculate_matrices()
        lambdas = np.array([100.0/2**n for n in xrange(1, 20)])
        k.lambd = k.choose_lambda(lambdas)
        k.estimate_pots()

        self.assertLess(k.lambd, 1.0)


class TestKCSD2D(unittest.TestCase):

    def setUp(self):
        pass

    def test_KCSD2D_int_pot(self):
        """results of int_pot function should be almost equal to kCSD2D (matlab) results"""

        expected_results = np.loadtxt('tests/test_datasets/KCSD2D/expected_pot_intargs_2D.dat', delimiter=',')
        params = np.loadtxt('tests/test_datasets/KCSD2D/intarg_parameters_2D.dat', delimiter=',')
        xps = params[0]
        yps = params[1]
        xs = params[2]
        Rs = params[3]
        hs = params[4]
        for i, expected_result in enumerate(expected_results):
            kcsd_result = pt.int_pot_2D(xp=xps[i], yp=yps[i], x=xs[i],
                                        R=Rs[i], h=hs[i],
                                        basis_func=bf.gauss_rescale_lim_2D)
            self.assertAlmostEqual(expected_result, kcsd_result, places=3)

    def test_KCSD2D_zero_pot(self):
        elec_pos = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        pots = np.array([0, 0, 0, 0])
        k = KCSD2D(elec_pos, pots)
        k.calculate_matrices()
        k.estimate_pots()
        for pot in k.estimated_pots.flatten():
            self.assertAlmostEqual(pot, 0.0, places=5)

    def test_KCSD2D_zero_csd(self):
        elec_pos = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        pots = np.array([0, 0, 0, 0])
        k = KCSD2D(elec_pos, pots)
        k.calculate_matrices()
        k.estimate_csd()
        for csd in k.estimated_csd.flatten():
            self.assertAlmostEqual(csd, 0.0, places=5)

    def tearDown(self):
        pass


class TestKCSD2D_full_recostruction(unittest.TestCase):

    def setUp(self):
        elec_pos = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_elecs.dat', delimiter=',')
        pots = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_pots.dat', delimiter=',')
        params = {'n_sources': 9, 'gdX': 0.1, 'gdY': 0.1}
        self.k = KCSD2D(elec_pos, pots, params)
        self.k.calculate_matrices()

    def test_KCSD2D_R_five_electrodes(self):
        expected_R = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_R.dat', delimiter=',')
        self.assertAlmostEqual(self.k.R, expected_R, places=5)

    def test_KCSD2D_b_pot_five_electrodes(self):
        expected_b_pot = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_bpot.dat', delimiter=',')
        err = norm(expected_b_pot - self.k.b_pot_matrix, ord=2)
        """fig, (ax11, ax21, ax22) = plt.subplots(1, 3)

        ax11.imshow(expected_b_pot,
                    interpolation='none', aspect='auto')
        ax11.set_title('matlab')
        ax11.autoscale_view(True, True, True)

        ax21.imshow(self.k.b_pot_matrix,
                    interpolation='none', aspect='auto')
        ax21.set_title('python')
        ax21.autoscale_view(True, True, True)

        ax22.imshow(expected_b_pot - self.k.b_pot_matrix,
                    interpolation='none', aspect='auto')
        ax22.set_title('diff')
        ax22.autoscale_view(True, True, True)

        show()"""
        self.assertAlmostEqual(err, 0.0, places=3)

    def test_KCSD2D_k_pot_five_electrodes(self):
        expected_k_pot = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_kpot.dat', delimiter=',')
        err = norm(expected_k_pot - self.k.k_pot, ord=2)
        self.assertAlmostEqual(err, 0.0, places=3)

    def test_KCSD2D_dist_table(self):
        expected_dt = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_dist_table.dat', delimiter=',')
        err = norm(expected_dt - self.k.dist_table)
        """plot(expected_dt-self.k.dist_table)
        show()"""
        self.assertAlmostEqual(err, 0.0, places=4)

    def test_KCSD2D_b_src_matrix_five_electrodes(self):
        expected_b_src_matrix = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_b_src_matrix.dat', delimiter=',')

        """fig, (ax11, ax21, ax22) = plt.subplots(1, 3)
        ax11.imshow(expected_b_src_matrix,
                    interpolation='none', aspect='auto')
        ax11.set_title('matlab')
        ax11.autoscale_view(True,True,True)

        ax21.imshow(self.k.b_src_matrix,
                    interpolation='none', aspect='auto')
        ax21.set_title('python')
        ax21.autoscale_view(True,True,True)

        ax22.imshow(expected_b_src_matrix - self.k.b_src_matrix,
                    interpolation='none', aspect='auto')
        ax22.set_title('diff')
        ax22.autoscale_view(True,True,True)

        show()"""
        err = norm(expected_b_src_matrix - self.k.b_src_matrix)
        self.assertAlmostEqual(err, 0.0, places=4)

    def test_KCSD2D_pot_estimation_five_electrodes(self):
        self.k.estimate_pots()
        expected_pots = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_estimated_pot.dat', delimiter=',')
        err = norm(expected_pots - self.k.estimated_pots, ord=2)
        """fig, (ax11, ax21, ax22) = plt.subplots(1, 3)

        ax11.imshow(expected_pots, interpolation='none', aspect='auto')
        ax11.set_title('matlab')
        ax11.autoscale_view(True, True, True)

        ax21.imshow(self.k.estimated_pots, interpolation='none', aspect='auto')
        ax21.set_title('python')
        ax21.autoscale_view(True, True, True)

        ax22.imshow(expected_pots - self.k.estimated_pots,
                    interpolation='none', aspect='auto')
        ax22.set_title('diff')
        ax22.autoscale_view(True, True, True)

        show()"""
        # print np.max(expected_pots - self.k.estimated_pots)
        self.assertAlmostEqual(err, 0.0, places=2)

    def test_KCSD2D_csd_estimation_five_electrodes(self):
        self.k.estimate_csd()
        expected_csd = np.loadtxt('tests/test_datasets/KCSD2D/five_elec_estimated_csd.dat', delimiter=',')
        err = norm(expected_csd - self.k.estimated_csd, ord=2)
        """fig, (ax11, ax21, ax22) = plt.subplots(1, 3)

        ax11.imshow(expected_csd,
                    interpolation='none', aspect='auto')
        ax11.set_title('matlab')
        ax11.autoscale_view(True, True, True)

        ax21.imshow(self.k.estimated_csd,
                    interpolation='none', aspect='auto')
        ax21.set_title('python')
        ax21.autoscale_view(True, True, True)

        ax22.imshow(expected_csd - self.k.estimated_csd,
                    interpolation='none', aspect='auto')
        ax22.set_title('diff')
        ax22.autoscale_view(True, True, True)

        show()"""
        # print np.max(expected_csd - self.k.estimated_csd)
        self.assertAlmostEqual(err, 0.0, places=0)

    def test_KCSD2D_cross_validation_five_electrodes(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
