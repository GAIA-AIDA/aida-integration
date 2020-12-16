#!/bin/bash

set -e

TOP_DIR=$(cd $(dirname $0) && pwd)
cd $TOP_DIR

PYTHONPATH=$(pegasus-config --python) python daxgen.py workflow.dax

pegasus-plan \
    --conf pegasus.conf \
    --dax workflow.dax \
    --dir $TOP_DIR/workflows \
    --cleanup leaf \
    --force \
    --sites saga \
    --output-site local \
    --submit
    

#--input-dir $TOP_DIR/input \
#--output-dir $TOP_DIR/output \
