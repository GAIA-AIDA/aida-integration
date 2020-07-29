# aida-integration
Central repository for all public AIDA resources


Steps to run the pipeline in a local minikube K8 cluster (Note this will not run in kind as docker does not have the required NFS kernel module).

## Step 0: Launching a a kubernetes clsuter.
To launch a pure cluster with minikube simply run the following steps.

### Start K8 if it is not running already.
```
minikube start.
```

## Step 1: Creating an NFS filesystem server.
Kubernetes support different typese of filesytems. The local filesystem can be only shared between the pods. Hence, in order for different components of the pipeline to share data, we need a shared filesystem over network. NFS filesystem is one such fielsystem. In production, you can create such a filesystem in AWS, GCE, etc. and use the address to the service to read/write from/into the filesystem. In a local cluster you need to create one such fielsystem. Two componenets are required:

### An NFS server. 
I used a popular nfs-server container (cpuguy83/nfs-server) that makes such a filesytem locally. This server runs in a pod. 

### A service accessible to other pods.
In order to have a filesystem that can be shared between pods, you need to create a point of contact using a kubernetes service. A service facilitates the handshaking between a replica set providing a service and the uses of the service. It plays the role of a load balancer as well.

The service and the server pod are located put in file step_1_nfs_server.yaml. 
```
kubectl apply -f step_0_nfs_server.yaml
```

This will launch two separate nfs storages one read-only input and one writable output on the default tcp and udp ports.

## Step 2: Find servcie ips and create directories on the output NFS volume.
Once the NFS services are up, we need to look up their ip address.
```
kubectl get services
```
Which will generate something like this:
```
NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)            AGE
kubernetes           ClusterIP   10.96.0.1      <none>        443/TCP            96m
nfs-service-input    ClusterIP   10.105.45.53   <none>        2049/TCP,111/UDP   9m17s
nfs-service-output   ClusterIP   10.99.39.187   <none>        2049/TCP,111/UDP   9m17s
```
Take the ip address for each service and plug them into the everypod that attaches to the NFS volumes. Next, we need to create a directory where database files are stored. Submit the second step in a similar way.
```
kubectl apply -f step_2_job_init_nfs.yaml
```
This job runs once and creates a directory for storing outputs and db files
### Step 3: Launch the first deployment.
This project has only one deployment, however, in practice every pod that runs ethernally must run under a deployment. 
```
kubectl apply -f step_3_mongo_db_server.yaml
```
This will launches the mongo db server and stores the intermediate files in the nfs output volume. Note the ip to the service should be updated in this file.


### Step 4: Run a job for preprocessing.
This is a job which runs and completes once (as opposed to ethernal pods).
```
kubectl apply -f step_4_prep.yaml
```

### Step 5: Run the pipeline
```
kubectl apply -f step_4_pipeline.yaml
```
```
