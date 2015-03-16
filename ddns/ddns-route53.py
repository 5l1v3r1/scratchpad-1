#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# Andrei Vacariu wrote this code. As long as you retain this notice you can 
# do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. <andrei@avacriu.me>
# ----------------------------------------------------------------------------

# This is a script for updating an A record on Amazon's Route53.
# It's intended to be run as a cron job.

from script_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, HOSTED_ZONE_ID

import route53
import subprocess
import sys

def current_IP():
    try:
        ip = subprocess.check_output(["dig +short myip.opendns.com @resolver1.opendns.com"], shell=True).strip().decode()
    except Exception as e:
        print("Failed to get IP.", e)
        sys.exit(1)
    return ip

def update_route53():
    conn = route53.connect(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY)

    zone = conn.get_hosted_zone_by_id(HOSTED_ZONE_ID)
    
    current_ip = current_IP()

    for record_set in zone.record_sets:
        if record_set.rrset_type == 'A':
            record_set.records = [current_ip]
            record_set.save()
            break

    with open("/tmp/last_ip_address", 'w') as last_ip:
        last_ip.write(current_ip)


def ip_changed():
    try:
        with open("/tmp/last_ip_address", 'r') as last_ip:
            ip = last_ip.read()
    except FileNotFoundError:
        return True
    else:
        if ip == current_IP():
            return False
    return True

if __name__ == "__main__":
    if ip_changed():
        update_route53()
