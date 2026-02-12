// Baker Street Laboratory - Main Application Logic
// Psychedelic Detective Desktop Application

class BakerStreetApp {
    constructor() {
        this.currentView = 'research';
        this.apiClient = new APIClient();
        this.uiManager = new UIManager();
        this.psychedelicEffects = new PsychedelicEffects();
        
        this.init();
    }

    async init() {
        console.log('🔬 Initializing Baker Street Laboratory Desktop App');
        
        // Initialize components
        await this.loadSettings();
        this.setupEventListeners();
        this.initializeUI();
        this.startBackgroundEffects();
        
        // Check API connection
        await this.checkAPIConnection();
        
        console.log('✅ Baker Street Laboratory initialized successfully');
    }

    async loadSettings() {
        try {
            // Load user preferences
            this.settings = {
                theme: await electronAPI.getSetting('theme', 'detective'),
                animations: await electronAPI.getSetting('animations', true),
                particleIntensity: await electronAPI.getSetting('particleIntensity', 'medium'),
                apiUrl: await electronAPI.getSetting('apiUrl', 'http://localhost:5000/api/v2'),
                autoSaveReports: await electronAPI.getSetting('autoSaveReports', true),
                ollamaModel: await electronAPI.getSetting('ollamaModel', 'llama3.2:latest'),
                aiTemperature: await electronAPI.getSetting('aiTemperature', 0.7)
            };
            
            // Apply settings
            this.applyTheme(this.settings.theme);
            this.psychedelicEffects.setParticleIntensity(this.settings.particleIntensity);
            
        } catch (error) {
            console.error('Failed to load settings:', error);
            this.showToast('Failed to load settings', 'error');
        }
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const view = e.currentTarget.dataset.view;
                this.switchView(view);
            });
        });

        // Research form
        const researchForm = document.getElementById('research-query');
        const conductBtn = document.getElementById('conduct-research-btn');
        
        if (researchForm && conductBtn) {
            researchForm.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.conductResearch();
                }
            });
            
            conductBtn.addEventListener('click', () => {
                this.conductResearch();
            });
        }

        // Settings
        const themeSelect = document.getElementById('theme-select');
        const animationsToggle = document.getElementById('animations-toggle');
        const particleIntensity = document.getElementById('particle-intensity');
        
        if (themeSelect) {
            themeSelect.value = this.settings.theme;
            themeSelect.addEventListener('change', (e) => {
                this.changeTheme(e.target.value);
            });
        }
        
        if (animationsToggle) {
            animationsToggle.checked = this.settings.animations;
            animationsToggle.addEventListener('change', (e) => {
                this.toggleAnimations(e.target.checked);
            });
        }
        
        if (particleIntensity) {
            particleIntensity.value = this.settings.particleIntensity;
            particleIntensity.addEventListener('change', (e) => {
                this.setParticleIntensity(e.target.value);
            });
        }

        // Quick actions
        const newResearchBtn = document.getElementById('new-research-btn');
        const recentReportsBtn = document.getElementById('recent-reports-btn');
        
        if (newResearchBtn) {
            newResearchBtn.addEventListener('click', () => {
                this.switchView('research');
                document.getElementById('research-query').focus();
            });
        }
        
        if (recentReportsBtn) {
            recentReportsBtn.addEventListener('click', () => {
                this.switchView('reports');
                this.loadReports();
            });
        }

        // Menu events from main process
        electronAPI.onMenuAction((event, data) => {
            this.handleMenuAction(event, data);
        });

        // API status check
        const testApiBtn = document.getElementById('test-api-btn');
        if (testApiBtn) {
            testApiBtn.addEventListener('click', () => {
                this.checkAPIConnection();
            });
        }

        // Ollama controls
        const testOllamaBtn = document.getElementById('test-ollama-btn');
        const refreshModelsBtn = document.getElementById('refresh-models-btn');
        const ollamaModelSelect = document.getElementById('ollama-model');
        const temperatureSlider = document.getElementById('ai-temperature');
        const temperatureValue = document.getElementById('temperature-value');

        if (testOllamaBtn) {
            testOllamaBtn.addEventListener('click', () => {
                this.testOllamaConnection();
            });
        }

        if (refreshModelsBtn) {
            refreshModelsBtn.addEventListener('click', () => {
                this.refreshOllamaModels();
            });
        }

        if (ollamaModelSelect) {
            ollamaModelSelect.addEventListener('change', (e) => {
                this.setOllamaModel(e.target.value);
            });
        }

        if (temperatureSlider && temperatureValue) {
            temperatureSlider.addEventListener('input', (e) => {
                temperatureValue.textContent = e.target.value;
                this.setAITemperature(parseFloat(e.target.value));
            });
        }

        // Data source testing
        document.querySelectorAll('.test-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const source = e.target.dataset.source;
                this.testDataSource(source);
            });
        });

        // Report modal
        const closeModalBtn = document.getElementById('close-report-modal');
        if (closeModalBtn) {
            closeModalBtn.addEventListener('click', () => {
                this.closeReportModal();
            });
        }

        // Theme toggle button
        const themeToggleBtn = document.getElementById('theme-toggle');
        if (themeToggleBtn) {
            themeToggleBtn.addEventListener('click', () => {
                this.cycleTheme();
            });
        }
    }

    initializeUI() {
        // Set initial view
        this.switchView(this.currentView);
        
        // Initialize tooltips and other UI components
        this.uiManager.initializeTooltips();
        
        // Load initial data
        this.loadReports();
        this.updateAnalytics();
        this.checkOllamaStatus();
    }

    startBackgroundEffects() {
        if (this.settings.animations) {
            this.psychedelicEffects.startParticles();
            this.psychedelicEffects.startBackgroundAnimation();
        }
    }

    switchView(viewName) {
        // Hide all views
        document.querySelectorAll('.view').forEach(view => {
            view.classList.remove('active');
        });
        
        // Show selected view
        const targetView = document.getElementById(`${viewName}-view`);
        if (targetView) {
            targetView.classList.add('active');
        }
        
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const activeNavItem = document.querySelector(`[data-view="${viewName}"]`);
        if (activeNavItem) {
            activeNavItem.classList.add('active');
        }
        
        this.currentView = viewName;
        
        // Load view-specific data
        this.loadViewData(viewName);
    }

    async loadViewData(viewName) {
        switch (viewName) {
            case 'reports':
                await this.loadReports();
                break;
            case 'data-sources':
                await this.checkDataSources();
                break;
            case 'analytics':
                await this.updateAnalytics();
                break;
            case 'settings':
                this.loadSettingsView();
                break;
        }
    }

    async conductResearch() {
        const queryInput = document.getElementById('research-query');
        const query = queryInput.value.trim();
        
        if (!query) {
            this.showToast('Please enter a research query', 'warning');
            return;
        }
        
        try {
            // Show progress
            this.showResearchProgress();
            
            // Get research options
            const dataSources = Array.from(document.querySelectorAll('input[name="data-source"]:checked'))
                .map(cb => cb.value);
            const maxResults = parseInt(document.getElementById('max-results').value);
            
            // Conduct research
            const result = await bakerStreetAPI.conductResearch(query, {
                dataSources,
                maxResults,
                outputDir: 'research/desktop_output'
            });
            
            if (result.success) {
                this.showResearchResults(result.data);
                this.showToast('Research completed successfully!', 'success');
            } else {
                throw new Error(result.error);
            }
            
        } catch (error) {
            console.error('Research failed:', error);
            this.showToast(`Research failed: ${error.message}`, 'error');
            this.hideResearchProgress();
        }
    }

    showResearchProgress() {
        const progressDiv = document.getElementById('research-progress');
        const resultsDiv = document.getElementById('research-results');
        
        if (progressDiv) progressDiv.classList.remove('hidden');
        if (resultsDiv) resultsDiv.classList.add('hidden');
        
        // Animate progress steps
        const steps = document.querySelectorAll('.progress-steps .step');
        steps.forEach((step, index) => {
            setTimeout(() => {
                step.classList.add('active');
            }, index * 1000);
        });
    }

    hideResearchProgress() {
        const progressDiv = document.getElementById('research-progress');
        if (progressDiv) progressDiv.classList.add('hidden');
        
        // Reset progress steps
        document.querySelectorAll('.progress-steps .step').forEach(step => {
            step.classList.remove('active');
        });
    }

    showResearchResults(data) {
        this.hideResearchProgress();
        
        const resultsDiv = document.getElementById('research-results');
        if (!resultsDiv) return;
        
        resultsDiv.classList.remove('hidden');
        
        // Update results content
        const sessionIdSpan = resultsDiv.querySelector('.session-id');
        const completionTimeSpan = resultsDiv.querySelector('.completion-time');
        const summaryDiv = resultsDiv.querySelector('.result-summary');
        
        if (sessionIdSpan) sessionIdSpan.textContent = `Session: ${data.session_id}`;
        if (completionTimeSpan) completionTimeSpan.textContent = `Completed: ${new Date(data.timestamp).toLocaleString()}`;
        if (summaryDiv) summaryDiv.textContent = data.summary || 'Research completed successfully';
        
        // Store current result for viewing/exporting
        this.currentResult = data;
    }

    async loadReports() {
        try {
            const result = await bakerStreetAPI.listReports();
            
            if (result.success) {
                this.displayReports(result.data.reports);
            } else {
                throw new Error(result.error);
            }
            
        } catch (error) {
            console.error('Failed to load reports:', error);
            this.showToast('Failed to load reports', 'error');
        }
    }

    displayReports(reports) {
        const reportsList = document.getElementById('reports-list');
        if (!reportsList) return;
        
        if (reports.length === 0) {
            reportsList.innerHTML = '<p class="no-reports">No reports found. Conduct some research to generate reports!</p>';
            return;
        }
        
        reportsList.innerHTML = reports.map(report => `
            <div class="report-card" data-report-id="${report.filename.replace('research_report_', '').replace('.md', '')}">
                <div class="report-header">
                    <h3>${report.filename}</h3>
                    <span class="report-date">${new Date(report.created).toLocaleDateString()}</span>
                </div>
                <div class="report-meta">
                    <span class="report-size">${(report.size / 1024).toFixed(1)} KB</span>
                </div>
                <div class="report-actions">
                    <button class="view-report-btn" data-report-id="${report.filename.replace('research_report_', '').replace('.md', '')}">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="export-report-btn" data-report-id="${report.filename.replace('research_report_', '').replace('.md', '')}">
                        <i class="fas fa-download"></i> Export
                    </button>
                </div>
            </div>
        `).join('');
        
        // Add event listeners to report buttons
        reportsList.querySelectorAll('.view-report-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const reportId = e.target.dataset.reportId;
                this.viewReport(reportId);
            });
        });
        
        reportsList.querySelectorAll('.export-report-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const reportId = e.target.dataset.reportId;
                this.exportReport(reportId);
            });
        });
    }

    async viewReport(reportId) {
        try {
            const result = await bakerStreetAPI.getReport(reportId);
            
            if (result.success) {
                this.showReportModal(result.data);
            } else {
                throw new Error(result.error);
            }
            
        } catch (error) {
            console.error('Failed to load report:', error);
            this.showToast('Failed to load report', 'error');
        }
    }

    showReportModal(reportData) {
        const modal = document.getElementById('report-modal');
        const content = document.getElementById('report-content');
        
        if (modal && content) {
            content.innerHTML = this.formatReportContent(reportData.content);
            modal.classList.remove('hidden');
        }
    }

    closeReportModal() {
        const modal = document.getElementById('report-modal');
        if (modal) {
            modal.classList.add('hidden');
        }
    }

    formatReportContent(markdown) {
        // Simple markdown to HTML conversion
        return markdown
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*)\*/gim, '<em>$1</em>')
            .replace(/\n/gim, '<br>');
    }

    async checkAPIConnection() {
        const statusIndicator = document.querySelector('.api-status .status-indicator');
        const statusText = document.querySelector('.api-status .status-text');
        
        try {
            const result = await bakerStreetAPI.getSystemHealth();
            
            if (result.success) {
                const health = result.data;
                statusIndicator.className = `fas fa-circle status-indicator ${health.status === 'healthy' ? 'healthy' : 'warning'}`;
                statusText.textContent = health.status === 'healthy' ? 'Connected' : 'Degraded';
                
                if (health.status === 'healthy') {
                    this.showToast('API connection healthy', 'success');
                }
            } else {
                throw new Error(result.error);
            }
            
        } catch (error) {
            console.error('API connection failed:', error);
            statusIndicator.className = 'fas fa-circle status-indicator error';
            statusText.textContent = 'Disconnected';
            this.showToast('API connection failed', 'error');
        }
    }

    async testDataSource(source) {
        const statusIndicator = document.getElementById(`${source}-status`);
        
        try {
            let result;
            switch (source) {
                case 'wikipedia':
                    result = await bakerStreetAPI.getWikipediaData('test', 1);
                    break;
                case 'arxiv':
                    result = await bakerStreetAPI.getArxivData('test', 1);
                    break;
                case 'news':
                    result = await bakerStreetAPI.getNewsData('test', 1);
                    break;
            }
            
            if (result.success) {
                statusIndicator.className = 'fas fa-circle healthy';
                this.showToast(`${source} connection successful`, 'success');
            } else {
                throw new Error(result.error);
            }
            
        } catch (error) {
            console.error(`${source} test failed:`, error);
            statusIndicator.className = 'fas fa-circle error';
            this.showToast(`${source} connection failed`, 'error');
        }
    }

    async updateAnalytics() {
        try {
            const reports = await bakerStreetAPI.listReports();
            
            if (reports.success) {
                const totalReports = reports.data.count;
                
                // Update analytics display
                const totalReportsEl = document.getElementById('total-reports');
                if (totalReportsEl) totalReportsEl.textContent = totalReports;
                
                // You can add more analytics here
            }
            
        } catch (error) {
            console.error('Failed to update analytics:', error);
        }
    }

    changeTheme(themeName) {
        this.settings.theme = themeName;
        electronAPI.setSetting('theme', themeName);
        this.applyTheme(themeName);
        this.showToast(`Theme changed to ${themeName}`, 'success');
    }

    applyTheme(themeName) {
        document.body.className = `${themeName}-theme`;
        this.psychedelicEffects.setTheme(themeName);
    }

    cycleTheme() {
        const themes = ['detective', 'laboratory', 'psychedelic'];
        const currentIndex = themes.indexOf(this.settings.theme);
        const nextIndex = (currentIndex + 1) % themes.length;
        this.changeTheme(themes[nextIndex]);
    }

    toggleAnimations(enabled) {
        this.settings.animations = enabled;
        electronAPI.setSetting('animations', enabled);
        
        if (enabled) {
            this.psychedelicEffects.startParticles();
            this.psychedelicEffects.startBackgroundAnimation();
        } else {
            this.psychedelicEffects.stopParticles();
            this.psychedelicEffects.stopBackgroundAnimation();
        }
        
        this.showToast(`Animations ${enabled ? 'enabled' : 'disabled'}`, 'success');
    }

    setParticleIntensity(intensity) {
        this.settings.particleIntensity = intensity;
        electronAPI.setSetting('particleIntensity', intensity);
        this.psychedelicEffects.setParticleIntensity(intensity);
        this.showToast(`Particle intensity set to ${intensity}`, 'success');
    }

    handleMenuAction(event, data) {
        switch (event) {
            case 'menu-new-research':
                this.switchView('research');
                document.getElementById('research-query').focus();
                break;
            case 'menu-conduct-research':
                this.conductResearch();
                break;
            case 'menu-view-reports':
                this.switchView('reports');
                break;
            case 'menu-settings':
                this.switchView('settings');
                break;
            case 'menu-api-status':
                this.checkAPIConnection();
                break;
            case 'menu-open-file':
                // Handle file opening
                break;
        }
    }

    showToast(message, type = 'info') {
        this.uiManager.showToast(message, type);
    }

    loadSettingsView() {
        // Update settings form with current values
        const themeSelect = document.getElementById('theme-select');
        const animationsToggle = document.getElementById('animations-toggle');
        const particleIntensity = document.getElementById('particle-intensity');
        const apiUrl = document.getElementById('api-url');
        const ollamaModel = document.getElementById('ollama-model');
        const aiTemperature = document.getElementById('ai-temperature');
        const temperatureValue = document.getElementById('temperature-value');

        if (themeSelect) themeSelect.value = this.settings.theme;
        if (animationsToggle) animationsToggle.checked = this.settings.animations;
        if (particleIntensity) particleIntensity.value = this.settings.particleIntensity;
        if (apiUrl) apiUrl.value = this.settings.apiUrl;
        if (ollamaModel) ollamaModel.value = this.settings.ollamaModel;
        if (aiTemperature) {
            aiTemperature.value = this.settings.aiTemperature;
            if (temperatureValue) temperatureValue.textContent = this.settings.aiTemperature;
        }
    }

    async exportReport(reportId) {
        try {
            const result = await electronAPI.showSaveDialog({
                title: 'Export Research Report',
                defaultPath: `research_report_${reportId}.md`,
                filters: [
                    { name: 'Markdown Files', extensions: ['md'] },
                    { name: 'Text Files', extensions: ['txt'] },
                    { name: 'All Files', extensions: ['*'] }
                ]
            });

            if (!result.canceled) {
                // In a full implementation, you would save the file here
                this.showToast('Report export functionality coming soon!', 'info');
            }

        } catch (error) {
            console.error('Export failed:', error);
            this.showToast('Export failed', 'error');
        }
    }

    // Ollama AI Integration Methods
    async checkOllamaStatus() {
        try {
            const result = await this.apiClient.getOllamaHealth();
            const statusDisplay = document.getElementById('ollama-status');

            if (result.success && statusDisplay) {
                const health = result.data;
                const statusText = statusDisplay.querySelector('.status-text');

                if (health.status === 'healthy') {
                    statusText.textContent = `Ollama: ${health.models_available || 0} models available`;
                    statusText.className = 'status-text healthy';
                } else if (health.status === 'degraded') {
                    statusText.textContent = 'Ollama: Connected but degraded';
                    statusText.className = 'status-text warning';
                } else {
                    statusText.textContent = 'Ollama: Not available';
                    statusText.className = 'status-text error';
                }
            }

            // Load available models
            await this.refreshOllamaModels();

        } catch (error) {
            console.error('Ollama status check failed:', error);
            const statusDisplay = document.getElementById('ollama-status');
            if (statusDisplay) {
                const statusText = statusDisplay.querySelector('.status-text');
                statusText.textContent = 'Ollama: Connection failed';
                statusText.className = 'status-text error';
            }
        }
    }

    async testOllamaConnection() {
        try {
            this.showToast('Testing Ollama connection...', 'info');

            const result = await this.apiClient.generateWithOllama(
                'Hello, this is a test message. Please respond briefly.',
                { model: this.settings.ollamaModel || 'llama3.2:latest' }
            );

            if (result.success) {
                this.showToast('Ollama connection successful!', 'success');
                console.log('Ollama test response:', result.data.response);
            } else {
                throw new Error(result.error || 'Unknown error');
            }

        } catch (error) {
            console.error('Ollama test failed:', error);
            this.showToast(`Ollama test failed: ${error.message}`, 'error');
        }
    }

    async refreshOllamaModels() {
        try {
            const result = await this.apiClient.getOllamaModels();

            if (result.success) {
                const modelSelect = document.getElementById('ollama-model');
                if (modelSelect) {
                    // Clear existing options
                    modelSelect.innerHTML = '';

                    // Add available models
                    const models = result.data.models || [];
                    const recommended = result.data.recommended || [];

                    if (models.length === 0) {
                        modelSelect.innerHTML = '<option value="">No models available</option>';
                        return;
                    }

                    // Add recommended models first
                    if (recommended.length > 0) {
                        const recommendedGroup = document.createElement('optgroup');
                        recommendedGroup.label = 'Recommended';

                        recommended.forEach(modelName => {
                            const option = document.createElement('option');
                            option.value = modelName;
                            option.textContent = modelName;
                            recommendedGroup.appendChild(option);
                        });

                        modelSelect.appendChild(recommendedGroup);
                    }

                    // Add all models
                    if (models.length > recommended.length) {
                        const allGroup = document.createElement('optgroup');
                        allGroup.label = 'All Models';

                        models.forEach(model => {
                            if (!recommended.includes(model.name)) {
                                const option = document.createElement('option');
                                option.value = model.name;
                                option.textContent = `${model.name} (${this.formatFileSize(model.size)})`;
                                allGroup.appendChild(option);
                            }
                        });

                        modelSelect.appendChild(allGroup);
                    }

                    // Set current selection
                    if (this.settings.ollamaModel) {
                        modelSelect.value = this.settings.ollamaModel;
                    }
                }

                this.showToast(`Found ${models.length} Ollama models`, 'success');
            } else {
                throw new Error(result.error || 'Failed to fetch models');
            }

        } catch (error) {
            console.error('Failed to refresh Ollama models:', error);
            this.showToast('Failed to refresh Ollama models', 'error');
        }
    }

    async setOllamaModel(modelName) {
        this.settings.ollamaModel = modelName;
        await electronAPI.setSetting('ollamaModel', modelName);
        this.showToast(`AI model set to ${modelName}`, 'success');
    }

    async setAITemperature(temperature) {
        this.settings.aiTemperature = temperature;
        await electronAPI.setSetting('aiTemperature', temperature);
    }

    formatFileSize(bytes) {
        if (!bytes) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BakerStreetApp();
});
