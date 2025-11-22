#!/bin/bash

source ./.env

echo -e "Container env: \n"
printenv
echo -e "\n"

sleep 2

python agent_eks_diagnose.py "$@"
