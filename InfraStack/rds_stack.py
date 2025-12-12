from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class RdsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, subnets: list, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Security group for RDS - allow MySQL from anywhere
        rds_sg = ec2.SecurityGroup(
            self,
            "RdsSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for RDS allowing MySQL (3306)",
            security_group_name="assignment3-rds-sg",
        )

        rds_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(3306),
            description="Allow MySQL access from anywhere",
        )

        # Subnet Group for RDS — requires >=2 AZs
        subnet_group = rds.SubnetGroup(
            self,
            "Assignment3RdsSubnetGroup",
            description="Subnet group for Assignment 3 RDS",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=subnets),
            subnet_group_name="assignment3-rds-subnet-group",
        )

        # Secret for master credentials
        credentials = rds.Credentials.from_generated_secret(
            username="admin",
            secret_name="assignment3-rds-credentials",
        )

        # RDS instance (MySQL 8.0)
        db = rds.DatabaseInstance(
            self,
            "Assignment3RdsInstance",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_5_7
            ),
            vpc=vpc,
            credentials=credentials,
            database_name="assignment3",
            multi_az=False,
            publicly_accessible=True,
            allocated_storage=20,
            max_allocated_storage=100,
            instance_type=ec2.InstanceType("t3.micro"),
            vpc_subnets=ec2.SubnetSelection(subnets=subnets),
            security_groups=[rds_sg],
            subnet_group=subnet_group,
        )

        # OUTPUTS for screenshot
        CfnOutput(
            self,
            "RdsEndpointAddress",
            value=db.db_instance_endpoint_address,
            description="RDS Endpoint Address",
        )

        CfnOutput(
            self,
            "RdsEndpointPort",
            value=db.db_instance_endpoint_port,
           description="RDS Endpoint Port",
        )

        CfnOutput(
            self,
            "DatabaseName",
            value="assignment3",
            description="Database Name",
        )
