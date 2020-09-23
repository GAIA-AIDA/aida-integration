Kubernetes resources for the CACI leaderboard.


Create conda environment:
```
$ conda create --name gaia-aws --file gaia-aws.requirements.txt
```

Activate
```
$ conda activate gaia-aws
```

Check yaml file is valid YAML.
```
$ python -c 'import yaml, sys; yaml.safe_load(sys.stdin)' < ./ta1_gaia_pipeline_M36.yaml
```

Inspect AWS S3
```
$ aws s3 ls s3://${S3_TA1_GAIA} --recursive
```
