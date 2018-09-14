#!/bin/bash

nohup python3 -m app.core.coreservice.py  >app/log/coreservice.log 2>&1 &
