#!/bin/bash

# Setup colour variables used throughout the script
GREEN=$'\e[0;32m'
RED=$'\e[0;31m'
BLUE=$'\e[0;34m'
YELLOW=$'\e[0;33m'
NC=$'\e[0m'

# Local username and group
NON_ROOT_USER="nruser"
NON_ROOT_GROUP="nrgroup"
NON_ROOT_USER_ID=2000
NON_ROOT_GROUP_ID=2000
LOCALLY_DEFINED_USER_PATTERN="nruser:x:2000:2000::/home/nruser:/usr/sbin/nologin"
LOCALLY_DEFINED_GROUP_PATTERN="nrgroup:x:2000"

# Define the directories here, so that the script can be templatised
TEMP_BASE_DATA_DIR="./tmp-data"

TEMP_BACKEND_POSTGRES_DIR="${TEMP_BASE_DATA_DIR}/tmp-backend-postgres"

TEMP_REDIS_DIR="${TEMP_BASE_DATA_DIR}/redis"

# Setup script variables
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $SCRIPT_DIR
cd ../..

# Extract hostname off host we are analysng
HOSTNAME=$(uname -n)

echo "${RED}************ STARTING TEMP DATA PREPARATION SCRIPT ... *************${NC}"
echo "===================================================================================================================="

# This block checks that certain directories are created, and if not, will print a message, then
# proceed to create them.
echo "==================================================================================================================="
echo "=========== Determining directories to be created =================="
echo "==== Checking for existing directory: ${BLUE}${TEMP_BACKEND_POSTGRES_DIR}${NC} ===="
if [ ! -d ${TEMP_BACKEND_POSTGRES_DIR} ]
then
    echo "==== Directory does not exist: ${YELLOW}${TEMP_BACKEND_POSTGRES_DIR}${NC} ===="
    mkdir -p ${TEMP_BACKEND_POSTGRES_DIR}
    echo "==== Directory now created: ${GREEN}${TEMP_BACKEND_POSTGRES_DIR}${NC} ===="
fi
echo "==== Checking for existing directory: ${BLUE}${TEMP_REDIS_DIR}${NC} ===="
if [ ! -d ${TEMP_REDIS_DIR} ]
then
    echo "==== Directory does not exist: ${YELLOW}${TEMP_REDIS_DIR}${NC} ===="
    mkdir -p ${TEMP_REDIS_DIR}
    echo "==== Directory now created: ${GREEN}${TEMP_REDIS_DIR}${NC} ===="
fi


echo "==================================================================================================================="
echo "===== Preparation complete for: ${GREEN}${HOSTNAME}${NC} ========="
echo "${RED}************ EXITING TEMP DATA PREPARATION SCRIPT ... *************${NC}"