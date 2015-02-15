#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# Andrei Vacariu wrote this code. As long as you retain this notice you can
# do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. <andrei@avacriu.me>
# ----------------------------------------------------------------------------

# This is a script for updating an A record on Amazon's Route53.
# It's intended to be run as a cron job.

from script_config import CF_EMAIL, CF_API_KEY, CF_REC_NAME, CF_ZONE

from pyflare import PyflareClient
import subprocess
import sys

# get the old IP address
dns_name = "%s.%s" % (CF_REC_NAME, CF_ZONE)
try:
    old_ip = subprocess.check_output(["dig +short %s" % dns_name], shell=True).strip().decode()
except Exception as e:
    print("Failed to get old IP.", e)
    sys.exit(1)

# get the new IP address
try:
    current_ip = subprocess.check_output(["dig +short myip.opendns.com @resolver1.opendns.com"], shell=True).strip().decode()
except Exception as e:
    print("Failed to get IP.", e)
    sys.exit(1)

# check that they're different
if old_ip == current_ip:
    sys.exit(0)

# the IP has changed, so let's update the record
cf = PyflareClient(CF_EMAIL, CF_API_KEY)
rec_id = None

for rec in cf.rec_load_all(CF_ZONE):
    if rec['display_name'] == CF_REC_NAME and rec['type'] == 'A':
        rec_id = rec['rec_id']
        break

if rec_id is None:
    print("Couldn't find the record.")
    sys.exit(2)

cf.rec_edit(CF_ZONE, 'A', int(rec_id), CF_REC_NAME, current_ip)
