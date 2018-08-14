import subprocess

class ShellManager():

    def curl(self, args):
        cmd = "curl {}".format(args)
        return self.exec_sh(cmd)


    def aws(self, args):
        cmd = "aws {}".format(args)
        return self.exec_sh(cmd)

    def etcdctl(self, args):

        def get_etcd_cert_flags():
            return "--cert /etc/etcd/pki/server.pem --key /etc/etcd/pki/server-key.pem --cacert /etc/etcd/pki/ca.crt"

        cmd = "export ETCDCTL_API=3; etcdctl {etcd_opts} {args}".format(etcd_opts=get_etcd_cert_flags(), args=args)
        return self.exec_sh(cmd)


    def exec_sh(self, cmd):
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return output.strip()
