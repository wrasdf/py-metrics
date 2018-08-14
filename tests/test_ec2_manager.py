import unittest
import io
import sys

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
        self.assertEqual(data[1].private_ip_address, "192.169.12.14")

    def test_prometheus_logger(self):
        cec2_manager = ClusterEC2Manager({
            "clusterId": "dylan.k8s.platform.myobdev.com",
            "clusterName": "dylan"
        })
        instances = cec2_manager.return_valid_instances([
            AttributeDict({"private_ip_address": "192.169.12.12", "state": {
                "Name": "running"
            }}),
            AttributeDict({"private_ip_address": None}),
            AttributeDict({"private_ip_address": "192.169.12.14", "state": {
                "Name": "installing"
            }}),
            AttributeDict({"private_ip_address": None})
        ])

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        cec2_manager.prometheus_logger("dylan", instances)
        sys.stdout = sys.__stdout__
        sys_outs = capturedOutput.getvalue().splitlines()
        self.assertEqual(len(sys_outs), 2)
        self.assertEqual(True, 'dylan' in sys_outs[0])
        self.assertEqual(True, 'health=1' in sys_outs[0])
        self.assertEqual(True, '192.169.12.12' in sys_outs[0])
        self.assertEqual(True, 'health=0' in sys_outs[1])
        self.assertEqual(True, '192.169.12.14' in sys_outs[1])
