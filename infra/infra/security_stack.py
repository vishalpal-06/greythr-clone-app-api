from aws_cdk import (
    CfnOutput,
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class SecurityStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.Vpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --------------------------------------------------
        # ALB Security Group
        # --------------------------------------------------
        self.alb_sg = ec2.SecurityGroup(
            self,
            "AlbSG",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for Greythr Application Load Balancer",
        )

        self.alb_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP traffic",
        )

        # --------------------------------------------------
        # ECS Security Group
        # --------------------------------------------------
        self.ecs_sg = ec2.SecurityGroup(
            self,
            "EcsSG",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for Greythr ECS tasks",
        )

        # Only ALB can communicate with FastAPI container.
        self.ecs_sg.add_ingress_rule(
            self.alb_sg,
            ec2.Port.tcp(8000),
            "Allow ALB to access FastAPI",
        )

        CfnOutput(
            self,
            "AlbSecurityGroupId",
            value=self.alb_sg.security_group_id,
        )

        CfnOutput(
            self,
            "EcsSecurityGroupId",
            value=self.ecs_sg.security_group_id,
        )
