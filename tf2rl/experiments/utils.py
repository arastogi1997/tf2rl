import os
import numpy as np
import joblib
import random

import tensorflow as tf


def save_path(samples, filename):
    joblib.dump(samples, filename, compress=3)


def restore_latest_n_traj(dirname):
    assert os.path.isdir(dirname)
    filenames = get_filenames(dirname)
    return load_trajectories(filenames)


def get_filenames(dirname, n_path=None):
    import re
    itr_reg = re.compile(r"step_(?P<step>[0-9]+)_epi_(?P<episodes>[0-9]+)_return_(?P<return_u>[0-9]+).(?P<return_l>[0-9]+).pkl")

    itr_files = []
    for _, filename in enumerate(os.listdir(dirname)):
        m = itr_reg.match(filename)
        if m:
            itr_count = m.group('step')
            itr_files.append((itr_count, filename))

    n_path = n_path if n_path is not None else len(itr_files)
    itr_files = sorted(itr_files, key=lambda x: int(x[0]), reverse=True)[:n_path]
    filenames = []
    for itr_file_and_count in itr_files:
        filenames.append(os.path.join(dirname, itr_file_and_count[1]))
    return filenames


def load_trajectories(filenames, max_steps=None):
    paths = []
    for filename in filenames:
        paths.append(joblib.load(filename))

    def get_obs_and_act(path):
        if max_steps is not None:
            return path['obs'][:max_steps], path['act'][:max_steps]
        else:
            return path['obs'], path['act']

    for i, path in enumerate(paths):
        if i == 0:
            obses, acts = get_obs_and_act(path)
        else:
            obs, act = get_obs_and_act(path)
            obses = np.vstack((obs, obses))
            acts = np.vstack((act, acts))
    return {'obses': obses, 'acts': acts}