#!/bin/bash

set -e

export INSTALL_DIR=$1
export MIST_HOST=$2
export MIST_PORT=$3
export SETUP_VIEW=$4
export PACKAGE_DIR=$5
export java64_home=$6

SETUP_VIEW=${SETUP_VIEW,,}
echo "SETUP_VIEW is $SETUP_VIEW"

SetupMist () {

    echo "Setting up Snapshot at $INSTALL_DIR"
    cd $INSTALL_DIR
        if [[ $SETUP_VIEW == "true" ]]
        then
            cp $PACKAGE_DIR/scripts/mist-ambari-view-0.0.1.jar .
            $java64_home/bin/jar xf mist-ambari-view-0.0.1.jar index.html
            sed -i "s/HOST_NAME:HOST_PORT/$MIST_HOST:$MIST_PORT/g" index.html
            $java64_home/bin/jar uf mist-ambari-view-0.0.1.jar index.html
        else
            echo "Skipping setup of Ambari view"
        fi
        echo "Skipping setup of Ambari view"

    }

SetupMist
echo "Setup complete"
