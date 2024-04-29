import struct


def int_to_varint(v: int) -> bytes:
    b = b""
    while True:
        t = v & 0b0111_1111
        v >>= 7
        if v == 0 or (v == -1 and t & 0b0100_0000 > 0):
            b += t.to_bytes(1, "little")
            break
        b += (t | 0b1000_0000).to_bytes(1, "little")
    return b


def no_compress_snappy(data: bytes):
    snappy = int_to_varint(len(data))
    for chunk in [data[i : i + 60] for i in range(0, len(data), 60)]:
        chunk_len = len(chunk)
        snappy += ((chunk_len - 1) << 2).to_bytes(1, "little")
        snappy += chunk
    return snappy


def data_with_length(data: bytes) -> bytes:
    length = len(data)
    return int_to_varint(length) + data


class Label:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class Sample:
    def __init__(self, value: float, timestamp: int):
        self.value = value
        self.timestamp = timestamp


class TimeSeries:
    def __init__(self):
        self.labels: list[Label] = []
        self.samples: list[Sample] = []

    def add_label(self, label: Label):
        self.labels.append(label)

    def add_sample(self, sample: Sample):
        self.samples.append(sample)


class PrometheusRemoteWritePayload:
    def __init__(self):
        self.timeseries: list[TimeSeries] = []

    def add_timeseries(self, timeseries: TimeSeries):
        self.timeseries.append(timeseries)

    def add_data(self, name: str, labels: dict[str, str], data: float, timestamp: int):
        timeseries = TimeSeries()
        timeseries.add_label(Label("__name__", name))
        for key in labels:
            timeseries.add_label(Label(key, labels[key]))
        timeseries.add_sample(Sample(data, timestamp))
        self.add_timeseries(timeseries)

    def get_payload(self) -> bytes:
        payload = b""
        for timeseries in self.timeseries:
            timeseries_data = b""
            for label in timeseries.labels:
                label_data = (1 << 3 | 2).to_bytes(1, "little")
                label_data += data_with_length(label.name.encode("utf-8"))
                label_data += (2 << 3 | 2).to_bytes(1, "little")
                label_data += data_with_length(label.value.encode("utf-8"))
                timeseries_data += (1 << 3 | 2).to_bytes(1, "little")
                timeseries_data += data_with_length(label_data)
            for sample in timeseries.samples:
                sample_data = (1 << 3 | 1).to_bytes(1, "little")
                sample_data += struct.pack("<d", sample.value)
                sample_data += (2 << 3 | 0).to_bytes(1, "little")
                sample_data += int_to_varint(sample.timestamp)
                timeseries_data += (2 << 3 | 2).to_bytes(1, "little")
                timeseries_data += data_with_length(sample_data)
            payload += (1 << 3 | 2).to_bytes(1, "little")
            payload += data_with_length(timeseries_data)
        return no_compress_snappy(payload)
