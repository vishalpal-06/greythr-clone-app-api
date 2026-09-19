import aws_cdk as cdk

from config import prod

from infra.alb_stack import AlbStack
from infra.ecr_stack import EcrStack
from infra.ecs_stack import ECSStack
from infra.ecs_service_stack import EcsServiceStack
from infra.iam_stack import IamStack
from infra.network_stack import NetworkStack
from infra.security_stack import SecurityStack

app = cdk.App()

image_tag = app.node.try_get_context("imageTag") or "latest"


# --------------------------------------------------
# Networking
# --------------------------------------------------
network = NetworkStack(
    app,
    "NetworkStack",
)


# --------------------------------------------------
# Security Groups
# --------------------------------------------------
security = SecurityStack(
    app,
    "SecurityStack",
    vpc=network.vpc,
)


# --------------------------------------------------
# Container Registry
# --------------------------------------------------
ecr = EcrStack(
    app,
    "EcrStack",
)


# --------------------------------------------------
# IAM
# --------------------------------------------------
iam = IamStack(
    app,
    "IamStack",
)


# --------------------------------------------------
# ECS Cluster
# --------------------------------------------------
ecs = ECSStack(
    app,
    "EcsStack",
    vpc=network.vpc,
)


# --------------------------------------------------
# Load Balancer
#
# ALB + Target Group only.
# --------------------------------------------------
alb = AlbStack(
    app,
    "AlbStack",
    vpc=network.vpc,
    alb_sg=security.alb_sg,
)


service = EcsServiceStack(
    app,
    "EcsServiceStack",
    cluster=ecs.cluster,
    repository=ecr.repo,
    execution_role=iam.execution_role,
    task_role=iam.task_role,
    ecs_security_group=security.ecs_sg,
    target_group=alb.target_group,
    log_group=ecs.log_group,
    image_tag=image_tag,
    cpu=prod.CPU,
    memory=prod.MEMORY,
    desired_tasks=prod.DESIRED_TASKS,
    min_tasks=prod.MIN_TASKS,
    max_tasks=prod.MAX_TASKS,
    container_port=prod.CONTAINER_PORT,
    cpu_target_utilization=prod.CPU_TARGET_UTILIZATION,
    memory_target_utilization=prod.MEMORY_TARGET_UTILIZATION,
)


app.synth()
