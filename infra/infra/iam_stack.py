from aws_cdk import (
    CfnOutput,
    Stack,
    aws_iam as iam,
)
from constructs import Construct


class IamStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --------------------------------------------------
        # ECS Task Execution Role
        # --------------------------------------------------
        # Used by ECS itself for:
        # - pulling image from ECR
        # - writing container logs to CloudWatch
        # --------------------------------------------------
        self.execution_role = iam.Role(
            self,
            "GreythrTaskExecutionRole",
            role_name="greythr-task-execution-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"
                )
            ],
        )

        # --------------------------------------------------
        # ECS Task Role
        # --------------------------------------------------
        # This role is used by the FastAPI application itself.
        #
        # Currently no AWS permissions are attached.
        # Add permissions here later if the application needs:
        # - S3
        # - Secrets Manager
        # - SQS
        # - SNS
        # etc.
        # --------------------------------------------------
        self.task_role = iam.Role(
            self,
            "GreythrTaskRole",
            role_name="greythr-task-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        CfnOutput(
            self,
            "TaskExecutionRoleArn",
            value=self.execution_role.role_arn,
        )

        CfnOutput(
            self,
            "TaskRoleArn",
            value=self.task_role.role_arn,
        )
