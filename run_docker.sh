#!/bin/bash

docker build -t mlperf-power .

docker run --rm -v $(pwd)/figures:/app/figures mlperf-power