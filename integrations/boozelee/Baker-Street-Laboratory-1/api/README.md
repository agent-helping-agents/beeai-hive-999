# Baker Street Laboratory - REST API

🔬 **AI-Augmented Research Framework API**

The Baker Street Laboratory REST API provides programmatic access to the research orchestrator, enabling you to conduct research, monitor system health, and manage reports through HTTP endpoints.

## 🚀 Quick Start

### 1. Start the API Server
```bash
# From the project root directory
./api/start_api.sh
```

The API will be available at:
- **Base URL**: `http://localhost:5000`
- **API Endpoints**: `http://localhost:5000/api/v1/`
- **Documentation**: `http://localhost:5000/docs/`

### 2. Test the API
```bash
# Using curl
curl -X GET http://localhost:5000/api/v1/system/health

# Using the Python client
python3 api/client_example.py

# Using VSCodium REST Client extension
# Open api/test_api.http and click "Send Request"
```

## 📋 API Endpoints

### 🔍 Research Operations

#### Conduct Research
```http
POST /api/v1/research/conduct
Content-Type: application/json

{
    "query": "What is the meaning of life?",
    "output_dir": "research/api_output"
}
```

**Response:**
```json
{
    "session_id": "1a44a2d6",
    "query": "What is the meaning of life?",
    "status": "completed",
    "timestamp": "2025-08-03T08:57:37",
    "summary": "Research report generated successfully",
    "report_path": "research/research_report_1a44a2d6.md",
    "output_dir": "research/api_output"
}
```

#### Get Research Status
```http
GET /api/v1/research/status/{session_id}
```

### 🏥 System Operations

#### Health Check
```http
GET /api/v1/system/health
```

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-08-03T08:57:37",
    "components": {
        "environment": {...},
        "orchestrator": {...},
        "api": "running"
    },
    "version": "1.0.0"
}
```

#### System Information
```http
GET /api/v1/system/info
```

### 📄 Reports Management

#### List Reports
```http
GET /api/v1/reports/list
```

**Response:**
```json
{
    "reports": [
        {
            "filename": "research_report_1a44a2d6.md",
            "path": "research/research_report_1a44a2d6.md",
            "size": 5420,
            "created": "2025-08-03T08:57:37"
        }
    ],
    "count": 1,
    "timestamp": "2025-08-03T08:57:37"
}
```

#### Get Specific Report
```http
GET /api/v1/reports/{report_id}
```

## 🐍 Python Client Usage

```python
from api.client_example import BakerStreetClient

# Initialize client
client = BakerStreetClient("http://localhost:5000")

# Check system health
health = client.check_health()
print(f"System status: {health['status']}")

# Conduct research
result = client.conduct_research("What are the latest AI developments?")
print(f"Research completed: {result['session_id']}")

# Get report
reports = client.list_reports()
if reports['reports']:
    report_id = reports['reports'][0]['filename'].replace('research_report_', '').replace('.md', '')
    report = client.get_report(report_id)
    print(f"Report content: {report['content'][:200]}...")
```

## 🧪 Testing with VSCodium

1. **Install REST Client Extension** (already installed)
2. **Open** `api/test_api.http`
3. **Click** "Send Request" above any HTTP request
4. **View** responses in the right panel

### Example Test Requests:

```http
### Test System Health
GET http://localhost:5000/api/v1/system/health

### Conduct Research
POST http://localhost:5000/api/v1/research/conduct
Content-Type: application/json

{
    "query": "What are the ethical implications of AI?",
    "output_dir": "research/api_output"
}
```

## 🔧 Configuration

### Environment Variables
The API uses the same `.env` configuration as the main application:

```bash
# AI API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=true
```

### Custom Configuration
Modify `api/app.py` to customize:
- **Port**: Change `app.run(port=5000)`
- **CORS**: Modify `CORS(app)` settings
- **Logging**: Adjust `setup_logging(level="INFO")`

## 📊 API Features

### ✅ Implemented Features
- **Research Orchestration**: Full integration with research pipeline
- **System Health Monitoring**: Environment and component status
- **Report Management**: List and retrieve research reports
- **Error Handling**: Comprehensive error responses
- **CORS Support**: Cross-origin requests enabled
- **API Documentation**: Interactive Swagger/OpenAPI docs
- **Async Support**: Handles async research operations

### 🔄 Response Formats
All responses are JSON with consistent structure:

```json
{
    "status": "success|error",
    "data": {...},
    "timestamp": "ISO-8601-timestamp",
    "message": "Human-readable message"
}
```

### 🚨 Error Handling
```json
{
    "error": "Error description",
    "status_code": 400,
    "timestamp": "2025-08-03T08:57:37"
}
```

## 🔗 Integration Examples

### JavaScript/Web Frontend
```javascript
const API_BASE = 'http://localhost:5000/api/v1';

async function conductResearch(query) {
    const response = await fetch(`${API_BASE}/research/conduct`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    });
    return response.json();
}
```

### cURL Commands
```bash
# Health check
curl -X GET http://localhost:5000/api/v1/system/health

# Conduct research
curl -X POST http://localhost:5000/api/v1/research/conduct \
  -H "Content-Type: application/json" \
  -d '{"query": "What is quantum computing?"}'

# List reports
curl -X GET http://localhost:5000/api/v1/reports/list
```

## 🛠️ Development

### Adding New Endpoints
1. **Create namespace**: `new_ns = Namespace('new', description='New operations')`
2. **Add to API**: `api.add_namespace(new_ns)`
3. **Create resource**: `@new_ns.route('/endpoint')`
4. **Add documentation**: `@new_ns.doc('endpoint_description')`

### Custom Middleware
Add custom middleware in `api/app.py`:

```python
@app.before_request
def before_request():
    # Custom logic before each request
    pass

@app.after_request
def after_request(response):
    # Custom logic after each request
    return response
```

## 🔒 Security Considerations

- **API Keys**: Store in environment variables, never in code
- **CORS**: Configure appropriately for production
- **Rate Limiting**: Consider adding rate limiting for production
- **Authentication**: Add authentication for sensitive operations
- **Input Validation**: All inputs are validated and sanitized

## 📈 Next Steps

1. **Desktop Application**: Use this API as backend for Electron app
2. **Mobile Application**: Flutter app can consume these endpoints
3. **Web Dashboard**: Create React/Vue frontend
4. **Batch Operations**: Add batch research endpoints
5. **WebSocket Support**: Real-time research progress updates

---

**🔬 Ready to build amazing applications on top of Baker Street Laboratory!** 🚀
