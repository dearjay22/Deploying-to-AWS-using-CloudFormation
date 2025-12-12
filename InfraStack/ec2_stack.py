from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
)
from constructs import Construct


class Ec2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, public_subnet: ec2.ISubnet, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Hardcoded AMI ID for us-east-1
        AMI_ID = "ami-0e86e20dae9224db8"

        # Hardcoded instance type
        INSTANCE_TYPE = "t3.micro"

        # Security Group (allow SSH from anywhere)
        sg = ec2.SecurityGroup(
            self,
            "Ec2SecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for EC2 allowing SSH",
            security_group_name="assignment3-ec2-sg",
        )

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow SSH from anywhere",
        )

        # EC2 instance
        instance = ec2.Instance(
            self,
            "Assignment3Ec2",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[public_subnet]),
            security_group=sg,
            instance_type=ec2.InstanceType(INSTANCE_TYPE),
            machine_image=ec2.MachineImage.generic_linux({
                self.region: AMI_ID
            }),
        )

        # Output Public IP for screenshot
        CfnOutput(
            self,
            "Ec2PublicIp",
            value=instance.instance_public_ip,
            description="Public IP of the EC2 instance",
        )
        CfnOutput(
            self,
            "Ec2InstanceId",
            value=instance.instance_id,
            description="EC2 Instance ID",
        )
