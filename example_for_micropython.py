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
