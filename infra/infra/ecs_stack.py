from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
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
        ecs_sg: ec2.SecurityGroup,
        repository,
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

        # Task Definition
        task_def = ecs.FargateTaskDefinition(
            self,
            "GreythrTask",
            family="greythr-task",
            cpu=512,
            memory_limit_mib=1024,
        )

        # Container
        container = task_def.add_container(
            "GreythrContainer",
            image=ecs.ContainerImage.from_ecr_repository(repository),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="greythr",
                log_retention=logs.RetentionDays.ONE_MONTH,
            ),
            environment={
                "APP_ENV": "prod",
            },
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "curl -f http://localhost:8000/ || exit 1"],
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                retries=3,
                start_period=Duration.seconds(60),
            ),
        )

        # Port Mapping
        container.add_port_mappings(ecs.PortMapping(container_port=8000))

        # ECS Service
        self.service = ecs.FargateService(
            self,
            "GreythrService",
            service_name="greythr-service",
            cluster=self.cluster,
            task_definition=task_def,
            desired_count=1,
            assign_public_ip=False,
            security_groups=[ecs_sg],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True),
            min_healthy_percent=100,
            max_healthy_percent=200,
        )

        # Auto Scaling
        scaling = self.service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=10,
        )

        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70,
        )

        scaling.scale_on_memory_utilization(
            "MemoryScaling",
            target_utilization_percent=75,
        )

        # Outputs
        CfnOutput(
            self,
            "ClusterName",
            value=self.cluster.cluster_name,
        )

        CfnOutput(
            self,
            "ServiceName",
            value=self.service.service_name,
        )

        CfnOutput(
            self,
            "TaskDefinitionFamily",
            value="greythr-task",
        )
