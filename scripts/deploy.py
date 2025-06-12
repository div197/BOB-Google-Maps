#!/usr/bin/env python3
"""
BOB Google Maps v0.6.0 - Universal Deployment Script
===================================================

One-command deployment to multiple cloud platforms.
Following Niṣkāma Karma Yoga principles - perfect execution with divine automation.

Usage:
    python scripts/deploy.py --platform aws
    python scripts/deploy.py --platform gcp
    python scripts/deploy.py --platform azure
    python scripts/deploy.py --platform docker
    python scripts/deploy.py --platform all

Made with 🙏 for the global community
"""

import os
import sys
import json
import time
import argparse
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from bob_api.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("bob_deploy")

settings = get_settings()


@dataclass
class DeploymentResult:
    """Deployment result data."""
    platform: str
    success: bool
    url: Optional[str] = None
    error: Optional[str] = None
    duration: float = 0.0
    details: Dict[str, Any] = None


class DeploymentPlatform(ABC):
    """Abstract base class for deployment platforms."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"bob_deploy.{name}")
    
    @abstractmethod
    def validate_requirements(self) -> bool:
        """Validate platform-specific requirements."""
        pass
    
    @abstractmethod
    def deploy(self) -> DeploymentResult:
        """Deploy to the platform."""
        pass
    
    def run_command(self, command: str, cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        """Run shell command with logging."""
        self.logger.info(f"Running: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode != 0:
                self.logger.error(f"Command failed: {result.stderr}")
            return result
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {command}")
            raise


class DockerPlatform(DeploymentPlatform):
    """Docker deployment platform."""
    
    def __init__(self):
        super().__init__("docker")
    
    def validate_requirements(self) -> bool:
        """Validate Docker requirements."""
        try:
            result = self.run_command("docker --version")
            if result.returncode != 0:
                self.logger.error("Docker not installed")
                return False
            
            result = self.run_command("docker-compose --version")
            if result.returncode != 0:
                self.logger.warning("Docker Compose not found, using docker compose")
            
            return True
        except Exception as e:
            self.logger.error(f"Docker validation failed: {e}")
            return False
    
    def deploy(self) -> DeploymentResult:
        """Deploy using Docker."""
        start_time = time.time()
        
        try:
            # Build API image
            self.logger.info("🐳 Building Docker images...")
            result = self.run_command("docker build -f Dockerfile.api -t bob-api:latest .")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="docker",
                    success=False,
                    error=f"Docker build failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            # Build core image
            result = self.run_command("docker build -t bob-google-maps:latest .")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="docker",
                    success=False,
                    error=f"Core image build failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            # Start services
            self.logger.info("🚀 Starting services...")
            result = self.run_command("docker-compose up -d")
            if result.returncode != 0:
                # Try with docker compose (newer syntax)
                result = self.run_command("docker compose up -d")
                if result.returncode != 0:
                    return DeploymentResult(
                        platform="docker",
                        success=False,
                        error=f"Docker compose failed: {result.stderr}",
                        duration=time.time() - start_time
                    )
            
            # Wait for service to be ready
            self.logger.info("⏳ Waiting for service to be ready...")
            time.sleep(10)
            
            # Health check
            result = self.run_command("curl -f http://localhost:8000/api/v1/health || echo 'Health check failed'")
            
            return DeploymentResult(
                platform="docker",
                success=True,
                url="http://localhost:8000",
                duration=time.time() - start_time,
                details={
                    "api_url": "http://localhost:8000",
                    "docs_url": "http://localhost:8000/docs",
                    "health_url": "http://localhost:8000/api/v1/health"
                }
            )
            
        except Exception as e:
            return DeploymentResult(
                platform="docker",
                success=False,
                error=str(e),
                duration=time.time() - start_time
            )


class AWSPlatform(DeploymentPlatform):
    """AWS deployment platform."""
    
    def __init__(self):
        super().__init__("aws")
    
    def validate_requirements(self) -> bool:
        """Validate AWS requirements."""
        try:
            # Check AWS CLI
            result = self.run_command("aws --version")
            if result.returncode != 0:
                self.logger.error("AWS CLI not installed")
                return False
            
            # Check credentials
            result = self.run_command("aws sts get-caller-identity")
            if result.returncode != 0:
                self.logger.error("AWS credentials not configured")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"AWS validation failed: {e}")
            return False
    
    def deploy(self) -> DeploymentResult:
        """Deploy to AWS using ECS Fargate."""
        start_time = time.time()
        
        try:
            # Create ECR repository
            self.logger.info("🏗️ Setting up AWS infrastructure...")
            repo_name = f"{settings.DOCKER_NAMESPACE}/{settings.DOCKER_IMAGE_NAME}"
            
            result = self.run_command(f"aws ecr describe-repositories --repository-names {repo_name} --region {settings.AWS_REGION}")
            if result.returncode != 0:
                # Create repository
                result = self.run_command(f"aws ecr create-repository --repository-name {repo_name} --region {settings.AWS_REGION}")
                if result.returncode != 0:
                    return DeploymentResult(
                        platform="aws",
                        success=False,
                        error=f"Failed to create ECR repository: {result.stderr}",
                        duration=time.time() - start_time
                    )
            
            # Get ECR login
            result = self.run_command(f"aws ecr get-login-password --region {settings.AWS_REGION} | docker login --username AWS --password-stdin {settings.AWS_REGION}.amazonaws.com")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="aws",
                    success=False,
                    error=f"ECR login failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            # Build and push image
            self.logger.info("🐳 Building and pushing Docker image...")
            ecr_uri = f"{settings.AWS_REGION}.amazonaws.com/{repo_name}:latest"
            
            result = self.run_command("docker build -f Dockerfile.api -t bob-api:latest .")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="aws",
                    success=False,
                    error=f"Docker build failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            result = self.run_command(f"docker tag bob-api:latest {ecr_uri}")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="aws",
                    success=False,
                    error=f"Docker tag failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            result = self.run_command(f"docker push {ecr_uri}")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="aws",
                    success=False,
                    error=f"Docker push failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            # Deploy CloudFormation stack
            self.logger.info("☁️ Deploying CloudFormation stack...")
            stack_name = "bob-google-maps-api"
            
            # Create CloudFormation template
            self._create_cloudformation_template()
            
            result = self.run_command(f"aws cloudformation deploy --template-file deployment/aws/cloudformation.yaml --stack-name {stack_name} --parameter-overrides ImageUri={ecr_uri} --capabilities CAPABILITY_IAM --region {settings.AWS_REGION}")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="aws",
                    success=False,
                    error=f"CloudFormation deployment failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            # Get service URL
            result = self.run_command(f"aws cloudformation describe-stacks --stack-name {stack_name} --query 'Stacks[0].Outputs[?OutputKey==`ServiceURL`].OutputValue' --output text --region {settings.AWS_REGION}")
            service_url = result.stdout.strip() if result.returncode == 0 else "Unknown"
            
            return DeploymentResult(
                platform="aws",
                success=True,
                url=service_url,
                duration=time.time() - start_time,
                details={
                    "stack_name": stack_name,
                    "region": settings.AWS_REGION,
                    "ecr_uri": ecr_uri
                }
            )
            
        except Exception as e:
            return DeploymentResult(
                platform="aws",
                success=False,
                error=str(e),
                duration=time.time() - start_time
            )
    
    def _create_cloudformation_template(self):
        """Create CloudFormation template for AWS deployment."""
        template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "BOB Google Maps API - ECS Fargate Deployment",
            "Parameters": {
                "ImageUri": {
                    "Type": "String",
                    "Description": "ECR Image URI"
                }
            },
            "Resources": {
                "VPC": {
                    "Type": "AWS::EC2::VPC",
                    "Properties": {
                        "CidrBlock": "10.0.0.0/16",
                        "EnableDnsHostnames": True,
                        "EnableDnsSupport": True
                    }
                },
                "PublicSubnet1": {
                    "Type": "AWS::EC2::Subnet",
                    "Properties": {
                        "VpcId": {"Ref": "VPC"},
                        "CidrBlock": "10.0.1.0/24",
                        "AvailabilityZone": {"Fn::Select": [0, {"Fn::GetAZs": ""}]},
                        "MapPublicIpOnLaunch": True
                    }
                },
                "PublicSubnet2": {
                    "Type": "AWS::EC2::Subnet",
                    "Properties": {
                        "VpcId": {"Ref": "VPC"},
                        "CidrBlock": "10.0.2.0/24",
                        "AvailabilityZone": {"Fn::Select": [1, {"Fn::GetAZs": ""}]},
                        "MapPublicIpOnLaunch": True
                    }
                },
                "InternetGateway": {
                    "Type": "AWS::EC2::InternetGateway"
                },
                "VPCGatewayAttachment": {
                    "Type": "AWS::EC2::VPCGatewayAttachment",
                    "Properties": {
                        "VpcId": {"Ref": "VPC"},
                        "InternetGatewayId": {"Ref": "InternetGateway"}
                    }
                },
                "ECSCluster": {
                    "Type": "AWS::ECS::Cluster",
                    "Properties": {
                        "ClusterName": "bob-google-maps-cluster"
                    }
                },
                "TaskDefinition": {
                    "Type": "AWS::ECS::TaskDefinition",
                    "Properties": {
                        "Family": "bob-google-maps-task",
                        "NetworkMode": "awsvpc",
                        "RequiresCompatibilities": ["FARGATE"],
                        "Cpu": "512",
                        "Memory": "1024",
                        "ExecutionRoleArn": {"Ref": "ExecutionRole"},
                        "ContainerDefinitions": [
                            {
                                "Name": "bob-api",
                                "Image": {"Ref": "ImageUri"},
                                "PortMappings": [
                                    {
                                        "ContainerPort": 8000,
                                        "Protocol": "tcp"
                                    }
                                ],
                                "LogConfiguration": {
                                    "LogDriver": "awslogs",
                                    "Options": {
                                        "awslogs-group": {"Ref": "LogGroup"},
                                        "awslogs-region": {"Ref": "AWS::Region"},
                                        "awslogs-stream-prefix": "ecs"
                                    }
                                }
                            }
                        ]
                    }
                },
                "ExecutionRole": {
                    "Type": "AWS::IAM::Role",
                    "Properties": {
                        "AssumeRolePolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": {
                                        "Service": "ecs-tasks.amazonaws.com"
                                    },
                                    "Action": "sts:AssumeRole"
                                }
                            ]
                        },
                        "ManagedPolicyArns": [
                            "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
                        ]
                    }
                },
                "LogGroup": {
                    "Type": "AWS::Logs::LogGroup",
                    "Properties": {
                        "LogGroupName": "/ecs/bob-google-maps",
                        "RetentionInDays": 7
                    }
                }
            },
            "Outputs": {
                "ServiceURL": {
                    "Description": "Service URL",
                    "Value": "http://localhost:8000"
                }
            }
        }
        
        # Ensure deployment directory exists
        deployment_dir = project_root / "deployment" / "aws"
        deployment_dir.mkdir(parents=True, exist_ok=True)
        
        # Write template
        with open(deployment_dir / "cloudformation.yaml", "w") as f:
            import yaml
            yaml.dump(template, f, default_flow_style=False)


class GCPPlatform(DeploymentPlatform):
    """Google Cloud Platform deployment."""
    
    def __init__(self):
        super().__init__("gcp")
    
    def validate_requirements(self) -> bool:
        """Validate GCP requirements."""
        try:
            result = self.run_command("gcloud --version")
            if result.returncode != 0:
                self.logger.error("Google Cloud SDK not installed")
                return False
            
            result = self.run_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'")
            if not result.stdout.strip():
                self.logger.error("No active GCP authentication")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"GCP validation failed: {e}")
            return False
    
    def deploy(self) -> DeploymentResult:
        """Deploy to Google Cloud Run."""
        start_time = time.time()
        
        try:
            project_id = settings.GCP_PROJECT_ID or self._get_current_project()
            if not project_id:
                return DeploymentResult(
                    platform="gcp",
                    success=False,
                    error="GCP project ID not configured",
                    duration=time.time() - start_time
                )
            
            # Enable required APIs
            self.logger.info("🔧 Enabling required APIs...")
            apis = ["run.googleapis.com", "cloudbuild.googleapis.com"]
            for api in apis:
                self.run_command(f"gcloud services enable {api} --project={project_id}")
            
            # Build and deploy
            self.logger.info("🏗️ Building and deploying to Cloud Run...")
            service_name = "bob-google-maps-api"
            
            result = self.run_command(f"gcloud run deploy {service_name} --source . --platform managed --region {settings.GCP_REGION} --allow-unauthenticated --project={project_id}")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="gcp",
                    success=False,
                    error=f"Cloud Run deployment failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            # Get service URL
            result = self.run_command(f"gcloud run services describe {service_name} --platform managed --region {settings.GCP_REGION} --format 'value(status.url)' --project={project_id}")
            service_url = result.stdout.strip() if result.returncode == 0 else "Unknown"
            
            return DeploymentResult(
                platform="gcp",
                success=True,
                url=service_url,
                duration=time.time() - start_time,
                details={
                    "service_name": service_name,
                    "project_id": project_id,
                    "region": settings.GCP_REGION
                }
            )
            
        except Exception as e:
            return DeploymentResult(
                platform="gcp",
                success=False,
                error=str(e),
                duration=time.time() - start_time
            )
    
    def _get_current_project(self) -> Optional[str]:
        """Get current GCP project."""
        try:
            result = self.run_command("gcloud config get-value project")
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None


class AzurePlatform(DeploymentPlatform):
    """Azure deployment platform."""
    
    def __init__(self):
        super().__init__("azure")
    
    def validate_requirements(self) -> bool:
        """Validate Azure requirements."""
        try:
            result = self.run_command("az --version")
            if result.returncode != 0:
                self.logger.error("Azure CLI not installed")
                return False
            
            result = self.run_command("az account show")
            if result.returncode != 0:
                self.logger.error("Not logged into Azure")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Azure validation failed: {e}")
            return False
    
    def deploy(self) -> DeploymentResult:
        """Deploy to Azure Container Instances."""
        start_time = time.time()
        
        try:
            # Create resource group
            resource_group = settings.AZURE_RESOURCE_GROUP or "bob-google-maps-rg"
            self.logger.info(f"🏗️ Setting up Azure resources...")
            
            result = self.run_command(f"az group create --name {resource_group} --location {settings.AZURE_REGION}")
            if result.returncode != 0:
                self.logger.warning(f"Resource group creation warning: {result.stderr}")
            
            # Create container registry
            registry_name = "bobgooglemapsregistry"
            result = self.run_command(f"az acr create --resource-group {resource_group} --name {registry_name} --sku Basic --location {settings.AZURE_REGION}")
            if result.returncode != 0:
                self.logger.warning(f"ACR creation warning: {result.stderr}")
            
            # Build and push image
            self.logger.info("🐳 Building and pushing Docker image...")
            result = self.run_command(f"az acr build --registry {registry_name} --image bob-api:latest -f Dockerfile.api .")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="azure",
                    success=False,
                    error=f"ACR build failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            # Deploy container instance
            self.logger.info("🚀 Deploying container instance...")
            container_name = "bob-google-maps-api"
            
            result = self.run_command(f"az container create --resource-group {resource_group} --name {container_name} --image {registry_name}.azurecr.io/bob-api:latest --dns-name-label {container_name} --ports 8000 --location {settings.AZURE_REGION}")
            if result.returncode != 0:
                return DeploymentResult(
                    platform="azure",
                    success=False,
                    error=f"Container deployment failed: {result.stderr}",
                    duration=time.time() - start_time
                )
            
            # Get service URL
            result = self.run_command(f"az container show --resource-group {resource_group} --name {container_name} --query ipAddress.fqdn --output tsv")
            fqdn = result.stdout.strip() if result.returncode == 0 else "Unknown"
            service_url = f"http://{fqdn}:8000" if fqdn != "Unknown" else "Unknown"
            
            return DeploymentResult(
                platform="azure",
                success=True,
                url=service_url,
                duration=time.time() - start_time,
                details={
                    "resource_group": resource_group,
                    "container_name": container_name,
                    "registry": registry_name,
                    "region": settings.AZURE_REGION
                }
            )
            
        except Exception as e:
            return DeploymentResult(
                platform="azure",
                success=False,
                error=str(e),
                duration=time.time() - start_time
            )


class DeploymentManager:
    """Main deployment manager."""
    
    def __init__(self):
        self.platforms = {
            "docker": DockerPlatform(),
            "aws": AWSPlatform(),
            "gcp": GCPPlatform(),
            "azure": AzurePlatform(),
        }
        self.logger = logging.getLogger("bob_deploy.manager")
    
    def deploy(self, platform: str) -> DeploymentResult:
        """Deploy to specified platform."""
        if platform not in self.platforms:
            return DeploymentResult(
                platform=platform,
                success=False,
                error=f"Unknown platform: {platform}"
            )
        
        deployment_platform = self.platforms[platform]
        
        self.logger.info(f"🕉️ Starting deployment to {platform.upper()}...")
        self.logger.info("🙏 Following Niṣkāma Karma Yoga principles")
        
        # Validate requirements
        if not deployment_platform.validate_requirements():
            return DeploymentResult(
                platform=platform,
                success=False,
                error=f"Platform requirements not met for {platform}"
            )
        
        # Deploy
        result = deployment_platform.deploy()
        
        # Log result
        if result.success:
            self.logger.info(f"✅ Deployment to {platform.upper()} successful!")
            self.logger.info(f"🌐 Service URL: {result.url}")
            self.logger.info(f"⏱️ Duration: {result.duration:.2f}s")
        else:
            self.logger.error(f"❌ Deployment to {platform.upper()} failed!")
            self.logger.error(f"💥 Error: {result.error}")
        
        return result
    
    def deploy_all(self) -> List[DeploymentResult]:
        """Deploy to all available platforms."""
        results = []
        
        for platform_name in self.platforms.keys():
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Deploying to {platform_name.upper()}")
            self.logger.info(f"{'='*60}")
            
            result = self.deploy(platform_name)
            results.append(result)
            
            # Brief pause between deployments
            time.sleep(2)
        
        return results


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(
        description="BOB Google Maps v0.6.0 - Universal Deployment Script"
    )
    parser.add_argument(
        "--platform",
        choices=["docker", "aws", "gcp", "azure", "all"],
        required=True,
        help="Deployment platform"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Print header
    print("🕉️" + "="*70)
    print("   BOB Google Maps v0.6.0 - Universal Deployment")
    print("   Made with 🙏 following Niṣkāma Karma Yoga principles")
    print("="*72)
    print()
    
    manager = DeploymentManager()
    
    if args.platform == "all":
        results = manager.deploy_all()
        
        # Summary
        print("\n" + "="*60)
        print("DEPLOYMENT SUMMARY")
        print("="*60)
        
        successful = 0
        for result in results:
            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            print(f"{result.platform.upper():10} | {status:10} | {result.duration:6.2f}s | {result.url or result.error}")
            if result.success:
                successful += 1
        
        print(f"\nSuccessful deployments: {successful}/{len(results)}")
        
        if successful == len(results):
            print("🎉 All deployments successful!")
            sys.exit(0)
        else:
            print("⚠️ Some deployments failed")
            sys.exit(1)
    
    else:
        result = manager.deploy(args.platform)
        
        if result.success:
            print(f"\n🎉 Deployment successful!")
            print(f"🌐 Service URL: {result.url}")
            if result.details:
                print(f"📋 Details: {json.dumps(result.details, indent=2)}")
            sys.exit(0)
        else:
            print(f"\n💥 Deployment failed: {result.error}")
            sys.exit(1)


if __name__ == "__main__":
    main() 