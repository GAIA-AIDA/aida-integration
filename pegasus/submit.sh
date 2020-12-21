#!/bin/bash

#--activate conda env before running this script
python daxgen.py workflow.dax

mkdir -p $(pwd)/workflows

pegasus-plan \
    --conf pegasus.conf \
    --dax workflow.dax \
    --dir $(pwd)/workflows \
    --cleanup leaf \
    --force \
    --sites saga \
    --output-site local \
    --submit
