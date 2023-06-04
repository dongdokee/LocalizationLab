from lib.bt_scan import scan, kill, ScanResult 
import asyncio 
from typing import List 
import argparse 
from lab.preprocess import preprocess
import pickle 
import numpy as np 
from lab.model import LocalizationModel
# from queue import Queue 


def perform_localization(fingerprint: np.ndarray, model):
    return model.predict(fingerprint)


async def on_receive_scan_data(scan_result: ScanResult, uuid_list: List[str], model):
    fingerprint = preprocess([scan_result], uuid_list)

    y = perform_localization(fingerprint, model) 
    print(y) 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    prog="train data sampler",
    description="트레이닝 데이터를 수집하는 프로그램입니다.") 
    
    #parser.add_argument('-t', '--time', type=float, default=10.0, help="측정 시간을 초 단위로 입력하세요. (-t 3이면 3초동안 측정)", required=True)
    parser.add_argument('-i', '--interval', type=float, help="스캔 결과를 보고받을 주기를 초 단위로 입력하세요.", required=True)

    args = parser.parse_args() 

    loop = asyncio.get_event_loop() 

    with open('uuid_list.pkl', 'rb') as f:
        uuid_list = pickle.load(f)

    model = LocalizationModel.load_model('model.dat')

    loop.run_until_complete(scan(args.interval, on_receive_scan_data, uuid_list=uuid_list, model=model))
#    await scan_task 
#    pass 