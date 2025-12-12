#!/usr/bin/env python3
import aws_cdk as cdk

from InfraStack.networking_stack import NetworkingStack
from InfraStack.ec2_stack import Ec2Stack
from InfraStack.rds_stack import RdsStack

app = cdk.App()

env_us_east_1 = cdk.Environment(region="us-east-1")

# 1) Networking Stack: VPC, subnet, IGW, route table
networking_stack = NetworkingStack(
    app,
    "NetworkingStack",
    env=env_us_east_1,
)

# 2) EC2 Stack: depends on Networking
ec2_stack = Ec2Stack(
    app,
    "Ec2Stack",
    vpc=networking_stack.vpc,
    public_subnet=networking_stack.public_subnet_1,
    env=env_us_east_1,
)

# 3) RDS Stack: depends on Networking
rds_stack = RdsStack(
    app,
    "RdsStack",
    vpc=networking_stack.vpc,
    subnets=[networking_stack.public_subnet_1, networking_stack.public_subnet_2],
    env=env_us_east_1,
)

app.synth()
