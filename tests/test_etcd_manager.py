import unittest
from unittest.mock import MagicMock
from utils.etcd_manager import ETCDManager


class TestETCDManager(unittest.TestCase):

    def test_tt(self):
        etcd_manager = ETCDManager({
            "clusterId": "dylan.k8s.platform.myobdev.com",
            "clusterName": "dylan"
        })
        data = etcd_manager.get_cluster_status()
        self.assertEqual(len(data['etcd_instances']), 3)
