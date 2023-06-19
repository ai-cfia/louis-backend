# Deployment

## Azure
Edit configurations

* .env.prod: your .env for your container

Build (do this from your WSL Ubuntu where Docker is already installed):

```
docker build -t louis-demo .
```

test locally:

```
docker run -p 5000:5000 -e PORT=5000 louis-demo
```

output:

```
ngadamr@QCMONTC701988P:~/src/louis-crawler$ docker run -p 5000:5000 louis-demo
[2023-06-14 19:12:56 +0000] [1] [INFO] Starting gunicorn 20.1.0
[2023-06-14 19:12:56 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2023-06-14 19:12:56 +0000] [1] [INFO] Using worker: gthread
[2023-06-14 19:12:56 +0000] [7] [INFO] Booting worker with pid: 7
[2023-06-14 19:12:57 +0000] [8] [INFO] Booting worker with pid: 8
[2023-06-14 19:12:57 +0000] [23] [INFO] Booting worker with pid: 23
[2023-06-14 19:12:57 +0000] [24] [INFO] Booting worker with pid: 24
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
```

## pushing to azure

You first need to push the container to the private registry:

```
docker tag louis-demo $CONTAINER_REGISTRY.azurecr.io/louis-demo
docker login -u $CONTAINER_REGISTRY_ADMIN --pasword-stdin $CONTAINER_REGISTRY
docker push $CONTAINER_REGISTRY.azurecr.io/louis-demo
```

The password and username $CONTAINER_REGISTRY_ADMIN is from from Portal Azure Access Keys page of the container registry view.

## pushing to google cloud run

https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling

```
sudo snap install google-cloud-cli --classic
gcloud auth configure-docker <your registry location>
docker tag louis-demo <registry>/<project-id>/<repository>/louis-demo
docker push <registry>/<project-id>/<repository>/louis-demo
```

...and you can then deploy

## fixing errors 308

https://cloud.google.com/api-gateway/docs/get-started-cloud-run

https://cloud.google.com/run/docs/configuring/static-outbound-ip?utm_campaign=CDR_ahm_aap-severless_cloud-run-faq_&utm_source=external&utm_medium=web

## Manually testing endpoints

```
curl -X POST https://$HOSTNAME:$PORT/search -H "Content-Type: application/json" --data '{"query": "bacteria"}'
```

## psycopg native extensions use

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`p
g_config --libdir`; flask run --debug
```