#!/bin/bash

for dir in $(ls); do
    if [ -d ${dir}/.git ]; then
        echo $dir
        echo --------------
        cd $dir
        git pull
        cd ..
        echo
        echo --------------
    fi
done
