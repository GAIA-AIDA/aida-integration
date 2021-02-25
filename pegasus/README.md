# Setup Environment to use Pegasus API 
```
$ conda create --name aida-pegasus --file ./conda.list.txt 
$ conda activate aida-pegasus
(aida-pegasus) $ python -m pip install --upgrade pip
(aida-pegasus) $ python -m pip install -r ./pip.req.txt 
```

# Confirm Pegasus API
```
$ conda activate aida-pegasus
(aida-pegasus) $ python -c 'import Pegasus.DAX3 as D; print(repr(D));'
/somepath/miniconda3/envs/aida-pegasus/lib/python3.8/site-packages/Pegasus/DAX3.py:162: DeprecationWarning: Pegasus.DAX3 API has been deprecated and will be removed in v5.1.0. Please use the new API released in v5.0.0.
  warnings.warn(
<module 'Pegasus.DAX3' from '/nas/home/napiersk/miniconda3/envs/aida-pegasus/lib/python3.8/site-packages/Pegasus/DAX3.py'>
```

# Generate and Submit a Workflow
```
(aida-pegasus) $ . ./submit.sh
```
