from aws_cdk import (
    CfnOutput,
    RemovalPolicy,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
)
from constructs import Construct


class ECSStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.Vpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ECS Cluster
        self.cluster = ecs.Cluster(
            self,
            "GreythrCluster",
            cluster_name="greythr-cluster",
            vpc=vpc,
            container_insights=True,
        )

        # CloudWatch log group used by application containers.
        #
        # Log infrastructure belongs to CDK.
        # The application Task Definition created by CI/CD will reference
        # this log group.
        self.log_group = logs.LogGroup(
            self,
            "GreythrLogGroup",
            log_group_name="/ecs/greythr-api",
            retention=logs.RetentionDays.ONE_MONTH,
            removal_policy=RemovalPolicy.RETAIN,
        )

        CfnOutput(
            self,
            "ClusterName",
            value=self.cluster.cluster_name,
        )

        CfnOutput(
            self,
            "LogGroupName",
            value=self.log_group.log_group_name,
        )
