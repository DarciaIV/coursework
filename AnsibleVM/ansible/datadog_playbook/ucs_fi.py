import subprocess
from checks import AgentCheck


class UCSFiCheck(AgentCheck):
    def check(self, instance):
        if 'ip_address' not in instance:
            self.log.info("Skipping instance, no ip_address found.")
            return

        p = subprocess.Popen(
            ["/opt/datadog-agent/embedded/bin/python", 
            "ucs-fault.py", 
            instance['ip_address'], 
            instance['username'], 
            instance['password']],
            stdout=subprocess.PIPE,
        )
        output, err = p.communicate()
        p_status = p.returncode
	self.service_check(
            check_name='ucs fi status',
            status=p_status,
            tags=instance['tags'],
            hostname=instance['ip_address'],
            message=output
        )


if __name__ == '__main__':
    check, instances = UCSFiCheck.from_yaml('/etc/dd-agent/conf.d/ucs_fi.yaml')
    for instance in instances:
        print "\nRunning the check against ip: %s" % (instance['ip_address'])
        check.check(instance)