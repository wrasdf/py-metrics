import subprocess

class ShellManager():

    def curl(self, args):
        cmd = "curl {}".format(args)
        return self.exec_sh(cmd)

    def aws(self, args):
        cmd = "aws {}".format(args)
        return self.exec_sh(cmd)

    def exec_sh(self, cmd):
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return output.strip()
