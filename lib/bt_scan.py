# Bluetooth Scan Libarary

import asyncio
import time
from datetime import datetime
from typing import List, Optional

from bleak import BleakScanner


class ScanResultEntry:
    uuid: str
    rssi: float

    def __init__(self, uuid: str, rssi: float) -> None:
        self.uuid = uuid
        self.rssi = rssi

    def __repr__(self) -> str:
        return f"ScanResult(uuid={self.uuid}, rssi={self.rssi})"


class ScanResult:
    t: float
    scan_result_entries: List[ScanResultEntry]

    def __init__(
        self, t: float, scan_result_entries: Optional[List[ScanResultEntry]] = None
    ):
        self.t = t
        self.scan_result_entries = scan_result_entries

    def add_scan_result_entry(self, scan_result_entry: ScanResultEntry) -> None:
        self.scan_result_entries.append(scan_result_entry)

    def __repr__(self) -> str:
        return (
            f"ScanResult(t: {self.t}, scan_result_entries: {self.scan_result_entries})"
        )


stop_event = asyncio.Event()
queue = asyncio.Queue()


async def scan(report_interval, processed_callback, *args, **kwargs):
    async def callback(device, advertisement_data):
        rssi = advertisement_data.rssi

        if (
            hasattr(advertisement_data, "service_data")
            and advertisement_data.service_data
        ):
            for (
                service_uuid,
                service_payload,
            ) in advertisement_data.service_data.items():
                company_code = service_uuid.split("-")[0][-4:]

                # fe9a: ESTIMOTE
                # refer https://btprodspecificationrefs.blob.core.windows.net/assigned-numbers/Assigned%20Number%20Types/Assigned_Numbers.pdf
                if company_code == "fe9a":
                    estimote_payload = service_payload.hex()

                    if estimote_payload.startswith("00"):
                        estimote_uuid = estimote_payload[2:-6]
                        timestamp = time.time()

                        # For DEBUG
                        print(timestamp, estimote_uuid, rssi)

                        await queue.put((timestamp, estimote_uuid, rssi))

    async with BleakScanner(callback) as scanner:
        process_task = asyncio.create_task(
            process(report_interval, processed_callback, *args, **kwargs)
        )

        await process_task
        await stop_event.wait()


async def process(report_interval, processed_callback, *args, **kwargs):
    bin_start_time = None
    process_queue = []
    while True:
        data = await queue.get()

        if not bin_start_time:
            bin_start_time = data[0]

            process_queue.append(data)
            continue

        if data[0] - bin_start_time > report_interval:
            # ScanResult 생성
            scan_result_entries = [
                ScanResultEntry(uuid, rssi) for _, uuid, rssi in process_queue
            ]
            scan_result = ScanResult(bin_start_time, scan_result_entries)

            await processed_callback(scan_result, *args, **kwargs)
            process_queue.clear()
            process_queue.append(data)
            bin_start_time += report_interval
        else:
            process_queue.append(data)


async def kill(delay):
    await asyncio.sleep(delay)
    stop_event.set()


if __name__ == "__main__":

    async def callback(scan_result: ScanResult):
        print(scan_result)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(scan(2, callback))
