import logging
import sys
from pathlib import Path
from Pegasus.api import *

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
home = Path.home().absolute()
shared_scratch_dir = f"{home}/workflows/scratch"
local_storage_dir = f"{home}/workflows/output"
sc = SiteCatalog()
saga = Site("saga", arch=Arch.X86_64, os_type=OS.LINUX)

saga.add_directories(
    Directory(Directory.SHARED_SCRATCH, shared_scratch_dir).add_file_servers(
        FileServer("file://" + shared_scratch_dir, Operation.ALL)),
    Directory(Directory.LOCAL_STORAGE, local_storage_dir).add_file_servers(
        FileServer("file://" + local_storage_dir, Operation.ALL))
)

saga.add_env(key="PEGASUS_HOME", value="/nas/gaia/shared/cluster/pegasus5/pegasus-5.0.0")
saga.add_dagman_profile(retry=0)
# saga31 has docker installed
# srun --partition=gaia --account=gaia --nodelist=saga31 --pty bash
saga.add_pegasus_profile(
        style="glite", 
        auxillary_local=True, 
        data_configuration="sharedfs", 
        cores=1, 
        nodes=1, 
        runtime="14400",
        glite_arguments="--partition=gaia --account=gaia --gpus=1 --nodelist=saga31", 
        project="gaia",
        queue="gaia",
    )
saga.add_condor_profile(grid_resource="batch slurm")

sc.add_sites(saga)

tc = TransformationCatalog()

py36_container = Container(
            "py36-container",
            Container.DOCKER,
            image="file:///nas/gaia/shared/cluster/docker/python-3-6-3.tar",
            image_site="saga",
            arguments=" --gpus=1",
            mounts=[f"{shared_scratch_dir}:/shared-data"],
            bypass_staging=True,
        )
#props["pegasus.transfer.bypass.input.staging"] = "true"

tc.add_containers(py36_container)

py36_version = Transformation(
             "py36-version",
             site="saga",
             pfn="/usr/local/bin/python3.6", # This is the correct path in the python image
             is_stageable=False, # When is_stageable is set to False, this means that the transformation is installed at the given pfn inside of the container
             container=py36_container,
)             
# NOTE: similar docker example output:
# $ docker run -it python:3.6.3 /usr/local/bin/python3.6 -V
# Python 3.6.3

tc = tc.add_transformations(py36_version)

job = Job(py36_version).add_args(" -V").set_stdout("/shared-data/demo.out")

Workflow("demo", infer_dependencies=True)\
    .add_site_catalog(sc)\
    .add_transformation_catalog(tc)\
    .add_jobs(job)\
    .plan(submit=True).wait()
