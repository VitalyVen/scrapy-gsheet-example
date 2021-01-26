#!/bin/bash
pipenv --version > /dev/null||sudo apt install pipenv -y
pipenv install --dev