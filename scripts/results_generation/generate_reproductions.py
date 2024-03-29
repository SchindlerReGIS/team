import argparse
from pathlib import Path

import numpy as np

from team.aligned_trajectories import AlignedTrajectories
from team.dynamical_movement_primitives import DynamicMovementPrimitives
from team.gaussian_mixture_regression import GMR
from team.probabilistic_encoding import ProbabilisticEncoding


def main():
    task_list = [
        "opening",
        "door_closing",
        "brush_homing",
        "brush_picking_up",
        "rail_cleaning",
    ]
    # read noise standard deviation from input argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--std-dev", type=float, default=1, help="noise standard deviation"
    )
    parser.add_argument(
        "--data-folder", type=str, default="maintenance_task", help="data folder name"
    )
    parser.add_argument(
        "--nb-repro", type=int, default=30, help="number of reproduction"
    )
    args = parser.parse_args()
    std_dev = args.std_dev
    if std_dev <= 0:
        raise ValueError("std-dev has to be strictly positive")

    base_folder = Path(__file__).parent.parent.parent.joinpath(
        f"data/{args.data_folder}"
    )
    base_folder.mkdir()
    experience_folder = base_folder.joinpath(f"maintenance_noise_{std_dev}")
    experience_folder.mkdir()
    for task in task_list:
        nb_repro = args.nb_repro
        # data loading
        data_dir = Path(__file__).parent.parent.parent.joinpath(
            f"data/learning_from_demonstrations/{task}"
        )
        # create task folder
        folder_path = experience_folder.joinpath(f"{task}")
        folder_path.mkdir()
        # data preprocessing
        trajectories = AlignedTrajectories.load_dataset_and_preprocess(str(data_dir))
        # GMM
        pe = ProbabilisticEncoding(
            trajectories, max_nb_components=10, min_nb_components=4, iterations=20
        )
        # GMR
        regression = GMR(trajectories, pe)
        target = regression.prediction[-1, 1:]
        initial_state = regression.prediction[0, 1:]
        dmp = DynamicMovementPrimitives(
            regression=regression.prediction,
            c_order=1,
            initial_joints=initial_state,
            goal_joints=target,
        )

        dmp.save_dmp(folder_path)

        # generate reproductions
        for i in range(1, nb_repro + 1):
            # DMP
            target = regression.prediction[-1, 1:]
            initial_state = regression.prediction[0, 1:]

            # apply noise on both initial and target references
            noise_target = np.random.normal(scale=std_dev)
            target = target + noise_target
            noise_init = np.random.normal(scale=std_dev)
            initial_state = initial_state + noise_init

            dmp_traj = dmp.compute_joint_dynamics(goal=target, y_init=initial_state)
            reproduction_folder = Path(folder_path, "reproduction" + str(i))
            reproduction_folder.mkdir()

            dmp_traj.save(
                path_to_file=Path(reproduction_folder, "task_config.json"),
                initial_state=initial_state,
                target=target,
            )


if __name__ == "__main__":
    main()
