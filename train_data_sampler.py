
import argparse 
import pandas as pd 
from lib.bt_scan import scan, kill, ScanResult
import asyncio 
import pickle 
from typing import List, Awaitable


async def on_receive_callback(scan_result: ScanResult, result_list: List[ScanResult]) -> Awaitable[None]:
    result_list.append(scan_result)
    print(scan_result)


def main():
    parser = argparse.ArgumentParser(
        prog="train data sampler",
        description="트레이닝 데이터를 수집하는 프로그램입니다.") 
    
    parser.add_argument('-t', '--time', type=float, default=10.0, help="측정 시간을 초 단위로 입력하세요. (-t 3이면 3초동안 측정)", required=True)
    parser.add_argument('-y', '--label', type=str, help="위치 라벨, 좌표를 x,y의 형태로 입력하거나 또는 정수 형태의 카테고리 라벨을 입력하세요. (-y 1.5,2.5이면 (1.5,2.5)의 위치에서 데이터를 측정, -y 1이면 1번 위치에서 측정)", required=True)
    parser.add_argument('-i', '--interval', type=float, help="스캔 결과를 보고받을 주기를 초 단위로 입력하세요.", required=True)

    args = parser.parse_args() 

    loop = asyncio.get_event_loop()

    result_list = [] 
    label = args.label 
    loop.create_task(scan(args.interval, on_receive_callback, result_list=result_list))
    loop.run_until_complete(kill(args.time))
    
    with open(f'data/bt_{label}.pkl', 'wb') as f:
        pickle.dump((label, result_list), f)


if __name__ == "__main__":
    main() 
