#!/usr/bin/env bash

#
# Copyright (c) 2022 Qualcomm Technologies, Inc.
# All Rights Reserved.
# Confidential and Proprietary - Qualcomm Technologies, Inc.
#

set -e  # catch all failures

# Following includes system requirements for building and running qnn-netron application
apt-get update
apt-get install -y libgtk-3-dev \
                   libasound2-dev \
                   libnss3 \
                   git \
                   nodejs \
                   npm \
                   libgbm-dev \
                   desktop-file-utils \
                   python3-dev \
                   python3-pip \
                   python3-setuptools

# setup npm
npm cache clean -f && npm install -g n && n 14.17.4
npm i -g npm@6.14.14
export npm_config_cache=/tmp/npm/

# install runtime python dependencies
pip3 install pip --upgrade
pip3 install absl-py==0.13.0 \
             matplotlib==3.3.4 \
             numpy==1.16.5 \
             pandas==0.24.2 \
             pathlib2==2.3.6 \
             Pillow==6.2.1 \
             six==1.16.0 \
             --no-cache
