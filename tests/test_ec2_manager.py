import unittest
from unittest.mock import MagicMock
from utils.ec2_manager import ClusterEC2Manager

class AttributeDict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(name)

class TestMetricsManager(unittest.TestCase):
    def test_return_valid_instances(self):
        cec2_manager = ClusterEC2Manager({
            "clusterId": "dylan.k8s.platform.myobdev.com",
            "clusterName": "dylan"
        })
        data = cec2_manager.return_valid_instances([
            AttributeDict({"private_ip_address": "192.169.12.12"}),
            AttributeDict({"private_ip_address": None}),
            AttributeDict({"private_ip_address": "192.169.12.14"}),
            AttributeDict({"private_ip_address": None})
        ])
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].private_ip_address, "192.169.12.12")
