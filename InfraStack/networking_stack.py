from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
)
from constructs import Construct


class NetworkingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC with NO default subnets
        self.vpc = ec2.Vpc(
            self,
            "Assignment3Vpc",
            vpc_name="assignment3-vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            subnet_configuration=[],
        )

        # Public Subnet 1 - us-east-1a
        self.public_subnet_1 = ec2.Subnet(
            self,
            "PublicSubnet1",
            vpc_id=self.vpc.vpc_id,
            cidr_block="10.0.1.0/24",
            availability_zone=f"{self.region}a",
            map_public_ip_on_launch=True,
        )

        # Public Subnet 2 - us-east-1b
        self.public_subnet_2 = ec2.Subnet(
            self,
            "PublicSubnet2",
            vpc_id=self.vpc.vpc_id,
            cidr_block="10.0.2.0/24",
            availability_zone=f"{self.region}b",
            map_public_ip_on_launch=True,
        )

        # Internet Gateway
        igw = ec2.CfnInternetGateway(self, "InternetGateway")

        ec2.CfnVPCGatewayAttachment(
            self,
            "IgwAttachment",
            vpc_id=self.vpc.vpc_id,
            internet_gateway_id=igw.ref,
        )

        # Route Table
        route_table = ec2.CfnRouteTable(
            self,
            "PublicRouteTable",
            vpc_id=self.vpc.vpc_id,
        )

        ec2.CfnRoute(
            self,
            "DefaultRoute",
            route_table_id=route_table.ref,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=igw.ref,
        )

        # Subnet associations
        ec2.CfnSubnetRouteTableAssociation(
            self,
            "SubnetAssoc1",
            subnet_id=self.public_subnet_1.subnet_id,
            route_table_id=route_table.ref,
        )

        ec2.CfnSubnetRouteTableAssociation(
            self,
            "SubnetAssoc2",
            subnet_id=self.public_subnet_2.subnet_id,
            route_table_id=route_table.ref,
        )

        # Outputs
        CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
        CfnOutput(self, "OutputSubnetAZ1", value=self.public_subnet_1.subnet_id)
        CfnOutput(self, "OutputSubnetAZ2", value=self.public_subnet_2.subnet_id)
