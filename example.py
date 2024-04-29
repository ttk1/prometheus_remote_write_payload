import sys
import time
from prometheus_remote_write_payload import PrometheusRemoteWritePayload

prometheus = PrometheusRemoteWritePayload()
prometheus.add_data(
    "test_test", {"instance": "test_instance"}, 987.654, int(time.time() * 1000)
)
sys.stdout.buffer.write(prometheus.get_payload())
