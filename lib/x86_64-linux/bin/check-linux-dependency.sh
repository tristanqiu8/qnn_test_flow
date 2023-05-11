#!/bin/bash
#==============================================================================
#
#  Copyright (c) 2020-2021 Qualcomm Technologies, Inc.
#  All Rights Reserved.
#  Confidential and Proprietary - Qualcomm Technologies, Inc.
#
#==============================================================================

function verify_pkg_installed() {
  echo $(dpkg-query -W --showformat='${Status}\n' $1|grep "install ok installed")
}

function setup_clang-9() {
  # Get the clang-9 pre-built binaries from llvm releases
  sudo apt-get update
  pkgs_to_check=('build-essential' 'curl')
  j=0
  while [ $j -lt ${#pkgs_to_check[*]} ]; do
    install_status=$(verify_pkg_installed ${pkgs_to_check[$j]})
    if [ "$install_status" == "" ]; then
      sudo apt-get install -y ${pkgs_to_check[$j]}
    fi
    j=$(( $j +1));
  done
  clang_binary_name='clang+llvm-9.0.0-x86_64-linux-gnu-ubuntu-16.04'
  sudo curl -SL http://releases.llvm.org/9.0.0/$clang_binary_name.tar.xz | sudo tar -xJC /usr/local/.
  sudo mv /usr/local/$clang_binary_name /usr/local/clang-9.0.0
  echo "Setting Path Variable"
  export PATH=/usr/local/clang-9.0.0/bin:$PATH
  export LD_LIBRARY_PATH=/usr/local/clang-9.0.0/lib:$LD_LIBRARY_PATH
  echo "Setup Complete. clang-9 package at /usr/local/clang-9.0.0"
}

function setup_flatbuffers-compiler() {
  sudo apt-get update
  pkgs_to_check=('software-properties-common')
  j=0
  while [ $j -lt ${#pkgs_to_check[*]} ]; do
    install_status=$(verify_pkg_installed ${pkgs_to_check[$j]})
    if [ "$install_status" == "" ]; then
      sudo apt-get install -y ${pkgs_to_check[$j]}
    fi
    j=$(( $j +1));
  done

  sudo add-apt-repository 'deb http://cz.archive.ubuntu.com/ubuntu focal main universe'
  sudo apt-get update
  sudo apt-get install -y 'flatbuffers-compiler'
  echo "Setup Complete. flatc installed at /usr/bin/flatc"
}

function setup_libflatbuffers-dev() {
  sudo apt-get update
  pkgs_to_check=('software-properties-common')
  j=0
  while [ $j -lt ${#pkgs_to_check[*]} ]; do
    install_status=$(verify_pkg_installed ${pkgs_to_check[$j]})
    if [ "$install_status" == "" ]; then
      sudo apt-get install -y ${pkgs_to_check[$j]}
    fi
    j=$(( $j +1));
  done

  sudo add-apt-repository 'deb http://cz.archive.ubuntu.com/ubuntu focal main universe'
  sudo apt-get update
  sudo apt-get install -y 'libflatbuffers-dev'
  echo "Setup Complete. libflatbuffers-dev installed."
}

function setup_rename() {
  sudo apt-get update
  pkgs_to_check=('software-properties-common')
  j=0
  while [ $j -lt ${#pkgs_to_check[*]} ]; do
    install_status=$(verify_pkg_installed ${pkgs_to_check[$j]})
    if [ "$install_status" == "" ]; then
      sudo apt-get install -y ${pkgs_to_check[$j]}
    fi
    j=$(( $j +1));
  done

  sudo add-apt-repository 'deb http://cz.archive.ubuntu.com/ubuntu focal main universe'
  sudo apt-get update
  sudo apt-get install -y 'rename'
  echo "Setup Complete. rename installed at /usr/bin/rename"
}

#Linux Package dependencies that are needed for QNN SDK
needed_depends=()
needed_depends+=('clang-9')
needed_depends+=('flatbuffers-compiler')
needed_depends+=('libflatbuffers-dev')
needed_depends+=('rename')

#Unmet dependencies
need_to_install=()
i=0
while [ $i -lt ${#needed_depends[*]} ]; do
  echo "Checking for ${needed_depends[$i]}: $PKG_INSTALLED"
  case "${needed_depends[$i]}" in
    clang-9 )
      PKG_INSTALLED=$(verify_pkg_installed ${needed_depends[$i]})
      if [ "$PKG_INSTALLED" == "" ]; then
        #Check if package  previously downloaded
        if [ -d /usr/local/clang-9.0.0 ]; then
          case ":$PATH:" in
            *:/usr/local/clang-9.0.0/bin:*) echo "clang-9 Found: /usr/local/clang-9.0.0";;
            *) export PATH=/usr/local/clang-9.0.0/bin:$PATH
               echo "clang-9 Found: /usr/local/clang-9.0.0 . Added to PATH variable";;
          esac
          case ":$LD_LIBRARY_PATH:" in
            *:/usr/local/clang-9.0.0/lib:*) ;;
            *) export LD_LIBRARY_PATH=/usr/local/clang-9.0.0/lib:$LD_LIBRARY_PATH;;
          esac
        else
          echo "No pre-installed ${needed_depends[$i]} is found!!"
          need_to_install+=(${needed_depends[$i]})
        fi
      fi
      ;;
    flatbuffers-compiler )
      PKG_INSTALLED=$(verify_pkg_installed ${needed_depends[$i]})
      if [ "$PKG_INSTALLED" == "" ]; then
        if [ -d /usr/bin/flatc ]; then
          case ":$PATH:" in
            *:/usr/bin/flatc:*) echo "flatc Found: /usr/bin/flatc";;
            *) export PATH=/usr/bin/flatc:$PATH
               echo "flatc Found: /usr/bin/flatc. Added to PATH variable";;
          esac
        else
          echo "No pre-installed ${needed_depends[$i]} is found!!"
          need_to_install+=(${needed_depends[$i]})
        fi
      fi
      ;;
    libflatbuffers-dev )
      PKG_INSTALLED=$(verify_pkg_installed ${needed_depends[$i]})
      if [ "$PKG_INSTALLED" == "" ]; then
        if [ -d /usr/include/flatbuffers ]; then
          echo "libfatbuffers-dev found at /usr/include/flatbuffers"
        else
          echo "No pre-installed ${needed_depends[$i]} is found!!"
          need_to_install+=(${needed_depends[$i]})
        fi
      fi
      ;;
    rename )
      PKG_INSTALLED=$(verify_pkg_installed ${needed_depends[$i]})
      if [ "$PKG_INSTALLED" == "" ]; then
        if [ -d /usr/bin/rename ]; then
          case ":$PATH:" in
            *:/usr/bin/rename:*) echo "rename Found: /usr/bin/rename";;
            *) export PATH=/usr/bin/rename:$PATH
               echo "rename found at /usr/bin/rename"
          esac
        else
          echo "No pre-installed ${needed_depends[$i]} is found!!"
          need_to_install+=(${needed_depends[$i]})
        fi
      fi
      ;;
  esac
  i=$(( $i +1));
done
echo "============================================================="
if [ ${#need_to_install[*]} -ne 0 ]; then
  i=0
  echo "Installing Missing Packages"
  echo "--------------------------------------------------------------"
  while [ $i -lt ${#need_to_install[*]} ]; do
    echo "Setting up Package: ${need_to_install[$i]}"
    case "${need_to_install[$i]}" in
      clang-9 )
        setup_clang-9
        ;;
      flatbuffers-compiler )
        setup_flatbuffers-compiler
        ;;
      libflatbuffers-dev )
        setup_libflatbuffers-dev
        ;;
      rename )
        setup_rename
        ;;
    esac
    i=$(( $i +1));
    echo "--------------------------------------------------------------"
  done
else
  echo "All Dependency Packages Found"
fi
echo "Done!!"
