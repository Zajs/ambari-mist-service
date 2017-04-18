#!/bin/bash

SCALA_VERSION="2.10.4"

apt-get remove scala-library scala
wget www.scala-lang.org/files/archive/scala-$SCALA_VERSION.deb
dpkg -i scala-$SCALA_VERSION.deb
apt-get update
apt-get install scala
wget http://scalasbt.artifactoryonline.com/scalasbt/sbt-native-packages/org/scala-sbt/sbt/0.12.4/sbt.deb
dpkg -i sbt.deb
apt-get update
apt-get install sbt
