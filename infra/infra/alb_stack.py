from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
)
from constructs import Construct


class AlbStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.Vpc,
        alb_sg: ec2.SecurityGroup,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --------------------------------------------------
        # Application Load Balancer
        # --------------------------------------------------
        self.alb = elbv2.ApplicationLoadBalancer(
            self,
            "GreythrAlb",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_sg,
            load_balancer_name="greythr-alb",
        )

        # --------------------------------------------------
        # ECS Target Group
        #
        # CDK owns the target group, but does NOT register
        # ECS tasks directly.
        #
        # ECS Service created by CI/CD will register Fargate
        # tasks automatically.
        # --------------------------------------------------
        self.target_group = elbv2.ApplicationTargetGroup(
            self,
            "GreythrTargetGroup",
            vpc=vpc,
            target_group_name="greythr-api-tg",
            port=8000,
            protocol=elbv2.ApplicationProtocol.HTTP,
            target_type=elbv2.TargetType.IP,
            health_check=elbv2.HealthCheck(
                path="/",
                healthy_http_codes="200",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                healthy_threshold_count=2,
                unhealthy_threshold_count=3,
            ),
        )

        # --------------------------------------------------
        # HTTP Listener
        # --------------------------------------------------
        listener = self.alb.add_listener(
            "HttpListener",
            port=80,
            open=True,
        )

        listener.add_target_groups(
            "GreythrForward",
            target_groups=[self.target_group],
        )

        # --------------------------------------------------
        # Outputs
        # --------------------------------------------------
        CfnOutput(
            self,
            "AlbDnsName",
            value=self.alb.load_balancer_dns_name,
        )

        CfnOutput(
            self,
            "AlbArn",
            value=self.alb.load_balancer_arn,
        )

        CfnOutput(
            self,
            "TargetGroupArn",
            value=self.target_group.target_group_arn,
        )
