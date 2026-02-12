#!/usr/bin/env python3
"""
TERRAFORM ARCHITECT BRAIN
Based on original bakery-lab (121M) + terraform projects
Automated infrastructure deployment with AI-powered optimization
GCP, AWS, Azure multi-cloud orchestration
"""

import os
import json
import yaml
import asyncio
import subprocess
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import tempfile
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudProvider(Enum):
    GCP = "gcp"
    AWS = "aws"
    AZURE = "azure"
    DIGITALOCEAN = "digitalocean"
    LINODE = "linode"

class InfrastructureType(Enum):
    WEB_APP = "web_app"
    DATABASE = "database"
    KUBERNETES = "kubernetes"
    SERVERLESS = "serverless"
    STORAGE = "storage"
    NETWORKING = "networking"
    SECURITY = "security"
    MONITORING = "monitoring"

class DeploymentStage(Enum):
    PLANNING = "planning"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    VERIFICATION = "verification"
    MONITORING = "monitoring"
    OPTIMIZATION = "optimization"

@dataclass
class InfrastructureRequest:
    id: str
    name: str
    description: str
    cloud_provider: CloudProvider
    infrastructure_type: InfrastructureType
    requirements: Dict[str, Any]
    budget_limit: float
    region: str
    environment: str  # dev, staging, prod
    created_at: datetime
    status: str = "pending"

@dataclass
class TerraformModule:
    name: str
    source: str
    version: str
    variables: Dict[str, Any]
    outputs: List[str]
    dependencies: List[str]

class TerraformGenerator:
    """Generate Terraform configurations based on requirements"""
    
    def __init__(self):
        self.module_templates = self.load_module_templates()
        self.provider_configs = self.load_provider_configs()
    
    def load_module_templates(self) -> Dict[str, Dict]:
        """Load Terraform module templates"""
        return {
            "gcp_web_app": {
                "compute_engine": {
                    "source": "terraform-google-modules/vm/google",
                    "version": "~> 7.0",
                    "variables": {
                        "project_id": "var.project_id",
                        "zone": "var.zone",
                        "machine_type": "e2-medium",
                        "image": "ubuntu-2004-lts",
                        "disk_size_gb": 20,
                        "network": "default"
                    }
                },
                "load_balancer": {
                    "source": "terraform-google-modules/lb-http/google",
                    "version": "~> 6.0",
                    "variables": {
                        "project": "var.project_id",
                        "name": "var.app_name",
                        "ssl": True,
                        "managed_ssl_certificate_domains": ["var.domain"]
                    }
                },
                "cloud_sql": {
                    "source": "terraform-google-modules/sql-db/google//modules/postgresql",
                    "version": "~> 13.0",
                    "variables": {
                        "project_id": "var.project_id",
                        "name": "var.db_name",
                        "database_version": "POSTGRES_13",
                        "tier": "db-f1-micro",
                        "zone": "var.zone"
                    }
                }
            },
            "aws_web_app": {
                "ec2_instance": {
                    "source": "terraform-aws-modules/ec2-instance/aws",
                    "version": "~> 4.0",
                    "variables": {
                        "name": "var.app_name",
                        "instance_type": "t3.micro",
                        "ami": "data.aws_ami.ubuntu.id",
                        "vpc_security_group_ids": ["aws_security_group.web.id"],
                        "subnet_id": "aws_subnet.public.id"
                    }
                },
                "rds": {
                    "source": "terraform-aws-modules/rds/aws",
                    "version": "~> 5.0",
                    "variables": {
                        "identifier": "var.db_name",
                        "engine": "postgres",
                        "engine_version": "13.7",
                        "instance_class": "db.t3.micro",
                        "allocated_storage": 20,
                        "db_name": "var.db_name",
                        "username": "var.db_username",
                        "password": "var.db_password"
                    }
                }
            },
            "kubernetes_cluster": {
                "gke": {
                    "source": "terraform-google-modules/kubernetes-engine/google",
                    "version": "~> 24.0",
                    "variables": {
                        "project_id": "var.project_id",
                        "name": "var.cluster_name",
                        "region": "var.region",
                        "zones": ["var.zone"],
                        "initial_node_count": 1,
                        "node_config": {
                            "machine_type": "e2-medium",
                            "disk_size_gb": 100,
                            "oauth_scopes": [
                                "https://www.googleapis.com/auth/cloud-platform"
                            ]
                        }
                    }
                },
                "eks": {
                    "source": "terraform-aws-modules/eks/aws",
                    "version": "~> 19.0",
                    "variables": {
                        "cluster_name": "var.cluster_name",
                        "cluster_version": "1.24",
                        "vpc_id": "aws_vpc.main.id",
                        "subnet_ids": ["aws_subnet.private[*].id"],
                        "node_groups": {
                            "main": {
                                "desired_capacity": 2,
                                "max_capacity": 4,
                                "min_capacity": 1,
                                "instance_types": ["t3.medium"]
                            }
                        }
                    }
                }
            }
        }
    
    def load_provider_configs(self) -> Dict[str, Dict]:
        """Load provider configurations"""
        return {
            "gcp": {
                "terraform": {
                    "required_providers": {
                        "google": {
                            "source": "hashicorp/google",
                            "version": "~> 4.0"
                        }
                    }
                },
                "provider": {
                    "google": {
                        "project": "var.project_id",
                        "region": "var.region",
                        "zone": "var.zone"
                    }
                }
            },
            "aws": {
                "terraform": {
                    "required_providers": {
                        "aws": {
                            "source": "hashicorp/aws",
                            "version": "~> 5.0"
                        }
                    }
                },
                "provider": {
                    "aws": {
                        "region": "var.region"
                    }
                }
            },
            "azure": {
                "terraform": {
                    "required_providers": {
                        "azurerm": {
                            "source": "hashicorp/azurerm",
                            "version": "~> 3.0"
                        }
                    }
                },
                "provider": {
                    "azurerm": {
                        "features": {}
                    }
                }
            }
        }
    
    def generate_terraform_config(self, request: InfrastructureRequest) -> Dict[str, str]:
        """Generate complete Terraform configuration"""
        config_files = {}
        
        # Generate main.tf
        config_files["main.tf"] = self.generate_main_tf(request)
        
        # Generate variables.tf
        config_files["variables.tf"] = self.generate_variables_tf(request)
        
        # Generate outputs.tf
        config_files["outputs.tf"] = self.generate_outputs_tf(request)
        
        # Generate terraform.tfvars
        config_files["terraform.tfvars"] = self.generate_tfvars(request)
        
        # Generate versions.tf
        config_files["versions.tf"] = self.generate_versions_tf(request)
        
        return config_files
    
    def generate_main_tf(self, request: InfrastructureRequest) -> str:
        """Generate main Terraform configuration"""
        provider = request.cloud_provider.value
        infra_type = request.infrastructure_type.value
        
        # Start with provider configuration
        config = self.provider_configs.get(provider, {})
        main_tf = self.dict_to_hcl(config)
        
        # Add resources based on infrastructure type
        if infra_type == "web_app":
            main_tf += self.generate_web_app_resources(request)
        elif infra_type == "kubernetes":
            main_tf += self.generate_kubernetes_resources(request)
        elif infra_type == "database":
            main_tf += self.generate_database_resources(request)
        elif infra_type == "serverless":
            main_tf += self.generate_serverless_resources(request)
        
        return main_tf
    
    def generate_web_app_resources(self, request: InfrastructureRequest) -> str:
        """Generate web application resources"""
        provider = request.cloud_provider.value
        resources = ""
        
        if provider == "gcp":
            # Compute Engine instance
            resources += '''
# Compute Engine Instance
resource "google_compute_instance" "web_server" {
  name         = "${var.app_name}-web"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = var.disk_size_gb
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = file("${path.module}/startup-script.sh")

  tags = ["web-server", var.environment]
}

# Cloud SQL Database
resource "google_sql_database_instance" "main" {
  name             = "${var.app_name}-db"
  database_version = "POSTGRES_13"
  region           = var.region

  settings {
    tier = var.db_tier
    
    backup_configuration {
      enabled = true
    }
    
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        value = "0.0.0.0/0"
        name  = "all"
      }
    }
  }

  deletion_protection = false
}

resource "google_sql_database" "database" {
  name     = var.db_name
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "user" {
  name     = var.db_username
  instance = google_sql_database_instance.main.name
  password = var.db_password
}

# Load Balancer
resource "google_compute_global_address" "default" {
  name = "${var.app_name}-address"
}

resource "google_compute_global_forwarding_rule" "default" {
  name       = "${var.app_name}-forwarding-rule"
  target     = google_compute_target_http_proxy.default.id
  port_range = "80"
  ip_address = google_compute_global_address.default.address
}

resource "google_compute_target_http_proxy" "default" {
  name    = "${var.app_name}-proxy"
  url_map = google_compute_url_map.default.id
}

resource "google_compute_url_map" "default" {
  name            = "${var.app_name}-url-map"
  default_service = google_compute_backend_service.default.id
}

resource "google_compute_backend_service" "default" {
  name        = "${var.app_name}-backend"
  port_name   = "http"
  protocol    = "HTTP"
  timeout_sec = 10

  backend {
    group = google_compute_instance_group.web_servers.id
  }

  health_checks = [google_compute_http_health_check.default.id]
}

resource "google_compute_instance_group" "web_servers" {
  name = "${var.app_name}-instance-group"
  zone = var.zone

  instances = [google_compute_instance.web_server.id]

  named_port {
    name = "http"
    port = "80"
  }
}

resource "google_compute_http_health_check" "default" {
  name               = "${var.app_name}-health-check"
  request_path       = "/health"
  check_interval_sec = 30
  timeout_sec        = 5
}
'''
        
        elif provider == "aws":
            resources += '''
# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.app_name}-vpc"
    Environment = var.environment
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.app_name}-igw"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.app_name}-public-subnet"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.app_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security Group
resource "aws_security_group" "web" {
  name_prefix = "${var.app_name}-web"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.app_name}-web-sg"
  }
}

# EC2 Instance
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name              = var.key_name
  vpc_security_group_ids = [aws_security_group.web.id]
  subnet_id             = aws_subnet.public.id

  user_data = file("${path.module}/user-data.sh")

  tags = {
    Name = "${var.app_name}-web"
    Environment = var.environment
  }
}

# RDS Database
resource "aws_db_subnet_group" "main" {
  name       = "${var.app_name}-db-subnet-group"
  subnet_ids = [aws_subnet.public.id, aws_subnet.private.id]

  tags = {
    Name = "${var.app_name}-db-subnet-group"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.region}b"

  tags = {
    Name = "${var.app_name}-private-subnet"
  }
}

resource "aws_security_group" "rds" {
  name_prefix = "${var.app_name}-rds"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  tags = {
    Name = "${var.app_name}-rds-sg"
  }
}

resource "aws_db_instance" "main" {
  identifier     = "${var.app_name}-db"
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = var.db_instance_class
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    Name = "${var.app_name}-db"
    Environment = var.environment
  }
}
'''
        
        return resources
    
    def generate_kubernetes_resources(self, request: InfrastructureRequest) -> str:
        """Generate Kubernetes cluster resources"""
        provider = request.cloud_provider.value
        resources = ""
        
        if provider == "gcp":
            resources += '''
# GKE Cluster
resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.region

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  # Enable network policy
  network_policy {
    enabled = true
  }

  # Enable IP aliasing
  ip_allocation_policy {}

  # Enable workload identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Enable logging and monitoring
  logging_service    = "logging.googleapis.com/kubernetes"
  monitoring_service = "monitoring.googleapis.com/kubernetes"
}

# Separately Managed Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "${google_container_cluster.primary.name}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  node_config {
    preemptible  = var.preemptible
    machine_type = var.machine_type

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.kubernetes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      env = var.environment
    }

    tags = ["gke-node", "${var.cluster_name}-node"]
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}

# VPC
resource "google_compute_network" "vpc" {
  name                    = "${var.cluster_name}-vpc"
  auto_create_subnetworks = "false"
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.cluster_name}-subnet"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.10.0.0/24"
}

# Service Account
resource "google_service_account" "kubernetes" {
  account_id = "${var.cluster_name}-sa"
}
'''
        
        elif provider == "aws":
            resources += '''
# EKS Cluster
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids = aws_subnet.private[*].id
  }

  depends_on = [
    aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy,
  ]
}

# EKS Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.cluster_name}-nodes"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = aws_subnet.private[*].id

  scaling_config {
    desired_size = var.desired_capacity
    max_size     = var.max_capacity
    min_size     = var.min_capacity
  }

  instance_types = var.instance_types

  depends_on = [
    aws_iam_role_policy_attachment.node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_AmazonEC2ContainerRegistryReadOnly,
  ]
}

# IAM Role for EKS Cluster
resource "aws_iam_role" "cluster" {
  name = "${var.cluster_name}-cluster-role"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "cluster_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster.name
}

# IAM Role for EKS Node Group
resource "aws_iam_role" "node" {
  name = "${var.cluster_name}-node-role"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "node_AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.node.name
}

resource "aws_iam_role_policy_attachment" "node_AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.node.name
}

resource "aws_iam_role_policy_attachment" "node_AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.node.name
}
'''
        
        return resources
    
    def generate_database_resources(self, request: InfrastructureRequest) -> str:
        """Generate database resources"""
        provider = request.cloud_provider.value
        db_engine = request.requirements.get('engine', 'postgresql')
        
        if provider == "gcp":
            return f'''
# Cloud SQL Instance
resource "google_sql_database_instance" "main" {{
  name             = var.db_instance_name
  database_version = "{db_engine.upper()}_13"
  region           = var.region

  settings {{
    tier = var.db_tier
    
    backup_configuration {{
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      backup_retention_settings {{
        retained_backups = 7
      }}
    }}
    
    ip_configuration {{
      ipv4_enabled = true
      require_ssl  = true
    }}
    
    database_flags {{
      name  = "log_statement"
      value = "all"
    }}
  }}

  deletion_protection = var.deletion_protection
}}

resource "google_sql_database" "database" {{
  name     = var.db_name
  instance = google_sql_database_instance.main.name
}}

resource "google_sql_user" "user" {{
  name     = var.db_username
  instance = google_sql_database_instance.main.name
  password = var.db_password
}}
'''
        
        elif provider == "aws":
            return f'''
# RDS Instance
resource "aws_db_instance" "main" {{
  identifier = var.db_instance_name
  
  engine         = "{db_engine}"
  engine_version = var.db_version
  instance_class = var.db_instance_class
  
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = var.backup_retention_period
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql"]
  
  skip_final_snapshot = !var.final_snapshot
  deletion_protection = var.deletion_protection

  tags = {{
    Name = var.db_instance_name
    Environment = var.environment
  }}
}}
'''
        
        return ""
    
    def generate_serverless_resources(self, request: InfrastructureRequest) -> str:
        """Generate serverless resources"""
        provider = request.cloud_provider.value
        
        if provider == "gcp":
            return '''
# Cloud Functions
resource "google_cloudfunctions_function" "function" {
  name        = var.function_name
  description = var.function_description
  runtime     = var.runtime

  available_memory_mb   = var.memory
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.zip.name
  trigger {
    http_trigger {
      url = var.trigger_url
    }
  }

  entry_point = var.entry_point
}

# Storage bucket for function source
resource "google_storage_bucket" "bucket" {
  name = "${var.function_name}-source"
}

resource "google_storage_bucket_object" "zip" {
  name   = "source.zip"
  bucket = google_storage_bucket.bucket.name
  source = var.source_zip_path
}
'''
        
        elif provider == "aws":
            return '''
# Lambda Function
resource "aws_lambda_function" "main" {
  filename      = var.lambda_zip_path
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  handler       = var.handler
  runtime       = var.runtime

  source_code_hash = filebase64sha256(var.lambda_zip_path)

  environment {
    variables = var.environment_variables
  }
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# API Gateway
resource "aws_api_gateway_rest_api" "main" {
  name        = "${var.function_name}-api"
  description = "API for ${var.function_name}"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_method.proxy.resource_id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.main.invoke_arn
}

resource "aws_api_gateway_deployment" "main" {
  depends_on = [
    aws_api_gateway_integration.lambda,
  ]

  rest_api_id = aws_api_gateway_rest_api.main.id
  stage_name  = "prod"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}
'''
        
        return ""
    
    def generate_variables_tf(self, request: InfrastructureRequest) -> str:
        """Generate variables.tf file"""
        variables = {
            "project_id": {"description": "GCP Project ID", "type": "string"},
            "region": {"description": "Region", "type": "string", "default": request.region},
            "zone": {"description": "Zone", "type": "string", "default": f"{request.region}-a"},
            "environment": {"description": "Environment", "type": "string", "default": request.environment},
            "app_name": {"description": "Application name", "type": "string", "default": request.name}
        }
        
        # Add infrastructure-specific variables
        if request.infrastructure_type == InfrastructureType.WEB_APP:
            variables.update({
                "machine_type": {"description": "Machine type", "type": "string", "default": "e2-medium"},
                "disk_size_gb": {"description": "Disk size in GB", "type": "number", "default": 20},
                "db_tier": {"description": "Database tier", "type": "string", "default": "db-f1-micro"},
                "db_name": {"description": "Database name", "type": "string"},
                "db_username": {"description": "Database username", "type": "string"},
                "db_password": {"description": "Database password", "type": "string", "sensitive": True}
            })
        
        elif request.infrastructure_type == InfrastructureType.KUBERNETES:
            variables.update({
                "cluster_name": {"description": "Kubernetes cluster name", "type": "string"},
                "node_count": {"description": "Number of nodes", "type": "number", "default": 2},
                "machine_type": {"description": "Node machine type", "type": "string", "default": "e2-medium"},
                "preemptible": {"description": "Use preemptible nodes", "type": "bool", "default": True}
            })
        
        # Convert to HCL format
        variables_hcl = ""
        for var_name, var_config in variables.items():
            variables_hcl += f'''
variable "{var_name}" {{
  description = "{var_config['description']}"
  type        = {var_config['type']}
'''
            if 'default' in var_config:
                if var_config['type'] == 'string':
                    variables_hcl += f'  default     = "{var_config["default"]}"\n'
                else:
                    variables_hcl += f'  default     = {str(var_config["default"]).lower()}\n'
            
            if var_config.get('sensitive'):
                variables_hcl += '  sensitive   = true\n'
            
            variables_hcl += '}\n'
        
        return variables_hcl
    
    def generate_outputs_tf(self, request: InfrastructureRequest) -> str:
        """Generate outputs.tf file"""
        outputs = {}
        
        if request.infrastructure_type == InfrastructureType.WEB_APP:
            if request.cloud_provider == CloudProvider.GCP:
                outputs = {
                    "instance_ip": {
                        "description": "Public IP of the web server",
                        "value": "google_compute_instance.web_server.network_interface[0].access_config[0].nat_ip"
                    },
                    "load_balancer_ip": {
                        "description": "Load balancer IP",
                        "value": "google_compute_global_address.default.address"
                    },
                    "database_connection": {
                        "description": "Database connection string",
                        "value": "google_sql_database_instance.main.connection_name",
                        "sensitive": True
                    }
                }
            elif request.cloud_provider == CloudProvider.AWS:
                outputs = {
                    "instance_ip": {
                        "description": "Public IP of the web server",
                        "value": "aws_instance.web.public_ip"
                    },
                    "database_endpoint": {
                        "description": "Database endpoint",
                        "value": "aws_db_instance.main.endpoint",
                        "sensitive": True
                    }
                }
        
        elif request.infrastructure_type == InfrastructureType.KUBERNETES:
            if request.cloud_provider == CloudProvider.GCP:
                outputs = {
                    "cluster_name": {
                        "description": "GKE cluster name",
                        "value": "google_container_cluster.primary.name"
                    },
                    "cluster_endpoint": {
                        "description": "GKE cluster endpoint",
                        "value": "google_container_cluster.primary.endpoint",
                        "sensitive": True
                    },
                    "cluster_ca_certificate": {
                        "description": "GKE cluster CA certificate",
                        "value": "google_container_cluster.primary.master_auth[0].cluster_ca_certificate",
                        "sensitive": True
                    }
                }
            elif request.cloud_provider == CloudProvider.AWS:
                outputs = {
                    "cluster_name": {
                        "description": "EKS cluster name",
                        "value": "aws_eks_cluster.main.name"
                    },
                    "cluster_endpoint": {
                        "description": "EKS cluster endpoint",
                        "value": "aws_eks_cluster.main.endpoint",
                        "sensitive": True
                    },
                    "cluster_ca_certificate": {
                        "description": "EKS cluster CA certificate",
                        "value": "aws_eks_cluster.main.certificate_authority[0].data",
                        "sensitive": True
                    }
                }
        
        # Convert to HCL format
        outputs_hcl = ""
        for output_name, output_config in outputs.items():
            outputs_hcl += f'''
output "{output_name}" {{
  description = "{output_config['description']}"
  value       = {output_config['value']}
'''
            if output_config.get('sensitive'):
                outputs_hcl += '  sensitive   = true\n'
            
            outputs_hcl += '}\n'
        
        return outputs_hcl
    
    def generate_tfvars(self, request: InfrastructureRequest) -> str:
        """Generate terraform.tfvars file"""
        tfvars = f'''# Terraform variables for {request.name}
region      = "{request.region}"
environment = "{request.environment}"
app_name    = "{request.name}"
'''
        
        # Add infrastructure-specific variables
        if request.infrastructure_type == InfrastructureType.WEB_APP:
            tfvars += f'''
# Database configuration
db_name     = "{request.name.replace('-', '_')}_db"
db_username = "app_user"
# db_password = "CHANGE_ME_IN_PRODUCTION"
'''
        
        elif request.infrastructure_type == InfrastructureType.KUBERNETES:
            tfvars += f'''
# Kubernetes configuration
cluster_name = "{request.name}-cluster"
node_count   = 2
machine_type = "e2-medium"
preemptible  = true
'''
        
        return tfvars
    
    def generate_versions_tf(self, request: InfrastructureRequest) -> str:
        """Generate versions.tf file"""
        return '''terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
'''
    
    def dict_to_hcl(self, data: Dict, indent: int = 0) -> str:
        """Convert dictionary to HCL format"""
        hcl = ""
        indent_str = "  " * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                hcl += f"{indent_str}{key} {{\n"
                hcl += self.dict_to_hcl(value, indent + 1)
                hcl += f"{indent_str}}}\n"
            elif isinstance(value, list):
                hcl += f"{indent_str}{key} = [\n"
                for item in value:
                    if isinstance(item, str):
                        hcl += f"{indent_str}  \"{item}\",\n"
                    else:
                        hcl += f"{indent_str}  {item},\n"
                hcl += f"{indent_str}]\n"
            elif isinstance(value, str):
                hcl += f"{indent_str}{key} = \"{value}\"\n"
            elif isinstance(value, bool):
                hcl += f"{indent_str}{key} = {str(value).lower()}\n"
            else:
                hcl += f"{indent_str}{key} = {value}\n"
        
        return hcl

class TerraformDeployer:
    """Deploy and manage Terraform configurations"""
    
    def __init__(self, work_dir: str = "/tmp/terraform"):
        self.work_dir = work_dir
        self.deployments = {}
        os.makedirs(work_dir, exist_ok=True)
    
    async def deploy_infrastructure(self, request: InfrastructureRequest, config_files: Dict[str, str]) -> Dict[str, Any]:
        """Deploy infrastructure using Terraform"""
        deployment_id = hashlib.md5(f"{request.id}_{time.time()}".encode()).hexdigest()[:8]
        deployment_dir = os.path.join(self.work_dir, deployment_id)
        
        try:
            # Create deployment directory
            os.makedirs(deployment_dir, exist_ok=True)
            
            # Write configuration files
            for filename, content in config_files.items():
                file_path = os.path.join(deployment_dir, filename)
                with open(file_path, 'w') as f:
                    f.write(content)
            
            # Initialize Terraform
            await self.run_terraform_command(deployment_dir, ["init"])
            
            # Plan deployment
            plan_result = await self.run_terraform_command(deployment_dir, ["plan", "-out=tfplan"])
            
            # Apply deployment
            apply_result = await self.run_terraform_command(deployment_dir, ["apply", "tfplan"])
            
            # Get outputs
            outputs = await self.get_terraform_outputs(deployment_dir)
            
            # Store deployment info
            self.deployments[deployment_id] = {
                'id': deployment_id,
                'request': request,
                'directory': deployment_dir,
                'status': 'deployed',
                'outputs': outputs,
                'deployed_at': datetime.now()
            }
            
            logger.info(f"Infrastructure deployed successfully: {deployment_id}")
            
            return {
                'deployment_id': deployment_id,
                'status': 'success',
                'outputs': outputs,
                'plan_result': plan_result,
                'apply_result': apply_result
            }
            
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return {
                'deployment_id': deployment_id,
                'status': 'failed',
                'error': str(e)
            }
    
    async def run_terraform_command(self, work_dir: str, args: List[str]) -> str:
        """Run Terraform command"""
        cmd = ["terraform"] + args
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=work_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"Terraform command failed: {stderr.decode()}")
        
        return stdout.decode()
    
    async def get_terraform_outputs(self, work_dir: str) -> Dict[str, Any]:
        """Get Terraform outputs"""
        try:
            output = await self.run_terraform_command(work_dir, ["output", "-json"])
            return json.loads(output)
        except Exception as e:
            logger.warning(f"Failed to get outputs: {e}")
            return {}
    
    async def destroy_infrastructure(self, deployment_id: str) -> Dict[str, Any]:
        """Destroy infrastructure"""
        if deployment_id not in self.deployments:
            return {'status': 'error', 'message': 'Deployment not found'}
        
        deployment = self.deployments[deployment_id]
        
        try:
            # Run terraform destroy
            result = await self.run_terraform_command(
                deployment['directory'], 
                ["destroy", "-auto-approve"]
            )
            
            # Update deployment status
            deployment['status'] = 'destroyed'
            deployment['destroyed_at'] = datetime.now()
            
            logger.info(f"Infrastructure destroyed: {deployment_id}")
            
            return {
                'deployment_id': deployment_id,
                'status': 'success',
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Destroy failed: {e}")
            return {
                'deployment_id': deployment_id,
                'status': 'failed',
                'error': str(e)
            }

class TerraformArchitect:
    """Main Terraform Architect system"""
    
    def __init__(self):
        self.generator = TerraformGenerator()
        self.deployer = TerraformDeployer()
        self.active_requests = {}
        self.deployment_history = []
    
    async def create_infrastructure(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create infrastructure from request"""
        # Create infrastructure request
        request = InfrastructureRequest(
            id=hashlib.md5(f"{request_data['name']}_{time.time()}".encode()).hexdigest()[:8],
            name=request_data['name'],
            description=request_data.get('description', ''),
            cloud_provider=CloudProvider(request_data['cloud_provider']),
            infrastructure_type=InfrastructureType(request_data['infrastructure_type']),
            requirements=request_data.get('requirements', {}),
            budget_limit=request_data.get('budget_limit', 1000.0),
            region=request_data.get('region', 'us-central1'),
            environment=request_data.get('environment', 'dev'),
            created_at=datetime.now()
        )
        
        # Store request
        self.active_requests[request.id] = request
        
        # Generate Terraform configuration
        config_files = self.generator.generate_terraform_config(request)
        
        # Deploy infrastructure
        deployment_result = await self.deployer.deploy_infrastructure(request, config_files)
        
        # Store in history
        self.deployment_history.append({
            'request': request,
            'deployment_result': deployment_result,
            'timestamp': datetime.now()
        })
        
        return {
            'request_id': request.id,
            'deployment_result': deployment_result,
            'config_files': list(config_files.keys())
        }
    
    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get deployment status"""
        if deployment_id in self.deployer.deployments:
            deployment = self.deployer.deployments[deployment_id]
            return {
                'deployment_id': deployment_id,
                'status': deployment['status'],
                'outputs': deployment.get('outputs', {}),
                'deployed_at': deployment.get('deployed_at'),
                'destroyed_at': deployment.get('destroyed_at')
            }
        
        return {'status': 'not_found'}
    
    def list_deployments(self) -> List[Dict[str, Any]]:
        """List all deployments"""
        deployments = []
        for deployment_id, deployment in self.deployer.deployments.items():
            deployments.append({
                'deployment_id': deployment_id,
                'name': deployment['request'].name,
                'cloud_provider': deployment['request'].cloud_provider.value,
                'infrastructure_type': deployment['request'].infrastructure_type.value,
                'status': deployment['status'],
                'deployed_at': deployment.get('deployed_at')
            })
        
        return deployments

# Example usage
if __name__ == "__main__":
    print("🏗️ TERRAFORM ARCHITECT BRAIN")
    print("============================")
    print("Multi-Cloud Infrastructure Automation")
    print("- Google Cloud Platform")
    print("- Amazon Web Services") 
    print("- Microsoft Azure")
    print("- Automated Terraform Generation")
    print("- Infrastructure as Code")
    print()
    
    # Initialize Terraform Architect
    architect = TerraformArchitect()
    
    # Example infrastructure request
    example_request = {
        'name': 'my-web-app',
        'description': 'Production web application',
        'cloud_provider': 'gcp',
        'infrastructure_type': 'web_app',
        'requirements': {
            'high_availability': True,
            'auto_scaling': True,
            'ssl_certificate': True
        },
        'budget_limit': 500.0,
        'region': 'us-central1',
        'environment': 'prod'
    }
    
    print("🏗️ Example Infrastructure Request:")
    print(json.dumps(example_request, indent=2))
    print()
    print("Use architect.create_infrastructure(request) to deploy!")