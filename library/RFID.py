import datetime
import serial
from collections import deque


class FixedLengthQueue:
    def __init__(self, max_length):
        self.max_length = max_length
        self.queue = deque(maxlen=max_length)

    def add(self, value):
        if len(self.queue) == self.max_length:
            self.queue.popleft()
        self.queue.append(value)

    def __str__(self):
        return str(list(self.queue))

# def get_rfid_reader(port):
#     baud_rate = 115200
#     serial_uri = f"alt://{port}?class=VTIMESerial"
#     reader = serial.serial_for_url(serial_uri, baudrate=baud_rate, timeout=0.1)
#     return reader

def get_rfid_reader(port):
    baud_rate = 115200
    reader = serial.Serial(port, baudrate=baud_rate, timeout=0.1)
    return reader


def columns():
    columns = [
    "tm_detection",
    "id_tag",
    "cat_sitecode",
    "cat_antenna",
    "tm_duration",
    "n_detections",
    "val_latitude",
    "val_longitude",
    "cat_detection_type",
    "id_tag_class",
    "id_tag_type",
    "id_time_reference",
    "val_effective_amps",
    "n_connected_satellites",
    "val_horizontal_accuracy",
    "txt_tag_signal_strength",
    "val_listen_amps",
    "val_antenna_voltage",
    "val_antenna_amperage",
    "val_noise"]
    return columns


def convert_stream_to_records(stream):
    if not stream: return []
    records = []
    cols = columns()
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    for read in stream:
        try:
            read = read.decode('utf-8', errors='replace')
            read = read.rstrip()
            read = read.split(",")
        except:
            print(read)
        if len(cols) == len(read):
            record = {k: v.strip() for k, v in zip(cols, read)}
            record.update({"device_timestamp": timestamp})
            records.append(record)
    return records


def get_antenna_events(records):
    if len(records) == 0: return [], [], []
    antennas = []
    events = []
    box_times = []
    for record in records:
        antenna = record["cat_antenna"]
        event = record["cat_detection_type"]
        box_time = record["tm_detection"]
        antennas.append(antenna)
        events.append(event)
        box_times.append(box_time)
    return antennas, events, box_times


def process_antenna_events(antennas, events):
    tags = []
    for antenna, event in zip(antennas, events):
        if event == 'I': tag = 'arrived ' + antenna[1:]
        if event == 'S': tag = 'left ' + antenna[1:]
        tags.append(tag)
    return tags