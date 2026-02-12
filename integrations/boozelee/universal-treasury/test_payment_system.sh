#!/bin/bash

# Universal Treasury Payment System Test Script
# This script tests the payment API functionality both locally and in Kubernetes

echo "🧪 Universal Treasury Payment System Test Suite"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_output="$3"
    
    echo -e "\n${YELLOW}📋 Running test: $test_name${NC}"
    
    # Execute the test command
    output=$(eval "$test_command" 2>&1)
    exit_code=$?
    
    # Check if expected output is provided and matches
    if [ -n "$expected_output" ]; then
        if echo "$output" | grep -q "$expected_output"; then
            echo -e "${GREEN}✅ PASS: $test_name${NC}"
            echo "Output: $output"
            ((PASSED++))
        else
            echo -e "${RED}❌ FAIL: $test_name${NC}"
            echo "Expected: $expected_output"
            echo "Got: $output"
            ((FAILED++))
        fi
    else
        if [ $exit_code -eq 0 ]; then
            echo -e "${GREEN}✅ PASS: $test_name${NC}"
            echo "Output: $output"
            ((PASSED++))
        else
            echo -e "${RED}❌ FAIL: $test_name${NC}"
            echo "Error: $output"
            ((FAILED++))
        fi
    fi
}

# Function to test local API
test_local_api() {
    echo -e "\n${YELLOW}🔧 Testing Local API Endpoints${NC}"
    
    # Start the API server in background
    echo "Starting payment API server..."
    go run main.go transactions serve &
    API_PID=$!
    
    # Wait for server to start
    sleep 3
    
    # Test health endpoint
    run_test "Health Check" "curl -s http://localhost:8080/api/v1/health" "healthy"
    
    # Test payment creation
    run_test "Create Payment" "curl -s -X POST http://localhost:8080/api/v1/payments \
        -H 'Content-Type: application/json' \
        -d '{\"amount\": 100.50, \"currency\": \"USD\", \"source_account\": \"acc_123\", \"target_account\": \"acc_456\", \"description\": \"Test payment\"}'" "Payment created successfully"
    
    # Test list payments
    run_test "List Payments" "curl -s http://localhost:8080/api/v1/payments" "100.50"
    
    # Test get specific payment
    run_test "Get Payment" "curl -s http://localhost:8080/api/v1/payments/1" "100.50"
    
    # Test webhook endpoint
    run_test "Webhook Endpoint" "curl -s -X POST http://localhost:8080/api/v1/webhooks/wise \
        -H 'Content-Type: application/json' \
        -d '{\"event_type\": \"transfer.state-change\", \"transfer_id\": \"tx_123\", \"state\": \"processing\"}'" "received"
    
    # Clean up
    kill $API_PID 2>/dev/null
    wait $API_PID 2>/dev/null
}

# Function to test Kubernetes deployment
test_kubernetes_deployment() {
    echo -e "\n${YELLOW}🚀 Testing Kubernetes Deployment${NC}"
    
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}⚠️  Skipping Kubernetes tests - kubectl not found${NC}"
        return
    fi
    
    # Check if we're connected to a cluster
    if ! kubectl cluster-info &> /dev/null; then
        echo -e "${RED}⚠️  Skipping Kubernetes tests - not connected to cluster${NC}"
        return
    fi
    
    echo "Testing Kubernetes deployment..."
    
    # Test deployment creation
    run_test "Create Deployment" "kubectl apply -f kubernetes/payment-api-deployment.yaml" "created"
    
    # Test service creation
    run_test "Create Service" "kubectl apply -f kubernetes/payment-api-service.yaml" "created"
    
    # Wait for pods to be ready
    echo "Waiting for pods to be ready..."
    sleep 10
    
    # Test pod status
    run_test "Pod Status" "kubectl get pods -l app=payment-api" "Running"
    
    # Test service status
    run_test "Service Status" "kubectl get service payment-api-service" "payment-api-service"
    
    # Test port forwarding
    echo "Setting up port forwarding..."
    kubectl port-forward svc/payment-api-service 8080:80 &
    PORT_FORWARD_PID=$!
    sleep 3
    
    # Test API through Kubernetes
    run_test "K8s Health Check" "curl -s http://localhost:8080/api/v1/health" "healthy"
    
    # Clean up port forwarding
    kill $PORT_FORWARD_PID 2>/dev/null
    wait $PORT_FORWARD_PID 2>/dev/null
    
    # Clean up Kubernetes resources
    echo "Cleaning up Kubernetes resources..."
    kubectl delete -f kubernetes/payment-api-service.yaml
    kubectl delete -f kubernetes/payment-api-deployment.yaml
}

# Function to test Docker build
test_docker_build() {
    echo -e "\n${YELLOW}🐳 Testing Docker Build${NC}"
    
    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}⚠️  Skipping Docker tests - docker not found${NC}"
        return
    fi
    
    # Test Docker build
    run_test "Docker Build" "docker build -f Dockerfile.payment-api -t universal-treasury-payment-api:test ." "Successfully built"
    
    # Test Docker image exists
    run_test "Docker Image" "docker images | grep universal-treasury-payment-api" "universal-treasury-payment-api"
    
    # Clean up
    docker rmi universal-treasury-payment-api:test 2>/dev/null
}

# Function to test configuration files
test_configuration() {
    echo -e "\n${YELLOW}📂 Testing Configuration Files${NC}"
    
    # Test Kubernetes YAML files
    run_test "Deployment YAML" "test -f kubernetes/payment-api-deployment.yaml && echo 'exists'" "exists"
    run_test "Service YAML" "test -f kubernetes/payment-api-service.yaml && echo 'exists'" "exists"
    run_test "ConfigMap YAML" "test -f kubernetes/payment-configmap.yaml && echo 'exists'" "exists"
    run_test "Secrets YAML" "test -f kubernetes/payment-secrets.yaml && echo 'exists'" "exists"
    
    # Test Dockerfile
    run_test "Payment Dockerfile" "test -f Dockerfile.payment-api && echo 'exists'" "exists"
    
    # Test Go files
    run_test "Transactions Command" "test -f cmd/transactions.go && echo 'exists'" "exists"
}

# Main test execution
main() {
    echo "Starting payment system tests..."
    
    # Test configuration files
    test_configuration
    
    # Test local API
    test_local_api
    
    # Test Docker build
    test_docker_build
    
    # Test Kubernetes deployment
    test_kubernetes_deployment
    
    # Summary
    echo -e "\n${YELLOW}📊 Test Summary${NC}"
    echo -e "${GREEN}✅ Passed: $PASSED${NC}"
    echo -e "${RED}❌ Failed: $FAILED${NC}"
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed! Payment system is working correctly.${NC}"
        exit 0
    else
        echo -e "${RED}💥 Some tests failed. Please check the output above.${NC}"
        exit 1
    fi
}

# Run main function
main