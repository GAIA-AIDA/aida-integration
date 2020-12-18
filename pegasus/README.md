# Setup Environment to use Pegasus API 
```
$ conda create --name aida-pegasus --file ./conda.list.txt 
$ conda activate aida-pegasus
$ python -m pip install --upgrade pip
$ python -m pip install -r ./pip.req.txt 
```

# Confirm Pegasus API
```
$ python
> import Pegasus.DAX3 as D
> repr(D)
"<module 'Pegasus.DAX3' from '/somepath/miniconda3/envs/aida-pegasus/lib/python3.8/site-packages/Pegasus/DAX3.py'>"
```
