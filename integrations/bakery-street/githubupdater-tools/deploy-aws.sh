#!/bin/bash
# AWS Deployment Script for Poly-AI Framework

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Configuration
STACK_NAME="poly-ai-framework"
REGION="us-east-1"
ECR_REPOSITORY="poly-ai-framework"
IMAGE_TAG="latest"

print_header "🚀 Poly-AI Framework AWS Deployment"
echo "Stack Name: $STACK_NAME"
echo "Region: $REGION"
echo "ECR Repository: $ECR_REPOSITORY"
echo ""

# Check prerequisites
check_prerequisites() {
    print_header "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    # Check GitHub token
    if [ -z "$GITHUB_TOKEN" ]; then
        print_error "GITHUB_TOKEN environment variable is not set."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials not configured. Run 'aws configure' first."
        exit 1
    fi
    
    print_status "All prerequisites met!"
}

# Create ECR repository
create_ecr_repository() {
    print_header "Creating ECR repository..."
    
    # Check if repository exists
    if aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $REGION &> /dev/null; then
        print_warning "ECR repository $ECR_REPOSITORY already exists"
    else
        aws ecr create-repository --repository-name $ECR_REPOSITORY --region $REGION
        print_status "ECR repository created: $ECR_REPOSITORY"
    fi
    
    # Get login token
    aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
    print_status "Logged in to ECR"
}

# Build and push Docker image
build_and_push_image() {
    print_header "Building and pushing Docker image..."
    
    # Get AWS account ID
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG"
    
    # Build Docker image
    print_status "Building Docker image..."
    docker build -t $ECR_REPOSITORY:$IMAGE_TAG .
    
    # Tag for ECR
    docker tag $ECR_REPOSITORY:$IMAGE_TAG $ECR_URI
    
    # Push to ECR
    print_status "Pushing image to ECR..."
    docker push $ECR_URI
    
    print_status "Image pushed successfully: $ECR_URI"
}

# Deploy CloudFormation stack
deploy_cloudformation() {
    print_header "Deploying CloudFormation stack..."
    
    # Check if stack exists
    if aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION &> /dev/null; then
        print_warning "Stack $STACK_NAME already exists. Updating..."
        OPERATION="update-stack"
    else
        print_status "Creating new stack: $STACK_NAME"
        OPERATION="create-stack"
    fi
    
    # Deploy stack
    aws cloudformation $OPERATION \
        --stack-name $STACK_NAME \
        --template-body file://aws-deployment.yml \
        --parameters ParameterKey=GitHubToken,ParameterValue=$GITHUB_TOKEN \
        --capabilities CAPABILITY_IAM \
        --region $REGION
    
    # Wait for stack completion
    print_status "Waiting for stack deployment to complete..."
    aws cloudformation wait stack-$OPERATION-complete --stack-name $STACK_NAME --region $REGION
    
    print_status "Stack deployment completed!"
}

# Get stack outputs
get_stack_outputs() {
    print_header "Getting stack outputs..."
    
    # Get load balancer URL
    LOAD_BALANCER_URL=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerURL`].OutputValue' \
        --output text)
    
    # Get database endpoint
    DATABASE_ENDPOINT=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`DatabaseEndpoint`].OutputValue' \
        --output text)
    
    # Get Redis endpoint
    REDIS_ENDPOINT=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`RedisEndpoint`].OutputValue' \
        --output text)
    
    print_status "Deployment completed successfully!"
    echo ""
    print_header "🎉 Poly-AI Framework is now running on AWS!"
    echo ""
    echo "📊 Deployment Information:"
    echo "  Load Balancer URL: $LOAD_BALANCER_URL"
    echo "  Database Endpoint: $DATABASE_ENDPOINT"
    echo "  Redis Endpoint: $REDIS_ENDPOINT"
    echo ""
    echo "🔗 Access your application at: $LOAD_BALANCER_URL"
    echo ""
    print_status "Next steps:"
    echo "  1. Test the application at the Load Balancer URL"
    echo "  2. Set up monitoring and alerts"
    echo "  3. Configure custom domain (optional)"
    echo "  4. Set up CI/CD pipeline for automatic deployments"
}

# Cleanup function
cleanup() {
    print_header "Cleaning up resources..."
    
    read -p "Are you sure you want to delete the stack? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION
        print_status "Stack deletion initiated. This may take several minutes."
    else
        print_status "Cleanup cancelled."
    fi
}

# Main deployment function
main() {
    case "${1:-deploy}" in
        "deploy")
            check_prerequisites
            create_ecr_repository
            build_and_push_image
            deploy_cloudformation
            get_stack_outputs
            ;;
        "cleanup")
            cleanup
            ;;
        "status")
            aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION
            ;;
        *)
            echo "Usage: $0 {deploy|cleanup|status}"
            echo ""
            echo "Commands:"
            echo "  deploy  - Deploy Poly-AI Framework to AWS (default)"
            echo "  cleanup - Delete the CloudFormation stack"
            echo "  status  - Show stack status and outputs"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
