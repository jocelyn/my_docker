#!/bin/bash

cd tags/nightly
docker build -f Dockerfile -t eiffel/eiffel:nightly .

