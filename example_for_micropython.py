import utime
import network
import urequests
import ntptime

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

prometheus = PrometheusRemoteWritePayload()
prometheus.add_data(
    "test_test", {"instance": "test_micropython"}, 987.654, int(utime.time() * 1000)
)

prometheus_remote_write_endpoint = "https://prometheus-remote-write-endpoint"
prometheus_remote_write_endpoint_basic_auth = "MD5 hash of user:password"
urequests.post(
    prometheus_remote_write_endpoint,
    headers={"Authorization": f"Basic {prometheus_remote_write_endpoint_basic_auth}"},
    data=prometheus.get_payload(),
)
