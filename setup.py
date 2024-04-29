from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="prometheus_remote_write_payload",
    version="1.0.0",
    description="Utility to generate Prometheus remote-write payloads",
    long_description=readme,
    author="tama@ttk1",
    author_email="tama@ttk1.net",
    url="https://github.com/ttk1/prometheus_remote_write_payload",
    license=license,
    packages=find_packages(exclude=("test",)),
)
