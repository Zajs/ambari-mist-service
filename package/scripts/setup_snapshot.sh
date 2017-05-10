#!/bin/bash

set -e
#e.g. /opt/incubator-zeppelin
export INSTALL_DIR=$1

export MIST_HOST=$2

export MIST_PORT=$3

export SETUP_VIEW=$4

export PACKAGE_DIR=$5
export java64_home=$6

SETUP_VIEW=${SETUP_VIEW,,}
echo "SETUP_VIEW is $SETUP_VIEW"

SetupMist () {

    echo "Setting up Mist at $INSTALL_DIR"
    cd $INSTALL_DIR
        if [[ $SETUP_VIEW == "true" ]]
        then
            cp $PACKAGE_DIR/scripts/mist-view-1.0-SNAPSHOT.jar .
            $java64_home/bin/jar xf mist-view-1.0-SNAPSHOT.jar index.html
            sed -i "s/HOST_NAME:HOST_PORT/$MIST_HOST:$MIST_PORT/g" index.html
            $java64_home/bin/jar uf mist-view-1.0-SNAPSHOT.jar index.html
        else
            echo "Skipping setup of Ambari view"
        fi
        echo "Skipping setup of Ambari view"

    }

SetupZeppelin
echo "Setup complete"
    
