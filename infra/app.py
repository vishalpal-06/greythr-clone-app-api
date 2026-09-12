import aws_cdk as cdk

from infra.network_stack import NetworkStack
from infra.security_stack import SecurityStack
from infra.ecr_stack import EcrStack
from infra.ecs_stack import ECSStack
from infra.alb_stack import AlbStack

app = cdk.App()

network = NetworkStack(app, "NetworkStack")

security = SecurityStack(app, "SecurityStack", vpc=network.vpc)

ecr = EcrStack(app, "EcrStack")

ecs = ECSStack(app, "EcsStack", vpc=network.vpc, ecs_sg=security.ecs_sg, repository=ecr.repo)

alb = AlbStack(app, "AlbStack", vpc=network.vpc, alb_sg=security.alb_sg, service=ecs.service)

app.synth()
