
# cf-ecs-deploy

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

### Running in codefresh.io yaml