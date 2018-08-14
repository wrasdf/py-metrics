import sys
import json
from utils.shell import ShellManager
from utils.ec2_manager import ClusterEC2Manager

# from shell import ShellManager
# from ec2_manager import ClusterEC2Manager


class ETCDManager:

    def __init__(self, cluster):
        self.cluster = cluster
        self.etcd_certs_v3 = "--cert /etc/etcd/pki/server.crt --key /etc/etcd/pki/server.key --cacert /etc/etcd/pki/ca.crt"
        self.etcd_certs_v2 = "--cert-file /etc/etcd/pki/server.crt --key-file /etc/etcd/pki/server.key --ca-file /etc/etcd/pki/ca.crt"
        self.shell = ShellManager()
        self.cec2_manager = ClusterEC2Manager(cluster)

    def get_etcd_endpoints(self):
        etcd_instances = self.cec2_manager.get_etcd_status()
        endpoints = []
        for instance in etcd_instances:
            endpoints.append("https://{0}:2379/".format(instance.private_ip_address))
        return endpoints

    def get_cluster_healthy_results(self):
        return self.shell.exec_sh("export ETCDCTL_API=2; etcdctl {0} --endpoints {1} cluster-health".format(
            self.etcd_certs,
            ','.join(self.get_etcd_endpoints())
        ))

    def get_cluster_nodes_resutls(self):
        return self.shell.exec_sh("export ETCDCTL_API=3; etcdctl {0} --endpoints {1} endpoint status -w json".format(
            self.etcd_certs,
            ','.join(self.get_etcd_endpoints())
        ))

    def update_cluster_status(self):

        cluster_healthy_results = self.get_cluster_healthy_results()
        etcd_endpoints = self.get_etcd_endpoints()
        nodes_results = self.get_cluster_nodes_resutls()

        result = {}
        result["etcd_cluster_health"] = ("0", "1")["cluster is healthy" in str(cluster_healthy_results)]
        result["etcd_instances"] = []
        for endpoint in etcd_endpoints:
            result["etcd_instances"].append(
                {"endpoint": endpoint, "health": False, "leader": False}
            )

        for node in nodes_results:
            for instance in result["etcd_instances"]:
                if instance["endpoint"] == node["Endpoint"]:
                    instance["health"] = True
                    if node["Status"]["header"]["member_id"] == node["Status"]["leader"]:
                        instance["leader"] = True

        return result

    # def get_cluster_status(self):
    #     return {
    #         "etcd_instances": [
    #             { "instance_ip": "192.168.50.133", "health": True, "leader": True },
    #             { "instance_ip": "192.168.67.230", "health": True },
    #             { "instance_ip": "192.168.95.159", "health": False }
    #         ],
    #         "etcd_cluster_health": 0,
    #         "etcd_cluster_healthy_percenage": 0.66
    #     }

#
# etcd_manager = ETCDManager({
#     "clusterId": "dylan.k8s.platform.myobdev.com",
#     "clusterName": "dylan"
# })
# print(etcd_manager.get_cluster_nodes_resutls())
