import pickle

import numpy as np

from lab.model import LocalizationModel
from lab.preprocess import enumerate_all_uuids, preprocess
from utils.utils import enumerate_all_data_path, load_data, process_label


def main():
    data_paths = enumerate_all_data_path()
    label_scan_result_list = [load_data(data_path) for data_path in data_paths]

    x = []
    y = []

    whole_scan_result_list = []
    for _, scan_result_list in label_scan_result_list:
        whole_scan_result_list.extend(scan_result_list)

    uuid_list = enumerate_all_uuids(whole_scan_result_list)

    for label, scan_result_list in label_scan_result_list:
        fingerprints = preprocess(scan_result_list, uuid_list)

        y.append(process_label(label, len(fingerprints)))
        x.append(fingerprints)

    x = np.vstack(x)
    y = np.vstack(y)

    # train with (x, y)
    model = LocalizationModel()
    model.train(x, y)
    model.save_model("./model.dat")

    with open("uuid_list.pkl", "wb") as f:
        pickle.dump(uuid_list, f)


if __name__ == "__main__":
    main()
