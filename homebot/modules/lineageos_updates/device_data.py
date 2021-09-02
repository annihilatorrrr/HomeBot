import requests
import yaml

DEVICES_DATA = "https://raw.githubusercontent.com/LineageOS/lineage_wiki/master/_data/devices/{device}.yml"

class DeviceData:
    def __init__(self, codename: str):
        """Get device data from LineageOS wiki data."""
        self.codename = codename
        self.yaml_url = DEVICES_DATA.format(device=self.codename)
        self.response = requests.get(url=self.yaml_url).text
        self.yaml = yaml.safe_load(self.response)

        self.name = self.yaml["name"]
