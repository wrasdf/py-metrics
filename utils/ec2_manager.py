import boto3
import datetime

class ClusterEC2Manager:

    def __init__(self, cluster):
        self.cluster = cluster
        self.region = 'ap-southeast-2'
        self.ec2 = boto3.resource('ec2', region_name=self.region)
        self.now = datetime.datetime.now()

    def get_etcd_status(self):
        nodes = self.ec2.instances.filter(Filters=[
            {'Name': 'tag:KubernetesCluster', 'Values': [self.cluster['clusterId']]},
            {'Name': 'tag:aws:cloudformation:stack-name', 'Values': ['{0}-etcd'.format(self.cluster['clusterName'])]}
        ])
        return self.return_valid_instances(nodes)

    def get_nodes_status(self):
        nodes = self.ec2.instances.filter(Filters=[
            {'Name': 'tag:KubernetesCluster', 'Values': [self.cluster['clusterId']]},
            {'Name': 'tag:aws:cloudformation:stack-name', 'Values': ['{0}-nodes'.format(self.cluster['clusterName'])]}
        ])
        return self.return_valid_instances(nodes)

    def get_masters_status(self):
        nodes = self.ec2.instances.filter(Filters=[
            {'Name': 'tag:KubernetesCluster', 'Values': [self.cluster['clusterId']]},
            {'Name': 'tag:aws:cloudformation:stack-name', 'Values': ['{0}-masters'.format(self.cluster['clusterName'])]}
        ])
        return self.return_valid_instances(nodes)

    def return_valid_instances(self, instances):
        results = []
        for instance in instances:
            if instance.private_ip_address != None:
                results.append(instance)

        return results

    def prometheus_logger(self, prefix ,instances):
        for instance in instances:
            print('{0},Cluster={1},Address={2} health={3} {4}000000000'.format(prefix, self.cluster['clusterName'], instance.private_ip_address, ("0", "1")[instance.state['Name'] == 'running'] ,self.now.microsecond))


# cec2_manager = ClusterEC2Manager({
#     "clusterId": "dylan.k8s.platform.myobdev.com",
#     "clusterName": "dylan"
# })
# # cec2_manager.get_nodes_status()
# # cec2_manager.get_masters_status()
# # print(cec2_manager.get_etcd_status())
#
# for instance in cec2_manager.get_etcd_status():
#     print(instance.private_ip_address)
