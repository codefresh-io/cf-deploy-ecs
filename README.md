
# cf-ecs-deploy
Deploys to existing Amazon ECS Service

### Deployment Flow
- get ECS service by providing aws region, ecs cluster and service names
- create new revision from current task definition of the service. If --image-name and --image-tag are provided, replace the tag of the image
- launche update-service with new task definition revision
- wait for deployment to complete (by default, if running withou --no-wait)
    * deployment is considered as completed successfully if runningCount == desiredCount for PRIMARY deployment - see `aws ecs describe-service`
    * cfecs-update exits with timeout if after --timeout (default = 900s) runningCount != desiredCount script exits with timeout
    * cfecs-update exits with error if 4 or more ecs tasks were stopped with error for the task definition being deployed

### Usage with docker

```bash
docker run --rm -it -e AWS_ACCESS_KEY_ID=**** -e AWS_SECRET_ACCESS_KEY=**** codefresh/cf-ecs-deploy cfecs-update [options] <aws-region> <ecs-cluster-name> <ecs-service-name>
```

### Usage in codefresh.io yaml
```yaml
version: '1.0'

steps:
  build-step:
    type: build
    image-name: kosta709/cf-show-nodejs

  push to registry:
    type: push
    candidate: ${{build-step}}
    tag: ${{CF_BRANCH}}

  deploy to ecs:
    image: codefresh/cf-deploy-ecs
    commands:
      - cfecs-update eu-west-1 test1 service-cf-show-nodejs
    environment:
      - AWS_ACCESS_KEY_ID=${{AWS_ACCESS_KEY_ID}}
      - AWS_SECRET_ACCESS_KEY=${{AWS_SECRET_ACCESS_KEY}}

    when:
      - name: "Execute for 'master' branch"
        condition: "'${{CF_BRANCH}}' == 'master'"
```

### cfecs-update -h
```
usage: cfecs-update [-h] [-i IMAGE_NAME] [-t IMAGE_TAG] [--wait | --no-wait]
                    [--timeout TIMEOUT] [--debug]
                    region_name cluster_name service_name

Codefresh ECS Deploy

positional arguments:
  region_name           AWS Region, ex. us-east-1
  cluster_name          ECS Cluster Name
  service_name          ECS Service Name

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE_NAME, --image-name IMAGE_NAME
                        Image Name in ECS Task Definition to deploy
  -t IMAGE_TAG, --image-tag IMAGE_TAG
                        Tag for the in ECS Task Definition to deploy
  --wait                Wait for deployment to complete (default)
  --no-wait             No Wait for deployment to complete
  --timeout TIMEOUT     deployment wait timeout
  --debug               show debug messages

```