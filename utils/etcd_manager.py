import sys
from utils.shell import ShellManager
from utils.ec2_manager import ClusterEC2Manager

class ETCDManager:

    def __init__(self, cluster):
        self.cluster = cluster
        self.shell = ShellManager()
        self.cec2_manager = ClusterEC2Manager(cluster)

    def get_instance_metadata(self):
        etcd_instances = self.cec2_manager.get_etcd_status()
        for instance in etcd_instances:
            print(instance.private_ip_address)
            # print('-s https://{0}:2379/health --cert /etc/etcd/pki/server.crt --key /etc/etcd/pki/server.key --cacert /etc/etcd/pki/ca.crt'.format(instance.private_ip_address))

    # get instances from ASG
    # use etcdctl get status
    # update cluster status

    def get_cluster_status(self):
        return {
            "etcd_instances": [
                { "instance_ip": "192.168.50.133", "health": True, "leader": True },
                { "instance_ip": "192.168.67.230", "health": True },
                { "instance_ip": "192.168.95.159", "health": False }
            ],
            "etcd_cluster_health": 0,
            "etcd_cluster_healthy_percenage": 0.66
        }


# etcd_manager = ETCDManager({
#     "clusterId": "dylan.k8s.platform.myobdev.com",
#     "clusterName": "dylan"
# })
#
# etcd_manager.get_instance_metadata()
