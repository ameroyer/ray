"""
[1] Mastering Diverse Domains through World Models - 2023
D. Hafner, J. Pasukonis, J. Ba, T. Lillicrap
https://arxiv.org/pdf/2301.04104v1.pdf

[2] Mastering Atari with Discrete World Models - 2021
D. Hafner, T. Lillicrap, M. Norouzi, J. Ba
https://arxiv.org/pdf/2010.02193.pdf
"""
# Run with:
# python run_regression_tests.py --dir [this file] --env DMC/[task]/[domain]
# e.g. --env=DMC/cartpole/swingup

from ray.rllib.algorithms.dreamerv3.dreamerv3 import DreamerV3Config


# Number of GPUs to run on.
num_gpus = 1

config = (
    DreamerV3Config()
    # Use image observations.
    .environment(env_config={"from_pixels": True})
    .resources(
        num_learner_workers=0 if num_gpus == 1 else num_gpus,
        num_gpus_per_learner_worker=1 if num_gpus else 0,
        num_cpus_for_local_worker=1,
    )
    .env_runners(num_envs_per_env_runner=4 * (num_gpus or 1), remote_worker_envs=True)
    .reporting(
        metrics_num_episodes_for_smoothing=(num_gpus or 1),
        report_images_and_videos=False,
        report_dream_data=False,
        report_individual_batch_item_stats=False,
    )
    # See Appendix A.
    .training(
        model_size="S",
        training_ratio=512,
        batch_size_B=16 * (num_gpus or 1),
    )
)
