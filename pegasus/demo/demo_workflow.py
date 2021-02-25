import logging
import sys
from pathlib import Path
from Pegasus.api import *

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
home = Path.home().absolute()
shared_scratch_dir = f"{home}/workflows/scratch"
local_storage_dir = f"{home}/workflows/output"
sc = SiteCatalog()
sc.add_sites(
    Site("local", arch=Arch.X86_64, os_type=OS.LINUX).add_directories(
        Directory(Directory.SHARED_SCRATCH, shared_scratch_dir).add_file_servers(
            FileServer("file://" + shared_scratch_dir, Operation.ALL)
        ),
        Directory(Directory.LOCAL_STORAGE, local_storage_dir).add_file_servers(
            FileServer("file://" + local_storage_dir, Operation.ALL)
        ),
    )
)

saga = Site("saga", arch=Arch.X86_64, os_type=OS.LINUX)

saga.add_directories(
    Directory(Directory.SHARED_SCRATCH, shared_scratch_dir).add_file_servers(
        FileServer("file://" + shared_scratch_dir, Operation.ALL)
    )
)

saga.add_env(
    key="PEGASUS_HOME", value="/nas/gaia/shared/cluster/pegasus5/pegasus-5.0.0"
)

saga.add_pegasus_profile(style="glite", auxillary_local=True, data_configuration="sharedfs")
saga.add_condor_profile(grid_resource="batch slurm")

sc.add_sites(saga)

# Container
py36_container = Container(
            "python36",
            Container.DOCKER,
            image="/nas/gaia/users/napiersk/archives/docker/python-3-6-3.tar",
            image_site="saga"
# ?other args: arguments, mounts, checksum, metadata, bypass_staging
        )

saga31_request = {"run_on_single_node": "saga31", "partition": "gaia"}

tc = TransformationCatalog().add_containers(py36_container)

py36_version = Transformation(
             "py36_version",
             pfn="/usr/local/bin/python",
             site="saga",
             container=py36_container,
# TODO: need to add resource request:?  resource_request=saga31_request,
# needed? type="INSTALLED",
)             

tc = tc.add_transformations(py36_version)

Workflow("demo", infer_dependencies=True, partition="scavenge")\
    .add_site_catalog(sc)\
    .add_transformation_catalog(tc)\
    .add_jobs(Job(py36_version).add_args(" -V").set_stdout("demo.out"))\
# TODO:         job.add_pegasus_profile(
#            runtime=self.job_time_in_minutes,
#            queue=str(self.partition.name),
#            project=None
#            if self.partition.name in (EPHEMERAL, SCAVENGE)
#            else self.partition.name,
#            glite_arguments=slurm_resource_content,
#        )
    .plan(submit=True).wait()
