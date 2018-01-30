import sys
from ucsmsdk.ucshandle import UcsHandle
import getpass
from ucsmsdk.mometa.fault.FaultInst import FaultInst
from collections import defaultdict

# check if the number of arugments provided are correct

run_as_script = True

if not len(sys.argv) > 1:
    print("Not enough arguments provided")
    print("Usage: {} <ip address> <username> <password>".format(sys.argv[0]))
    sys.exit(3)

# Create UCS handle and login to UCS system

try:
	password = sys.argv[3]
except:
	password = getpass.getpass("Password for " + sys.argv[2] + ": ")

handle = UcsHandle(ip=str(sys.argv[1]),username=str(sys.argv[2]),password=password)
# handle = UcsHandle(ip=sys.argv[1],username=sys.argv[2],password=sys.argv[3])
handle.login()

# Filter specific errors

filter_exp =  '(ack,"no",type="eq")'

# Collect UCS fualts using filter

ucs_faults = handle.query_classid("faultInst",filter_str=filter_exp)

# setup dictionary with default value for a new entry is an empty list

dict_of_faults = defaultdict(list)

# loop over faults and append it to the appropriate exit code key 
# UCS fault details can be found here
# https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/ts/faults/reference/ErrMess/FaultsIntroduction.html#wp1070261


# if ucs_faults is empty
# logout and return exit code '0'

if not ucs_faults:
	print("Everything is fine -- Keep Calm and Carry On!")
	handle.logout()
	sys.exit(0)

# else if ucs_fault is not empty 
# check each fault and parse it based on severity
# for 'critical' & 'major' events return 2
# for 'warning' return 1
# for anything else return 0
# status: An integer describing the service status. You may also use the class status definitions:
# AgentCheck.OK or 0 for success
# AgentCheck.WARNING or 1 for warning
# AgentCheck.CRITICAL or 2 for failure
# AgentCheck.UNKNOWN or 3 for indeterminate status
# https://docs.datadoghq.com/agent/agent_checks/

else:
	for fault in ucs_faults:
	    # Contruct fault msg format
	    fault_msg = '{} {} {} {}'.format(fault.severity,
                                                fault.type,
			                        fault.created,
			                        fault.descr)	    

	    if fault.severity.lower() in ['critical','major']:
	        dict_of_faults[2].append(fault_msg)
	    elif fault.severity.lower() in ['warning']:
	        dict_of_faults[1].append(fault_msg)
	    elif fault.severity.lower() in ['minor', 'info','cleared']:
	        dict_of_faults[0].append(fault_msg)
	    
	    # print out faults 
	    print(fault_msg)

handle.logout()
sys.exit(max(dict_of_faults.keys()))