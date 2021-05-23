#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False

. ./team-61-openrc.sh; ansible-playbook --ask-become-pass maintenance.yaml -i ./inventory/hosts.ini