#!/usr/bin/env python
"""
Python script to launch instances based on arguments provided by the user
through the command line.
Adapted from the python nova api client and openstack SDK.
Assumes a properly installed Openstack environment, and packages for the command
line client and the SDK are also installed.
Allows users to pass in arguments through the command line to customize VM
rather than using the coded defaults here.
"""
import time
import argparse
from credentials import get_nova_credentials_v2
from novaclient.client import Client

"""
Parser included so that users could designate specific parameters to be set
when launching an instance or to simply default to the set values
coded in this script.
"""
parser = argparse.ArgumentParser(description='Cabinet options.')
parser.add_argument('--n', metavar='name', type=str,
					dest="vm_name",default="VM1",
					help="Name of launched instance.")
parser.add_argument('--i', metavar='img', type=str,
					dest="image_name", default="cirros",
					help="Name of image to load.")
parser.add_argument('--f', metavar='flavor', type=str,
					dest="flavor_name", default="m1.tiny",
					help="Flavor for the instance.")

args = parser.parse_args()

vm_name = args.vm_name
image_name = args.image_name
flavor_name = args.flavor_name

"""
Code to launch a virtual machine instance through the nova client and
credentials obtained through environment variables. If there was more time I
could add additional arguments so that users have a larger degree of
customizability when it comes to their instances. I could also improve the error
handling surrounding edge cases and improper arguments. 
"""
try:
	credentials = get_nova_credentials_v2()
	nova_client = Client(**credentials)

	image = nova_client.images.find(name=image_name)
	flavor = nova_client.flavors.find(name=flavor_name)
	net = nova_client.networks.find(label=p"private")
	nics = [{'net-id': net.id}]
	instance = nova_client.servers.create(name=vm_name, image=image,
										  flavor=flavor, key_name="keypair-1",
										  nics=nics)
	print("Sleeping for 5s after create command")
	time.sleep(5)
	print("List of VMs")
	print(nova_client.servers.list())
finally:
	print("Server Create Completed")
