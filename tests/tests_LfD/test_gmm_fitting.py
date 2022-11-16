import unittest
from pathlib import Path

import numpy as np

from team.aligned_trajectories import AlignedTrajectories
from team.gaussian_mixture_regression import GMR
from team.probabilistic_encoding import ProbabilisticEncoding


class ProbabilisticEncodingTest(unittest.TestCase):
    @staticmethod
    def _create_trajectory_and_prob_encoding() -> tuple[
        AlignedTrajectories, ProbabilisticEncoding
    ]:
        base_path = Path(__file__).parent.absolute()
        data_path = str(Path(base_path, "data"))
        trajectories = AlignedTrajectories.load_dataset_and_preprocess(data_path)
        pe = ProbabilisticEncoding(
            trajectories,
            max_nb_components=10,
            min_nb_components=2,
            iterations=1,
            random_state=0,
        )
        return trajectories, pe

    def test_probabilistic_encoding(self):
        _, pe = self._create_trajectory_and_prob_encoding()
        # check best number GMM components
        self.assertEqual(pe.gmm.n_components, 3)
        # check norm of covariance matrices
        for i, norm in enumerate([333, 591, 5]):
            self.assertEqual(int(np.linalg.norm(pe.gmm.covariances_[i])), norm)

    def test_nb_gmm_components(self):

        # dummy data
        data_3 = np.array([0.4, 0.2, 0.3, 0.35, 0.25, 0.33, 0.8])
        data_4 = np.array([0.3, 0.25, 0.28, 0.27, 0.26, 0.29, 0.26])
        data_5 = np.array([0.3, 0.23, 0.35, 0.20, 0.17, 0.25, 0.34])
        _, pe = self._create_trajectory_and_prob_encoding()
        pe.js_metric_results = {3: data_3, 4: data_4, 5: data_5}
        pe._iterations = 7
        nb_comp_js = pe._statistically_significant_component()
        self.assertEqual(nb_comp_js, 4)

    def test_gmr_implementation(self):

        traj, pe = self._create_trajectory_and_prob_encoding()
        # compute regression curve
        regression = GMR(traj, pe)
        # check prediction vector, first timestamp
        np.testing.assert_array_almost_equal(
            regression.prediction[0, :],
            np.array([0.0, 1.5, -20.8, 68.6, 8.4, -50.9, -12.9]),
            decimal=1,
        )

        # check prediction vector, last timestamp
        np.testing.assert_array_almost_equal(
            regression.prediction[-1, :],
            np.array([10.3, 18.2, 39.4, 0.2, 22.7, -44.7, -20.3]),
            decimal=1,
        )
