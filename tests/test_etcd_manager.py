import unittest
from unittest.mock import MagicMock
from utils.etcd_manager import ETCDManager


class TestETCDManager(unittest.TestCase):

    def test_healthy_cluster_with_all_healthy_nodes(self):
        etcd_manager = ETCDManager({
            "clusterId": "dylan.k8s.platform.myobdev.com",
            "clusterName": "dylan"
        })
        etcd_manager.get_cluster_healthy_results = MagicMock(return_value="""
member 25de9ae4efe60f3 is healthy: got healthy result from https://192.168.74.205:2379
member 2a3962c75e3090e9 is healthy: got healthy result from https://192.168.59.98:2379
member 90c6a5999b3154d3 is healthy: got healthy result from https://192.168.95.40:2379
cluster is healthy
        """)

        etcd_manager.get_etcd_endpoints = MagicMock(return_value=[
            "https://192.168.95.40:2379/",
            "https://192.168.74.205:2379/",
            "https://192.168.59.98:2379/"
        ])

        etcd_manager.get_cluster_nodes_resutls = MagicMock(return_value=[
            {"Endpoint":"https://192.168.95.40:2379/","Status":{"header":{"cluster_id":8428508670516781110,"member_id":10432207666002613459,"revision":76089,"raft_term":766},"version":"3.2.18","dbSize":3764224,"leader":170549295768822003,"raftIndex":91245,"raftTerm":766}},
            {"Endpoint":"https://192.168.74.205:2379/","Status":{"header":{"cluster_id":8428508670516781110,"member_id":170549295768822003,"revision":76089,"raft_term":766},"version":"3.2.18","dbSize":3772416,"leader":170549295768822003,"raftIndex":91245,"raftTerm":766}},
            {"Endpoint":"https://192.168.59.98:2379/","Status":{"header":{"cluster_id":8428508670516781110,"member_id":3042571631683735785,"revision":76089,"raft_term":766},"version":"3.2.18","dbSize":3936256,"leader":170549295768822003,"raftIndex":91245,"raftTerm":766}}
        ])

        result = etcd_manager.update_cluster_status()
        self.assertEqual(result["etcd_cluster_health"], "1")
        self.assertEqual(len(result["etcd_instances"]), 3)
        self.assertEqual(result["etcd_instances"][0]["endpoint"], "https://192.168.95.40:2379/")
        self.assertEqual(result["etcd_instances"][0]["leader"], False)
        self.assertEqual(result["etcd_instances"][0]["health"], True)
        self.assertEqual(result["etcd_instances"][1]["leader"], True)


    def test_healthy_cluster_with_some_healthy_nodes(self):
        etcd_manager = ETCDManager({
            "clusterId": "dylan.k8s.platform.myobdev.com",
            "clusterName": "dylan"
        })

        etcd_manager.get_cluster_healthy_results = MagicMock(return_value="""
member 25de9ae4efe60f3 is healthy: got healthy result from https://192.168.74.205:2379
failed to check the health of member 2a3962c75e3090e9 on https://192.168.59.98:2379: Get https://192.168.59.98:2379/health: dial tcp 192.168.59.98:2379: getsockopt: connection refused
member 2a3962c75e3090e9 is unreachable: [https://192.168.59.98:2379] are all unreachable
member 90c6a5999b3154d3 is healthy: got healthy result from https://192.168.95.40:2379
cluster is healthy
        """)

        etcd_manager.get_etcd_endpoints = MagicMock(return_value=[
            "https://192.168.95.40:2379/",
            "https://192.168.74.205:2379/",
            "https://192.168.59.98:2379/"
        ])

        etcd_manager.get_cluster_nodes_resutls = MagicMock(return_value=[
            {"Endpoint":"https://192.168.95.40:2379/","Status":{"header":{"cluster_id":8428508670516781110,"member_id":10432207666002613459,"revision":79450,"raft_term":766},"version":"3.2.18","dbSize":3764224,"leader":170549295768822003,"raftIndex":95137,"raftTerm":766}},
            {"Endpoint":"https://192.168.74.205:2379/","Status":{"header":{"cluster_id":8428508670516781110,"member_id":170549295768822003,"revision":79450,"raft_term":766},"version":"3.2.18","dbSize":3772416,"leader":170549295768822003,"raftIndex":95137,"raftTerm":766}}
        ])

        result = etcd_manager.update_cluster_status()
        self.assertEqual(result["etcd_cluster_health"], "1")
#
#     def test_un_healthy_etcd_cluster(self):
#         etcd_manager = ETCDManager({
#             "clusterId": "dylan.k8s.platform.myobdev.com",
#             "clusterName": "dylan"
#         })
#         etcd_manager.get_cluster_healthy_results = MagicMock(return_value="""
# member 25de9ae4efe60f3 is unhealthy: got unhealthy result from https://192.168.74.205:2379
# failed to check the health of member 2a3962c75e3090e9 on https://192.168.59.98:2379: Get https://192.168.59.98:2379/health: dial tcp 192.168.59.98:2379: getsockopt: connection refused
# member 2a3962c75e3090e9 is unreachable: [https://192.168.59.98:2379] are all unreachable
# failed to check the health of member 90c6a5999b3154d3 on https://192.168.95.40:2379: Get https://192.168.95.40:2379/health: dial tcp 192.168.95.40:2379: getsockopt: connection refused
# member 90c6a5999b3154d3 is unreachable: [https://192.168.95.40:2379] are all unreachable
# cluster is unhealthy
#         """)
#         result = etcd_manager.update_cluster_status()
#         self.assertEqual(result["etcd_cluster_health"], "0")
