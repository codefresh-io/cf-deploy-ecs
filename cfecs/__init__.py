import sys, json, pprint, boto3
from datetime import datetime

def now():
    return datetime.now().strftime('%d-%b-%Y %H:%M:%S.%f')[:-3]

def log(message):
    print('{}: {}'.format(now(), message))


def update_service(region, cluster_name, service_name):

    log("Entering cfecs.update_service: region = {} , cluster = {} , service = {}".format(region, cluster_name, service_name))
    ecs = boto3.client('ecs', region_name = region)
    services = ecs.describe_services(cluster=cluster_name, services=[service_name])

    service_def = services['services'][0]
    task_definition_name = service_def["taskDefinition"]
    log('task_definition_name = {}'.format(task_definition_name))

    task_definition_desc = ecs.describe_task_definition(taskDefinition = task_definition_name)
    task_definition = task_definition_desc['taskDefinition']
    keys_to_remove = ["status", "taskDefinitionArn", "requiresAttributes", "revision"]
    for k in keys_to_remove:
        task_definition.pop(k, None)

    register_task_resp = ecs.register_task_definition(**task_definition)
    new_task_arn = register_task_resp['taskDefinition']['taskDefinitionArn']

    log("new task arn: {}".format(new_task_arn))

    update_service_params = {
        'cluster': cluster_name,
        'service': service_name,
        'desiredCount': service_def['desiredCount'],
        'taskDefinition': new_task_arn,
        'deploymentConfiguration': service_def['deploymentConfiguration']
    }
    log("Updating Service: {}".format(pprint.pformat(update_service_params)))
    response = ecs.update_service(**update_service_params)
    return response

