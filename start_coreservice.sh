#!/bin/bash

nohup python3 -m app.core.coreservice.py  >app/core/coreservice.log 2>&1 &
