import boto3


class AutoscalingManager:
    def __init__(self):
        self.region = 'ap-southeast-2'
        self.ac = boto3.client('autoscaling', region_name=self.region)

    def get_instances_status(self, name):
        return self.ac.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                name
            ]
        )

#
# ac_manager = AutoscalingManager()
# print(ac_manager.get_instances_status('etcd.europa-stg.jupiter.myobdev.com')['AutoScalingGroups'][0]['Instances'])
