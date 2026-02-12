# Universal Treasury Payment System

A comprehensive Kubernetes-ready payment processing system with REST API endpoints, webhook integration, and monitoring capabilities.

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│                        UNIVERSAL TREASURY PAYMENT SYSTEM                      │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────────────────────────────────┐
│             │    │             │    │                                     │
│   Client    ├───►│  Load       │    │                                     │
│  (Mobile/Web)│    │  Balancer  │───►│  Payment API (Kubernetes Pods)       │
│             │    │             │    │                                     │
└─────────────┘    └─────────────┘    └─────────────────────────────────────────┘
                                                      │
                                                      ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│                            WISE PAYMENT PLATFORM                              │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│                            WEBHOOK PROCESSING                                 │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

## API Endpoints

### Payment Processing
- `POST /api/v1/payments` - Create a new payment transaction
- `GET /api/v1/payments` - List all payment transactions
- `GET /api/v1/payments/{id}` - Get payment transaction details

### Health & Monitoring
- `GET /api/v1/health` - Health check endpoint

### Webhooks
- `POST /api/v1/webhooks/wise` - Wise webhook receiver

## Kubernetes Deployment

### Components
1. **Payment API Deployment** - 3 replicas for high availability
2. **Load Balancer Service** - Exposes API to external clients
3. **ConfigMap** - Configuration for payment processing
4. **Secrets** - Secure storage for API keys and credentials

### Deployment Steps

1. **Build Docker Image:**
```bash
cd universal-treasury
docker build -f Dockerfile.payment-api -t universal-treasury-payment-api:1.0.0 .
```

2. **Apply Kubernetes Configuration:**
```bash
kubectl apply -f kubernetes/payment-secrets.yaml
kubectl apply -f kubernetes/payment-configmap.yaml
kubectl apply -f kubernetes/payment-api-deployment.yaml
kubectl apply -f kubernetes/payment-api-service.yaml
```

3. **Verify Deployment:**
```bash
kubectl get pods -l app=payment-api
kubectl get services payment-api-service
kubectl logs -f <payment-api-pod-name>
```

## Configuration

### Environment Variables
- `WISE_API_KEY` - Wise API authentication key
- `WISE_CLIENT_ID` - Wise OAuth client ID
- `WISE_CLIENT_SECRET` - Wise OAuth client secret
- `ENVIRONMENT` - Deployment environment (development/production)

### ConfigMap Settings
- `log_level` - Logging verbosity (debug/info/warn/error)
- `payment_timeout` - Payment processing timeout in seconds
- `max_transaction_amount` - Maximum allowed transaction amount
- `supported_currencies` - Array of supported currency codes
- `webhook_secret` - Secret for webhook signature verification

## Payment Processing Flow

1. **Client Request** - Client sends payment request to API
2. **Validation** - API validates request parameters
3. **Transaction Creation** - Payment transaction is created with "pending" status
4. **Wise Integration** - API communicates with Wise platform
5. **Status Updates** - Transaction status updated via webhooks
6. **Completion** - Payment marked as "completed" when processed

## Webhook Processing

The system supports Wise webhook events:
- `transfer.state-change` - Payment status updates
- `recipient.created` - New recipient notifications

## Monitoring and Logging

### Built-in Logging
- Request/response logging with timestamps
- Payment processing duration tracking
- Error logging with stack traces

### Kubernetes Monitoring
- Liveness and readiness probes
- Resource usage metrics
- Pod health monitoring

## Testing

### Local Testing
```bash
# Start API server locally
go run main.go transactions serve

# Test health endpoint
curl http://localhost:8080/api/v1/health

# Create payment
curl -X POST http://localhost:8080/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.50, "currency": "USD", "source_account": "acc_123", "target_account": "acc_456", "description": "Test payment"}'
```

### Kubernetes Testing
```bash
# Port forward to access service locally
kubectl port-forward svc/payment-api-service 8080:80

# Test endpoints as above
```

## Security Considerations

1. **Secrets Management** - All sensitive data stored in Kubernetes Secrets
2. **TLS Termination** - Configure ingress controller for HTTPS
3. **Webhook Verification** - Validate webhook signatures
4. **Rate Limiting** - Implement API rate limiting
5. **Input Validation** - Validate all API inputs

## Scaling

The system is designed for horizontal scaling:
- Increase replicas in deployment for higher load
- Add resource requests/limits based on usage
- Implement auto-scaling based on CPU/memory usage

## Troubleshooting

### Common Issues

1. **Pods not starting** - Check logs with `kubectl logs <pod-name>`
2. **Connection refused** - Verify service is running and ports are correct
3. **API errors** - Check request format and authentication
4. **Webhook failures** - Verify webhook URL and signature

### Debugging Commands
```bash
# Check pod status
kubectl get pods -l app=payment-api

# View pod logs
kubectl logs -f <pod-name>

# Describe pod for details
kubectl describe pod <pod-name>

# Check service endpoints
kubectl get endpoints payment-api-service
```

## Future Enhancements

1. **Database Integration** - Add PostgreSQL for transaction persistence
2. **Caching Layer** - Implement Redis for performance optimization
3. **Advanced Monitoring** - Prometheus and Grafana integration
4. **Distributed Tracing** - Jaeger/OpenTelemetry integration
5. **Multi-currency Support** - Enhanced currency conversion
6. **Fraud Detection** - Machine learning-based fraud prevention