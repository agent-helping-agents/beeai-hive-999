// Baker Street Laboratory - API Client
// Handles communication with the research API backend

class APIClient {
    constructor(baseUrl = 'http://localhost:5000/api/v2') {
        this.baseUrl = baseUrl;
        this.timeout = 30000; // 30 seconds
    }

    async request(method, endpoint, data = null) {
        try {
            const config = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'BakerStreetLaboratory/1.0.0'
                }
            };

            if (data) {
                config.body = JSON.stringify(data);
            }

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);
            config.signal = controller.signal;

            const response = await fetch(`${this.baseUrl}${endpoint}`, config);
            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            return { success: true, data: result };

        } catch (error) {
            console.error('API Request Error:', error);
            return { 
                success: false, 
                error: error.message || 'Unknown error occurred' 
            };
        }
    }

    // Research Operations
    async conductResearch(query, options = {}) {
        return await this.request('POST', '/research/conduct', {
            query,
            output_dir: options.outputDir || 'research/desktop_output',
            data_sources: options.dataSources || ['wikipedia', 'arxiv', 'news'],
            max_results: options.maxResults || 10,
            language: options.language || 'en'
        });
    }

    async getResearchStatus(sessionId) {
        return await this.request('GET', `/research/status/${sessionId}`);
    }

    // System Operations
    async getSystemHealth() {
        return await this.request('GET', '/system/health');
    }

    async getSystemInfo() {
        return await this.request('GET', '/system/info');
    }

    // Reports Management
    async listReports() {
        return await this.request('GET', '/reports/list');
    }

    async getReport(reportId) {
        return await this.request('GET', `/reports/${reportId}`);
    }

    // Data Sources
    async getWikipediaData(query, maxResults = 5) {
        return await this.request('GET', `/data/wikipedia/${encodeURIComponent(query)}?max_results=${maxResults}`);
    }

    async getArxivData(query, maxResults = 5) {
        return await this.request('GET', `/data/arxiv/${encodeURIComponent(query)}?max_results=${maxResults}`);
    }

    async getNewsData(query, maxResults = 10) {
        return await this.request('GET', `/data/news/${encodeURIComponent(query)}?max_results=${maxResults}`);
    }

    // Ollama AI Operations
    async getOllamaModels() {
        return await this.request('GET', '/ollama/models');
    }

    async generateWithOllama(prompt, options = {}) {
        return await this.request('POST', '/ollama/generate', {
            prompt,
            model: options.model || 'llama3.2:latest',
            system_prompt: options.systemPrompt,
            temperature: options.temperature || 0.7,
            max_tokens: options.maxTokens || 2000
        });
    }

    async analyzeWithOllama(query, model = 'llama3.2:latest') {
        return await this.request('POST', '/ollama/analyze', {
            query,
            model
        });
    }

    async getOllamaHealth() {
        return await this.request('GET', '/ollama/health');
    }

    // Connection Testing
    async testConnection() {
        try {
            const result = await this.getSystemHealth();
            return result.success;
        } catch (error) {
            return false;
        }
    }

    // Update base URL
    setBaseUrl(url) {
        this.baseUrl = url;
    }

    // Set timeout
    setTimeout(ms) {
        this.timeout = ms;
    }
}
