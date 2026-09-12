from aws_cdk import Stack, RemovalPolicy, CfnOutput, aws_ecr as ecr
from constructs import Construct


class EcrStack(Stack):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.repo = ecr.Repository(
            self,
            "GreythrRepo",
            repository_name="greythr-api",
            image_scan_on_push=True,
            removal_policy=RemovalPolicy.RETAIN,
        )

        CfnOutput(self, "EcrRepoName", value=self.repo.repository_name)
