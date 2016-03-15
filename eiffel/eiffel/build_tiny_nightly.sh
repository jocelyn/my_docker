#!/bin/bash

cd tags/tiny_nightly
docker build -f Dockerfile -t eiffel/eiffel:tiny_nightly .

