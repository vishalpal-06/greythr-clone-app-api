import aws_cdk as cdk

from infra.alb_stack import AlbStack
from infra.ecr_stack import EcrStack
from infra.ecs_stack import ECSStack
from infra.iam_stack import IamStack
from infra.network_stack import NetworkStack
from infra.security_stack import SecurityStack


app = cdk.App()


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
# ECS Infrastructure
#
# Cluster only.
# No Task Definition.
# No ECS Service.
# No application image.
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
# No direct ECS Service dependency.
# --------------------------------------------------
alb = AlbStack(
    app,
    "AlbStack",
    vpc=network.vpc,
    alb_sg=security.alb_sg,
)


app.synth()
