from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2,
)

from constructs import Construct


class AlbStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.Vpc,
        alb_sg: ec2.SecurityGroup,
        service,
        **kwargs,
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        self.alb = elbv2.ApplicationLoadBalancer(
            self,
            "GreythrAlb",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_sg,
            load_balancer_name="greythr-alb",
        )

        listener = self.alb.add_listener(
            "HttpListener",
            port=80,
            open=True,
        )

        listener.add_targets(
            "GreythrTargetGroup",
            port=8000,
            targets=[service],
            health_check=elbv2.HealthCheck(
                path="/",
                healthy_http_codes="200",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                healthy_threshold_count=2,
                unhealthy_threshold_count=3,
            ),
        )

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

        self.alb_dns = self.alb.load_balancer_dns_name
