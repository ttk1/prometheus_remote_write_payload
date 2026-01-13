# Prometheus Remote-Write Payload Generator

This utility generates payloads for [Prometheus remote-write v1.0](https://prometheus.io/docs/concepts/remote_write_spec/), compatible with Python 3 and MicroPython environments.

## Requirements

* Python 3 or MicroPython

## Installation

### Python 3

```sh
pip install git+https://github.com/ttk1/prometheus_remote_write_payload.git
```

### MicroPython (mpremote)

```sh
mpremote mip install github:ttk1/prometheus_remote_write_payload
```

### MicroPython (mip)

```py
import mip
mip.install("github:ttk1/prometheus_remote_write_payload")
```

## Example Usage

### Python 3

```py
import sys
import time

from prometheus_remote_write_payload import PrometheusRemoteWritePayload

prometheus = PrometheusRemoteWritePayload()
prometheus.add_data(
    "test_test", {"instance": "test_instance"}, 123.456, int(time.time() * 1000)
)
sys.stdout.buffer.write(prometheus.get_payload())
```

```sh
python example.py | curl -u "${user}:${password}" \
  -H 'Content-Encoding:snappy' \
  -H 'Content-Type:application/x-protobuf' \
  -H 'X-Prometheus-Remote-Write-Version:0.1.0' \
  --data-binary @- https://${prometheus-remote-write-endpoint}
```

### MicroPython

```py
import network
import ntptime
import urequests
import utime

from prometheus_remote_write_payload import PrometheusRemoteWritePayload

ssid = "ssid"
password = "password for ssid"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
utime.sleep(5)
if wlan.status() != 3:
    raise Exception("network connection failed")
ntptime.settime()

headers = {
    "Content-Encoding": "snappy",
    "Content-Type": "application/x-protobuf",
    "User-Agent": "MicroPython",
    "X-Prometheus-Remote-Write-Version": "0.1.0",
}

prometheus = PrometheusRemoteWritePayload()
prometheus.add_data(
    "test_test", {"instance": "test_micropython"}, 987.654, int(utime.time() * 1000)
)

prometheus_remote_write_endpoint = "https://prometheus-remote-write-endpoint"
prometheus_remote_write_endpoint_basic_auth = ("user", "password")
urequests.post(
    prometheus_remote_write_endpoint,
    headers=headers,
    data=prometheus.get_payload(),
    auth=prometheus_remote_write_endpoint_basic_auth,
)
```
