import boto3
import datetime

class CWManager:

    def __init__(self, namespace="Sys"):
        self.cw = boto3.client('cloudwatch')
        self.namespace = namespace

    def formater(self, name, value):
        return {
            'MetricName': str(name),
            'Dimensions': [
                {
                    'Name': str(name),
                    'Value': str(value)
                }
            ],
            'Timestamp': datetime.datetime.now(),
            'StatisticValues': {
                'Maximum':     float(value),
				'Minimum':     float(value),
				'SampleCount': float(1.0),
				'Sum':         float(value),
            },
            'Unit': 'Seconds',
            'StorageResolution': 60
        }

    def send_metrics(self, array_data):
        self.cw.put_metric_data(Namespace=self.namespace, MetricData=array_data)

    def put_metric_alarm(self):
        print("TODO")
