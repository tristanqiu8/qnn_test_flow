#!/bin/bash
#=============================================================================
#
#  Copyright (c) 2020-2021 Qualcomm Technologies, Inc.
#  All Rights Reserved.
#  Confidential and Proprietary - Qualcomm Technologies, Inc.
#
#=============================================================================

PYV=`python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
if [ $PYV = '3.6' ]; then
    echo Supported version of Python found: $PYV

    #Check if pip3 is installed on the system
    if type pip3 &> /dev/null; then
        #Dependencies that are needed for running pip
        needed_depends=()
        needed_depends+=('numpy')
        needed_depends+=('scipy')
        needed_depends+=('scikit-image')
        needed_depends+=('pyyaml')
        needed_depends+=('mako')
        needed_depends+=('six')
        needed_depends+=('lxml')
        #Version Dependencies for packages
        version_depends=()
        version_depends+=('1.16.5')
        version_depends+=('1.3.1')
        version_depends+=('0.15.0')
        version_depends+=('3.10')
        version_depends+=('1.1.0')
        version_depends+=('1.14.0')
        version_depends+=('4.6.2')
        #Unmet dependencies
        need_to_install=()
        version_to_install=()
        i=0
        while [ $i -lt ${#needed_depends[*]} ]; do
            pip_version_str=$(pip3 show ${needed_depends[$i]} | grep "Version")
            if [[ ! -z "$pip_version_str" ]]; then
                if [ "$pip_version_str" == "Version: ${version_depends[$i]}" ]; then
                    echo "${needed_depends[$i]} is already installed with tested ${pip_version_str}"
                else
                    echo "WARNING: ${needed_depends[$i]} installed $pip_version_str does not match tested version: ${version_depends[$i]}"
                fi
                echo "-------------------------------------------------------------"
            else
                need_to_install+=("${needed_depends[$i]}")
                version_to_install+=("${version_depends[$i]}")
            fi
            i=$(( $i +1));
        done
        if [ ${#need_to_install[*]} -ne 0 ]; then
            i=0
            echo "Python Modules missing:"
            echo "=========================="
            while [ $i -lt ${#need_to_install[*]} ]; do
                echo "${need_to_install[$i]}"
                i=$(( $i +1));
            done
            echo "-------------------------------------------------------------"
            echo "Installing Missing Modules using pip3"
            echo "======================================="
            i=0
            while [ $i -lt ${#need_to_install[*]} ]; do
                echo "Installing ${need_to_install[$i]} Ver:${version_to_install[$i]}"
                pip3 install ${need_to_install[$i]}"=="${version_to_install[$i]}
                i=$(( $i +1));
            done
        else
           echo "All Dependency Modules Found"
        fi
    else
        echo pip3 is not installed. Please Install
    fi

else
    echo Supported versions of Python are 3.6 . Found instead:  $PYV
fi
echo "Done!!"
