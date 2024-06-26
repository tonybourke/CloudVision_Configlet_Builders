from cvplibrary import Form
from cvplibrary import CVPGlobalVariables, GlobalVariableNames
import yaml
from re import search

def get_hostname():
  stuff = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)
  for item in stuff:
    key, value = item.split(':')
    if key == 'hostname':
      hostname = value
  return(hostname)

hostname = get_hostname()



DC1 = """
spine1-DC1:
  interfaces:
    - loopback0: 192.168.101.101/32
    - Ethernet2: 192.168.103.1/31
    - Ethernet3: 192.168.103.7/31
    - Ethernet4: 192.168.103.13/31
    - Ethernet5: 192.168.103.19/31
    - Ethernet6: 192.168.103.25/31
    - Ethernet7: 192.168.103.31/31
  BGP:
    - ASN: 65100
spine2-DC1:
  interfaces:
    - loopback0: 192.168.101.102/32
    - Ethernet2: 192.168.103.3/31
    - Ethernet3: 192.168.103.9/31
    - Ethernet4: 192.168.103.15/31
    - Ethernet5: 192.168.103.21/31
    - Ethernet6: 192.168.103.27/31
    - Ethernet7: 192.168.103.33/31
  BGP:
    - ASN: 65100
spine3-DC1:
  interfaces:
    - loopback0: 192.168.101.103/32
    - Ethernet2: 192.168.103.5/31
    - Ethernet3: 192.168.103.11/31
    - Ethernet4: 192.168.103.17/31
    - Ethernet5: 192.168.103.23/31
    - Ethernet6: 192.168.103.29/31
    - Ethernet7: 192.168.103.35/31
  BGP:
    - ASN: 65100
leaf1-DC1:
  interfaces:
    - loopback0: 192.168.101.11/32
    - loopback1: 192.168.102.11/32
    - Ethernet3: 192.168.103.0/31
    - Ethernet4: 192.168.103.2/31
    - Ethernet5: 192.168.103.4/31
  BGP: 
    - ASN: 65101
leaf2-DC1:
  interfaces:
    - loopback0: 192.168.101.12/32
    - loopback1: 192.168.102.11/32
    - Ethernet3: 192.168.103.6/31
    - Ethernet4: 192.168.103.8/31
    - Ethernet5: 192.168.103.10/31
  BGP:
    - ASN: 65101
leaf3-DC1:
  interfaces:
    - loopback0: 192.168.101.13/32
    - loopback1: 192.168.102.13/32
    - Ethernet3: 192.168.103.12/31
    - Ethernet4: 192.168.103.14/31
    - Ethernet5: 192.168.103.16/31
  BGP:
    - ASN: 65102
leaf4-DC1:
  interfaces:
    - loopback0: 192.168.101.14/32
    - loopback1: 192.168.102.13/32
    - Ethernet3: 192.168.103.18/31
    - Ethernet4: 192.168.103.20/31
    - Ethernet5: 192.168.103.22/31
  BGP:
    - ASN: 65102
borderleaf1-DC1:
  interfaces:
    - loopback0: 192.168.101.21/32
    - loopback1: 192.168.102.21/32
    - Ethernet3: 192.168.103.24/31
    - Ethernet4: 192.168.103.26/31
    - Ethernet5: 192.168.103.28/31
  BGP:
    - ASN: 65103
borderleaf2-DC1:
  interfaces:
    - loopback0: 192.168.101.21/32
    - loopback1: 192.168.102.21/32
    - Ethernet3: 192.168.103.30/31
    - Ethernet4: 192.168.103.32/31
    - Ethernet5: 192.168.103.34/31
  BGP:
    - ASN: 65103
"""

dict = yaml.load(DC1)

# Create the interface
def gen_interfaces(interface, ipmask):
    print("interface %s") % (interface)
    print("  ip address %s") % (ipmask)


# Pull off the CIDR notation (needed for router-id)
def unmask(IP):
    maskless = IP.split("/", 1)
    return maskless[0]

def neighbors():
    print("  neighbor 192.168.101.101 peer-group eBGP-EVPN-Spines")
    print("  neighbor 192.168.101.102 peer-group eBGP-EVPN-Spines")
    print("  neighbor 192.168.101.103 peer-group eBGP-EVPN-Spines")
# Create the 
def gen_BGP_leaf(ASN,ip):
    router_id = unmask(ip)
    print("router bgp %s") % (ASN)
    print("  router-id %s") % (router_id)
    print("  neighbor eBGP-EVPN-Spines peer group")
    print("  neighbor eBGP-EVPN-Spines remote-as 65100")
    print("  neighbor eBGP-EVPN-Spines bfd")
    print("  neighbor eBGP-EVPN-Spines ebgp-multihop 5")
    print("  neighbor eBGP-EVPN-Spines send-community")
    print("  neighbor eBGP-EVPN-Spines maximum-routes 0")
    neighbors()
    print("")
    print("  address-family evpn")
    print("     neighbor eBGP-EVPN-Spines activate")
    print("")
    print("")

def config_leaf(leaf):
    for interfaces in dict[leaf]['interfaces']:
        for interface,ip in interfaces.items():
            gen_interfaces(interface,ip)
    for BGP in dict[switch]['BGP']:
        for key, ASN in BGP.items():
            ifaces = (dict[switch]['interfaces'])
            ip = ifaces[0]
            ifaces2 = ip['loopback0']
            gen_BGP_leaf(ASN, ifaces2)



for switch in dict:
  if switch == hostname:
        config_leaf(switch)




