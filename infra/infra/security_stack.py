from aws_cdk import Stack, aws_ec2 as ec2
from constructs import Construct


class SecurityStack(Stack):

    def __init__(self, scope, construct_id, vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.alb_sg = ec2.SecurityGroup(self, "AlbSG", vpc=vpc, allow_all_outbound=True)

        self.alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))

        self.ecs_sg = ec2.SecurityGroup(self, "EcsSG", vpc=vpc, allow_all_outbound=True)

        self.ecs_sg.add_ingress_rule(self.alb_sg, ec2.Port.tcp(8000))
