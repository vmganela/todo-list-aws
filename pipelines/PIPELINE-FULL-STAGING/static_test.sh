#!/bin/bash

source todo-list-aws/bin/activate
set -x

RAD_ERRORS=$(radon cc src -nc | wc -l)

if [[ $RAD_ERRORS -ne 0 ]]
then
    echo 'Ha fallado el análisis estatico de RADON - CC'
    exit 1
fi
RAD_ERRORS=$(radon mi src -nc | wc -l)
if [[ $RAD_ERRORS -ne 0 ]]
then
    echo 'Ha fallado el análisis estatico de RADON - MI'
    exit 1
fi

#flake8 src/*.py
#if [[ $? -ne 0 ]]
#then
#    echo 'Ha fallado el análisis de estilo(flake8)'
#    exit 1
#fi
bandit src/*.py
if [[ $? -ne 0 ]]
then
    echo 'Ha fallado el análisis de seguridad de codigo (bandit)'
    exit 1
fi
# PEP8 style guidelines
#pylint --errors-only src/*.py
#if [[ $? -ne 0 ]]
#then
#    echo 'Ha fallado el análisis de estilo(pylint)'
#    exit 1
#fi