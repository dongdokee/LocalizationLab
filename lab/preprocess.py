import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from typing import List

import numpy as np

from lib.bt_scan import ScanResult


def enumerate_all_uuids(scan_result_list: List[ScanResult]) -> List[str]:
    result = set()

    for scan_result in scan_result_list:
        for scan_result_entry in scan_result.scan_result_entries:
            result.add(scan_result_entry.uuid)

    return list(result)


def preprocess(scan_result_list: List[ScanResult], uuid_list: List[str]) -> np.ndarray:
    """
    1. 결측치 None 값으로 설정
    2. 여러번 관측된 beacon에 대해서는 RSSI 값을 평균
    """
    if uuid_list is None:
        uuid_list = enumerate_all_uuids(scan_result_list)

    num_entries = len(scan_result_list)
    num_beacons = len(uuid_list)

    result = np.zeros((num_entries, num_beacons))

    for i, scan_result in enumerate(scan_result_list):
        for j, uuid in enumerate(uuid_list):
            # find scan_result_entry with uuid
            acc = 0
            num_hits = 0
            for scan_result_entry in scan_result.scan_result_entries:
                if uuid == scan_result_entry.uuid:
                    acc = scan_result_entry.rssi
                    num_hits += 1

            if num_hits > 0:
                # observed
                mean_rssi = acc / num_hits
                result[i, j] = mean_rssi
            else:
                # missing
                result[i, j] = None

    return result


import pickle

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "..", "bt_3.pkl")
    with open(data_path, "rb") as f:
        scan_result_list = pickle.load(f)

    preprocess(scan_result_list)
