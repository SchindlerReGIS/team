from pathlib import Path
from typing import Optional

import numpy as np
from gmr import GMM

from team.aligned_trajectories import AlignedTrajectories
from team.probabilistic_encoding import ProbabilisticEncoding
from team.utility.handling_data import save_json_dict


class GMR:
    """
    Calculates the Gaussian Mixture Regression line from the probability encoding of the
    data. Each time step is used as query point and the corresponding predictions denote
    the regression line

    ```python
    # probabilistic encoding
    pe = ProbabilisticEncoding(trajectories=trajectories, iterations=10,
         max_nb_components=10, min_nb_components=2)
    # extraction of regression line from probability distributions and plot shown
    gmr = GMR(trajectories=trajectories, prob_encoding=pe)
    regression = gmr.prediction
    ```

    :param trajectories: preprocessed dataset
    :param prob_encoding: probabilistic encoding of the data through GMM models
    """

    def __init__(
        self,
        trajectories: AlignedTrajectories,
        prob_encoding: ProbabilisticEncoding,
        random_state: Optional[int] = None,
    ) -> None:
        self._trajectories = trajectories
        self._gmm = GMM(
            n_components=prob_encoding.gmm.n_components,
            priors=prob_encoding.gmm.weights_,
            means=prob_encoding.gmm.means_,
            covariances=np.array(prob_encoding.gmm.covariances_),
            random_state=random_state,
        )
        self.prediction = self._predict_regression()

    def _predict_regression(self) -> np.ndarray:
        """
        Computes the Gaussian Mixture Regression line

        :return: the predicted regression line
        """
        # extract first feature -> time vector (query points)
        x1 = self._trajectories.timestamps.reshape(-1, 1)
        x1_index = [0]
        # make predictions for all features
        y_predicted_mean = self._gmm.predict(x1_index, x1)
        # stack time vector with predictions
        y_predicted_mean = np.hstack((x1, y_predicted_mean))
        return y_predicted_mean

    def save_regression(self, dir_path: Path, exist_ok: bool = False) -> None:
        """
        Saves regression information in a json file.

        :param dir_path: path to the directory where the data will be saved
        :param exist_ok: boolean to allow file override
        """

        # define file path and data to store
        file_path = dir_path.joinpath("regression.json")
        joints = self.prediction[:, 1:]
        data = {
            "regression": joints.tolist(),
        }
        save_json_dict(file_path, data, exist_ok)
