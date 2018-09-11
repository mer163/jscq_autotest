#!/bin/bash

nohup python3 -m app.core.coreservice.py  >>coreservice.log 2>&1 &
