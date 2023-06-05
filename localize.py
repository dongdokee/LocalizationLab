import argparse
import asyncio
import os
import pickle
import signal
import sys
import threading
from typing import List

import numpy as np
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

import y_def
from lab.model import LocalizationModel
from lab.preprocess import preprocess
from lib.bt_scan import ScanResult, kill, scan

app = Flask(__name__)

current_prediction = {"ydef": y_def.y_def, "y": None}

with open("viewer.html", "r") as f:
    viewer_html = f.read()


@app.route("/", methods=["GET"])
def index():
    return viewer_html


@app.route("/y", methods=["GET"])
def get_ydef():
    return current_prediction


def perform_localization(fingerprint: np.ndarray, model):
    return model.predict(fingerprint)


async def on_receive_scan_data(scan_result: ScanResult, uuid_list: List[str], model):
    # fingerprint = preprocess([scan_result], uuid_list)

    # y = perform_localization(fingerprint, model)
    import random

    print("on_receive_scan_data", flush=True)

    y = y_def.y_def[list(y_def.y_def.keys())[random.randint(0, 3)]]

    current_prediction["y"] = y


def real_main(args, event):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    with open("uuid_list.pkl", "rb") as f:
        uuid_list = pickle.load(f)

    model = LocalizationModel.load_model("model.dat")

    async def kill_check():
        while True:
            await asyncio.sleep(0.5)
            if event.is_set():
                loop.stop()

    loop.create_task(kill_check())

    loop.run_until_complete(
        scan(args.interval, on_receive_scan_data, uuid_list=uuid_list, model=model)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="train data sampler", description="트레이닝 데이터를 수집하는 프로그램입니다."
    )

    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        help="스캔 결과를 보고받을 주기를 초 단위로 입력하세요.",
        required=True,
    )

    args = parser.parse_args()

    event = threading.Event()

    def signal_handler(sig, frame):
        event.set()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    threading.Thread(target=real_main, args=(args, event)).start()

    app.run(host="localhost", port=5001)
