#!/usr/bin/env python

"""
Create DigitalOcean droplets with DNS entries
"""

import os
import sys
import time
import digitalocean

# API token and Domain name
API_TOKEN = os.environ['API_TOKEN']
DOMAIN_NAME = os.environ['DOMAIN_NAME']

# Objects for API requests
MANAGER = digitalocean.Manager(token=API_TOKEN)
DOMAIN = digitalocean.Domain(token=API_TOKEN,
                             name=DOMAIN_NAME)
DOMAIN_SLICE = len(DOMAIN_NAME)*-1


def generate_droplet_list():
    """
    Sort droplets by name
    """
    return sorted(MANAGER.get_all_droplets(), key=lambda x: x.name, reverse=False)

# List of available actions
ACTION_LIST = ["list", "create", "destroy", "dkim", "help"]

# List of droplet names
DROPLET_NAMELIST = []
for server in generate_droplet_list():
    if server.name[:4] == "test" and server.name[5] == ".":
        DROPLET_NAMELIST.append(server.name[:5])
    if server.name[:4] == "test" and server.name[5] != ".":
        DROPLET_NAMELIST.append(server.name[:6])

def list_droplets():
    """
    List all droplets
    """
    i = 1

    for droplet in generate_droplet_list():
        print(str(i) + " " + droplet.name)
        i += 1

def create_droplet():
    """
    Create new droplet
    """
    list_droplets()

    for i in range(1, 100):
        if "test"+str(i) not in DROPLET_NAMELIST:
            short_hostname = "test"+str(i)
            break

    droplet_name = input("Please, enter droplet short hostname (" + short_hostname + "): ")
    if droplet_name == "":
        droplet_name = short_hostname
    if droplet_name in DROPLET_NAMELIST:
        print("Droplet already exists!")
        exit(1)
    droplet = digitalocean.Droplet(token=API_TOKEN,
                                   name=droplet_name + '.' + DOMAIN_NAME,
                                   region='fra1',
                                   image='centos-7-x64',
                                   size_slug='1gb',
                                   backups=False)
    delete_dns_record(droplet) # if DNS record for unexisting droplet exists
    droplet.create()
    return droplet_name + '.' + DOMAIN_NAME

def choose_droplet():
    """
    Return droplet ID
    """
    list_droplets()
    droplet_number = input("Enter ID of droplet to destroy: ")
    droplet = generate_droplet_list()[int(droplet_number)-1]
    return droplet

def create_dns_record(droplet_name):
    """
    Create A record for droplet
    """
    time.sleep(5)
    for droplet in generate_droplet_list():
        if droplet.name == droplet_name:
            DOMAIN.create_new_domain_record(type="A",
                                            name=droplet.name[:DOMAIN_SLICE],
                                            data=droplet.ip_address)
            print("Created: " + droplet.name)

def delete_dns_record(droplet):
    """
    Delete A record of droplet
    """
    short_hostname = droplet.name[:DOMAIN_SLICE-1]
    for record in DOMAIN.get_records():
        if record.name == short_hostname:
            record.destroy()
            print("Deleted: " + record.name)

def create_txt_records(droplet, dkim_key):
    """
    Create TXT record for droplet
    """
    short_hostname = droplet.name[:DOMAIN_SLICE-1]
    DOMAIN.create_new_domain_record(type="TXT",
                                    name=short_hostname + '._domainkey.' + short_hostname,
                                    data=dkim_key)
    DOMAIN.create_new_domain_record(type="TXT",
                                    name='default' + '._domainkey.' + short_hostname,
                                    data=dkim_key)

def delete_txt_records(droplet):
    """
    Delete TXT record for droplet
    """
    short_hostname = droplet.name[:DOMAIN_SLICE-1]
    for record in DOMAIN.get_records():
        if record.name == short_hostname + '._domainkey.' + short_hostname:
            record.destroy()
            print("Deleted: " + record.name)
        if record.name == 'default' + '._domainkey.' + short_hostname:
            record.destroy()
            print("Deleted: " + record.name)

def add_dkim_record():
    """
    Add TXT record
    """
    list_droplets()
    droplet_number = input("Enter ID of droplet to add key: ")
    droplet = generate_droplet_list()[int(droplet_number)-1]
    dkim_key_raw = input("Enter DKIM key: ")
    dkim_key = "v=DKIM1; k=rsa; p=" + dkim_key_raw
    short_hostname = droplet.name[:DOMAIN_SLICE-1]
    delete_txt_records(droplet)
    create_txt_records(droplet, dkim_key)
    print("Record added. Commands to check:")
    print("nslookup -type=txt " + \
           short_hostname + "._domainkey." + short_hostname + "." + DOMAIN_NAME)
    print("nslookup -type=txt " + \
          "default" + "._domainkey." + short_hostname + "." + DOMAIN_NAME)

def cli_help():
    """
    Print usage help
    """
    print("USAGE:")
    print("\t list: list existing droplets")
    print("\t create: create new droplet with DNS A-record")
    print("\t destroy: destroy selected droplet")
    print("\t dkim: add key for DNS TXT-record and print DKIM validation command")

# MAIN FLOW

# Check input

if len(sys.argv) > 2:
    print("Extra argument given")
    exit(1)

elif len(sys.argv) < 2:
    cli_help()
    exit(0)

if sys.argv[1].lower() not in ACTION_LIST:
    print("Incorrect command")
    exit(1)

# Execute command

if sys.argv[1].lower() == "list":
    list_droplets()

elif sys.argv[1].lower() == "create":
    create_dns_record(create_droplet())

elif sys.argv[1].lower() == "destroy":
    DROPLET_TO_DELETE = choose_droplet()
    delete_dns_record(DROPLET_TO_DELETE)
    delete_txt_records(DROPLET_TO_DELETE)
    DROPLET_TO_DELETE.destroy()

elif sys.argv[1].lower() == "dkim":
    add_dkim_record()

elif sys.argv[1].lower() == "help":
    cli_help()
