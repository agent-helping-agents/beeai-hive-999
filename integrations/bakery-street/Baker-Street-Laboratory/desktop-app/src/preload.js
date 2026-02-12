const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // API Communication
  apiRequest: (method, endpoint, data) => 
    ipcRenderer.invoke('api-request', { method, endpoint, data }),
  
  // Settings Management
  getSetting: (key, defaultValue) => 
    ipcRenderer.invoke('get-setting', key, defaultValue),
  setSetting: (key, value) => 
    ipcRenderer.invoke('set-setting', key, value),
  
  // File System
  showSaveDialog: (options) => 
    ipcRenderer.invoke('show-save-dialog', options),
  showOpenDialog: (options) => 
    ipcRenderer.invoke('show-open-dialog', options),
  
  // Menu Events
  onMenuAction: (callback) => {
    ipcRenderer.on('menu-new-research', callback);
    ipcRenderer.on('menu-open-file', callback);
    ipcRenderer.on('menu-settings', callback);
    ipcRenderer.on('menu-conduct-research', callback);
    ipcRenderer.on('menu-view-reports', callback);
    ipcRenderer.on('menu-api-status', callback);
  },
  
  // App Events
  onAppBeforeQuit: (callback) => {
    ipcRenderer.on('app-before-quit', callback);
  },
  
  // Remove listeners
  removeAllListeners: (channel) => {
    ipcRenderer.removeAllListeners(channel);
  }
});

// Baker Street Laboratory specific API
contextBridge.exposeInMainWorld('bakerStreetAPI', {
  // Research Operations
  conductResearch: async (query, options = {}) => {
    return await ipcRenderer.invoke('api-request', {
      method: 'POST',
      endpoint: '/research/conduct',
      data: {
        query,
        output_dir: options.outputDir || 'research/desktop_output',
        data_sources: options.dataSources || ['wikipedia', 'arxiv', 'news'],
        max_results: options.maxResults || 10,
        language: options.language || 'en'
      }
    });
  },
  
  // Get Research Status
  getResearchStatus: async (sessionId) => {
    return await ipcRenderer.invoke('api-request', {
      method: 'GET',
      endpoint: `/research/status/${sessionId}`
    });
  },
  
  // System Health
  getSystemHealth: async () => {
    return await ipcRenderer.invoke('api-request', {
      method: 'GET',
      endpoint: '/system/health'
    });
  },
  
  // Reports Management
  listReports: async () => {
    return await ipcRenderer.invoke('api-request', {
      method: 'GET',
      endpoint: '/reports/list'
    });
  },
  
  getReport: async (reportId) => {
    return await ipcRenderer.invoke('api-request', {
      method: 'GET',
      endpoint: `/reports/${reportId}`
    });
  },
  
  // Data Sources
  getWikipediaData: async (query, maxResults = 5) => {
    return await ipcRenderer.invoke('api-request', {
      method: 'GET',
      endpoint: `/data/wikipedia/${encodeURIComponent(query)}?max_results=${maxResults}`
    });
  },
  
  getArxivData: async (query, maxResults = 5) => {
    return await ipcRenderer.invoke('api-request', {
      method: 'GET',
      endpoint: `/data/arxiv/${encodeURIComponent(query)}?max_results=${maxResults}`
    });
  },
  
  getNewsData: async (query, maxResults = 10) => {
    return await ipcRenderer.invoke('api-request', {
      method: 'GET',
      endpoint: `/data/news/${encodeURIComponent(query)}?max_results=${maxResults}`
    });
  }
});

// Psychedelic Visual Effects API
contextBridge.exposeInMainWorld('psychedelicAPI', {
  // Theme Management
  setTheme: async (themeName) => {
    return await ipcRenderer.invoke('set-setting', 'theme', themeName);
  },
  
  getTheme: async () => {
    return await ipcRenderer.invoke('get-setting', 'theme', 'detective');
  },
  
  // Animation Controls
  enableAnimations: async (enabled) => {
    return await ipcRenderer.invoke('set-setting', 'animations', enabled);
  },
  
  getAnimationsEnabled: async () => {
    return await ipcRenderer.invoke('get-setting', 'animations', true);
  },
  
  // Particle Effects
  setParticleIntensity: async (intensity) => {
    return await ipcRenderer.invoke('set-setting', 'particleIntensity', intensity);
  },
  
  getParticleIntensity: async () => {
    return await ipcRenderer.invoke('get-setting', 'particleIntensity', 'medium');
  }
});

// Utility functions
contextBridge.exposeInMainWorld('utils', {
  // Format date
  formatDate: (date) => {
    return new Date(date).toLocaleString();
  },
  
  // Generate UUID
  generateUUID: () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  },
  
  // Debounce function
  debounce: (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },
  
  // Sanitize HTML
  sanitizeHTML: (str) => {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
  }
});
