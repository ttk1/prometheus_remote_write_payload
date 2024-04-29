# Prometheus remote-write payload

This utility generates payloads for [Prometheus remote-write](https://prometheus.io/docs/concepts/remote_write_spec/).

## Requirements

Python 3 or MicroPython

## Installation (Python 3)

```sh
pip install git+https://github.com/ttk1/prometheus_remote_write_payload.git
```

## Example

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
python example.py | curl -u "${user}:${password}" --data-binary @- https://${prometheus-remote-write-endpoint}
```

### MicroPython

TODO
