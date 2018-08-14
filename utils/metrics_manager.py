# -*- coding: utf-8 -*-
import os
from utils.cw_manager import CWManager
from utils.etcd_manager import ETCDManager


os.environ.setdefault('AWS_DEFAULT_REGION', 'ap-southeast-2')

class MetricsManager:

    def __init__(self, cluster):
        self.cluster = cluster
        self.cw_manager = CWManager(namespace='PY_METRICS_DEMO/{0}'.format(self.cluster['clusterName']))
        self.etcd_manager = ETCDManager(self.cluster)

    def get_formated_cluster_metrics_data(self):
        data = []
        cluster_status = self.etcd_manager.get_cluster_status()
        for metric in cluster_status:
            if metric != 'etcd_instances':
                data.append(
                    self.cw_manager.formater(metric, cluster_status[metric])
                )
        return data

    def send_cluster_metrics(self):
        self.cw_manager.send_metrics(
            self.get_formated_cluster_metrics_data()
        )

# if __name__ == '__main__':
#     m = MetricsManager()
#     m.send_cluster_metrics()
