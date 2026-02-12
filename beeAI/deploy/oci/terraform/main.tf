# Oracle Cloud Infrastructure Terraform Configuration for beeAI
# This creates a VM.Standard.A1.Flex instance with 2 OCPUs and 8GB RAM

terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 4.0.0"
    }
  }
}

provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

# Get availability domains
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

# Get the latest Ubuntu 22.04 image
data "oci_core_images" "ubuntu_image" {
  compartment_id           = var.compartment_id
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "22.04"
  shape                    = "VM.Standard.A1.Flex"
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

# Create VCN
resource "oci_core_vcn" "beeai_vcn" {
  compartment_id = var.compartment_id
  cidr_block     = "10.0.0.0/16"
  display_name   = "beeai-vcn"
  dns_label      = "beeai"
}

# Create Internet Gateway
resource "oci_core_internet_gateway" "beeai_igw" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.beeai_vcn.id
  display_name   = "beeai-internet-gateway"
}

# Create Route Table
resource "oci_core_route_table" "beeai_route_table" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.beeai_vcn.id
  display_name   = "beeai-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.beeai_igw.id
  }
}

# Create Security List
resource "oci_core_security_list" "beeai_security_list" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.beeai_vcn.id
  display_name   = "beeai-security-list"

  # Allow SSH
  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "0.0.0.0/0"
    description = "SSH"
    tcp_options {
      min = 22
      max = 22
    }
  }

  # Allow HTTP
  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "0.0.0.0/0"
    description = "HTTP"
    tcp_options {
      min = 80
      max = 80
    }
  }

  # Allow HTTPS
  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "0.0.0.0/0"
    description = "HTTPS"
    tcp_options {
      min = 443
      max = 443
    }
  }

  # Allow beeAI API
  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "0.0.0.0/0"
    description = "beeAI API"
    tcp_options {
      min = 22181
      max = 22181
    }
  }

  # Allow all outbound
  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
    description = "All outbound traffic"
  }
}

# Create Subnet
resource "oci_core_subnet" "beeai_subnet" {
  compartment_id      = var.compartment_id
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  vcn_id              = oci_core_vcn.beeai_vcn.id
  cidr_block          = "10.0.1.0/24"
  display_name        = "beeai-subnet"
  dns_label           = "beeai"
  route_table_id      = oci_core_route_table.beeai_route_table.id
  security_list_ids   = [oci_core_security_list.beeai_security_list.id]
}

# Create Compute Instance
resource "oci_core_instance" "beeai_instance" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_id
  display_name        = "beeai-server"
  shape               = "VM.Standard.A1.Flex"

  shape_config {
    ocpus         = 2
    memory_in_gbs = 8
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.beeai_subnet.id
    assign_public_ip = true
  }

  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.ubuntu_image.images[0].id
    boot_volume_size_in_gbs = 100
  }

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key_path)
  }

  freeform_tags = {
    "Project"   = "beeAI"
    "ManagedBy" = "Terraform"
  }
}

# Output the public IP
output "instance_public_ip" {
  value       = oci_core_instance.beeai_instance.public_ip
  description = "Public IP of the beeAI server"
}

output "ssh_command" {
  value       = "ssh ubuntu@${oci_core_instance.beeai_instance.public_ip}"
  description = "SSH command to connect to the instance"
}

output "api_endpoint" {
  value       = "http://${oci_core_instance.beeai_instance.public_ip}:22181"
  description = "beeAI API endpoint"
}
