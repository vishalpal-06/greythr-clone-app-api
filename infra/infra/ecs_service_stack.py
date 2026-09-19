from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct


class EcsServiceStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        cluster: ecs.Cluster,
        repository: ecr.Repository,
        execution_role: iam.Role,
        task_role: iam.Role,
        ecs_security_group: ec2.SecurityGroup,
        target_group: elbv2.ApplicationTargetGroup,
        log_group: logs.LogGroup,
        image_tag: str,
        cpu: int,
        memory: int,
        desired_tasks: int,
        min_tasks: int,
        max_tasks: int,
        container_port: int,
        cpu_target_utilization: int,
        memory_target_utilization: int,
        **kwargs,
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        # --------------------------------------------------
        # Task Definition
        # --------------------------------------------------
        task_definition = ecs.FargateTaskDefinition(
            self,
            "GreythrTaskDefinition",
            family="greythr-task",
            cpu=cpu,
            memory_limit_mib=memory,
            execution_role=execution_role,
            task_role=task_role,
        )

        # --------------------------------------------------
        # Container
        # --------------------------------------------------
        container = task_definition.add_container(
            "GreythrContainer",
            image=ecs.ContainerImage.from_ecr_repository(
                repository,
                tag=image_tag,
            ),
            essential=True,
            environment={
                "APP_ENV": "prod",
            },
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="greythr",
                log_group=log_group,
            ),
            health_check=ecs.HealthCheck(
                command=[
                    "CMD-SHELL",
                    f"python -c \"import urllib.request; urllib.request.urlopen('http://localhost:{container_port}/health')\" || exit 1",
                ],
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                retries=3,
                start_period=Duration.seconds(60),
            ),
        )

        container.add_port_mappings(
            ecs.PortMapping(
                container_port=container_port,
                protocol=ecs.Protocol.TCP,
            )
        )

        # --------------------------------------------------
        # ECS Fargate Service
        # --------------------------------------------------
        self.service = ecs.FargateService(
            self,
            "GreythrService",
            service_name="greythr-service",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=desired_tasks,
            assign_public_ip=False,
            security_groups=[
                ecs_security_group,
            ],
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
            ),
            # Rolling deployment configuration
            min_healthy_percent=100,
            max_healthy_percent=200,
            # Automatic rollback if deployment fails
            circuit_breaker=ecs.DeploymentCircuitBreaker(
                rollback=True,
            ),
            # Give container some time before ALB health checking matters
            health_check_grace_period=Duration.seconds(60),
        )

        # --------------------------------------------------
        # Connect ECS Service -> ALB Target Group
        # --------------------------------------------------
        self.service.attach_to_application_target_group(target_group)

        # --------------------------------------------------
        # ECS Auto Scaling
        # --------------------------------------------------
        scaling = self.service.auto_scale_task_count(
            min_capacity=min_tasks,
            max_capacity=max_tasks,
        )

        # CPU-based scaling
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=cpu_target_utilization,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )

        # Memory-based scaling
        scaling.scale_on_memory_utilization(
            "MemoryScaling",
            target_utilization_percent=memory_target_utilization,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )
