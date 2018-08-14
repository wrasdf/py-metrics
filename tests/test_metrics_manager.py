import unittest
from unittest.mock import MagicMock
from utils.metrics_manager import MetricsManager

class TestMetricsManager(unittest.TestCase):

    def test_get_etcd_metrics_data(self):
        metrics_manager = MetricsManager({
            "clusterId": "dylan.k8s.platform.myobdev.com",
            "clusterName": "dylan"
        })
        metrics_manager.etcd_manager.get_cluster_status = MagicMock(return_value={
            "etcd_instances": [
                { "instance_ip": "192.168.50.133", "health": True, "leader": True },
                { "instance_ip": "192.168.67.230", "health": True },
                { "instance_ip": "192.168.95.159", "health": False }
            ],
            "etcd_cluster_health": 0,
            "etcd_cluster_healthy_percenage": 0.66
        })
        data = metrics_manager.get_formated_cluster_metrics_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['MetricName'], 'etcd_cluster_health')
        self.assertEqual(data[0]['StatisticValues']['Maximum'], 0.0)
        self.assertEqual(data[1]['MetricName'], 'etcd_cluster_healthy_percenage')
        self.assertEqual(data[1]['StatisticValues']['Maximum'], 0.66)
