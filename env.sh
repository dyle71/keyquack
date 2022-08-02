#!/usr/bin/bash

# ------------------------------------------------------------
# env.sh
#
# Setup development environment.
#
#   Do not call this directly but source it into your current shell.
#
#       Like:
#           $ source ./env.sh
#       or
#           $ . ./env.sh
#
# (C) Copyright 2021-2022, see the 'LICENSE' file in the project root.
# KEEQuant GmbH, https://www.keequant.com
# ------------------------------------------------------------

( return 0 2>/dev/null ) && SOURCED="yes" || SOURCED="no"
if [[ "${SOURCED}" == "no" ]]; then
    echo "Please do not call this script directly but source it into your current shell."
    echo "Like:"
    echo "$ source ${0}"
    exit 1
fi

echo "Setting up development environment..."

PROJECT_ROOT=$(dirname $(readlink -f ${BASH_SOURCE}))
pushd PROJECT_ROOT &> /dev/null

# Check for python3 installment.
PYTHON3=$(which python3)
if [[ "$?" != "0" ]]; then
    echo "Did not found python3. Please install a version."
    popd &> /dev/null
    exit 1
fi

# Setup virtual environment.
if [[ ! -d venv ]]; then
    ${PYTHON3} -m venv venv
fi

source venv/bin/activate
export PYTHONPATH=${PROJECT_ROOT}/src:${PROJECT_ROOT}/test
export PATH=${PROJECT_ROOT}/src/bin:${PATH}
export PROJECT_ROOT
popd &> /dev/null
