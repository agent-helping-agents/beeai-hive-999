const { app, BrowserWindow, Menu, ipcMain, dialog, shell } = require('electron');
const { autoUpdater } = require('electron-updater');
const Store = require('electron-store');
const path = require('path');
const axios = require('axios');

// Initialize electron store for settings
const store = new Store();

// Keep a global reference of the window object
let mainWindow;
let splashWindow;

// API Configuration
const API_BASE_URL = store.get('apiUrl', 'http://localhost:5000/api/v2');

function createSplashWindow() {
  splashWindow = new BrowserWindow({
    width: 600,
    height: 400,
    frame: false,
    alwaysOnTop: true,
    transparent: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  splashWindow.loadFile(path.join(__dirname, 'splash.html'));
  
  splashWindow.on('closed', () => {
    splashWindow = null;
  });

  // Auto-close splash after 3 seconds
  setTimeout(() => {
    if (splashWindow) {
      splashWindow.close();
      createMainWindow();
    }
  }, 3000);
}

function createMainWindow() {
  // Create the browser window with psychedelic theme
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    show: false,
    icon: path.join(__dirname, '../assets/icon.png'),
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#1A0F08', // Dark detective background
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      webSecurity: true,
      allowRunningInsecureContent: false
    }
  });

  // Load the main application
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Focus on the window
    if (process.platform === 'darwin') {
      app.dock.show();
    }
    
    // Check for updates
    if (!process.env.NODE_ENV || process.env.NODE_ENV === 'production') {
      autoUpdater.checkForUpdatesAndNotify();
    }
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Development tools
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
    
    // Install React/Vue DevTools if available
    const { default: installExtension, REACT_DEVELOPER_TOOLS, VUEJS_DEVTOOLS } = require('electron-devtools-installer');
    
    installExtension([REACT_DEVELOPER_TOOLS, VUEJS_DEVTOOLS])
      .then((name) => console.log(`Added Extension: ${name}`))
      .catch((err) => console.log('An error occurred: ', err));
  }
}

// Create application menu
function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New Research',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('menu-new-research');
          }
        },
        {
          label: 'Open Report',
          accelerator: 'CmdOrCtrl+O',
          click: async () => {
            const result = await dialog.showOpenDialog(mainWindow, {
              properties: ['openFile'],
              filters: [
                { name: 'Markdown Files', extensions: ['md'] },
                { name: 'All Files', extensions: ['*'] }
              ]
            });
            
            if (!result.canceled) {
              mainWindow.webContents.send('menu-open-file', result.filePaths[0]);
            }
          }
        },
        { type: 'separator' },
        {
          label: 'Settings',
          accelerator: 'CmdOrCtrl+,',
          click: () => {
            mainWindow.webContents.send('menu-settings');
          }
        },
        { type: 'separator' },
        {
          role: 'quit'
        }
      ]
    },
    {
      label: 'Research',
      submenu: [
        {
          label: 'Conduct Research',
          accelerator: 'CmdOrCtrl+R',
          click: () => {
            mainWindow.webContents.send('menu-conduct-research');
          }
        },
        {
          label: 'View Reports',
          accelerator: 'CmdOrCtrl+Shift+R',
          click: () => {
            mainWindow.webContents.send('menu-view-reports');
          }
        },
        { type: 'separator' },
        {
          label: 'API Status',
          click: () => {
            mainWindow.webContents.send('menu-api-status');
          }
        }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Window',
      submenu: [
        { role: 'minimize' },
        { role: 'close' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About Baker Street Laboratory',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About Baker Street Laboratory',
              message: 'Baker Street Laboratory',
              detail: 'Psychedelic Detective-themed AI Research Framework\nVersion 1.0.0\n\nTraversing kaleidoscopic dreamscapes of knowledge with the methodical precision of the world\'s greatest detective.',
              buttons: ['OK']
            });
          }
        },
        {
          label: 'Documentation',
          click: () => {
            shell.openExternal('https://github.com/BoozeLee/Baker-Street-Laboratory');
          }
        }
      ]
    }
  ];

  // macOS specific menu adjustments
  if (process.platform === 'darwin') {
    template.unshift({
      label: app.getName(),
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideOthers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' }
      ]
    });

    // Window menu
    template[4].submenu = [
      { role: 'close' },
      { role: 'minimize' },
      { role: 'zoom' },
      { type: 'separator' },
      { role: 'front' }
    ];
  }

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// IPC Handlers
ipcMain.handle('api-request', async (event, { method, endpoint, data }) => {
  try {
    const config = {
      method,
      url: `${API_BASE_URL}${endpoint}`,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    if (data) {
      config.data = data;
    }

    const response = await axios(config);
    return { success: true, data: response.data };
  } catch (error) {
    console.error('API Request Error:', error);
    return { 
      success: false, 
      error: error.response?.data || error.message 
    };
  }
});

ipcMain.handle('get-setting', (event, key, defaultValue) => {
  return store.get(key, defaultValue);
});

ipcMain.handle('set-setting', (event, key, value) => {
  store.set(key, value);
  return true;
});

ipcMain.handle('show-save-dialog', async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, options);
  return result;
});

ipcMain.handle('show-open-dialog', async (event, options) => {
  const result = await dialog.showOpenDialog(mainWindow, options);
  return result;
});

// App event handlers
app.whenReady().then(() => {
  createSplashWindow();
  createMenu();
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  // Save any pending data
  if (mainWindow) {
    mainWindow.webContents.send('app-before-quit');
  }
});

// Auto-updater events
autoUpdater.on('checking-for-update', () => {
  console.log('Checking for update...');
});

autoUpdater.on('update-available', (info) => {
  console.log('Update available.');
  dialog.showMessageBox(mainWindow, {
    type: 'info',
    title: 'Update Available',
    message: 'A new version is available. It will be downloaded in the background.',
    buttons: ['OK']
  });
});

autoUpdater.on('update-not-available', (info) => {
  console.log('Update not available.');
});

autoUpdater.on('error', (err) => {
  console.log('Error in auto-updater. ' + err);
});

autoUpdater.on('download-progress', (progressObj) => {
  let log_message = "Download speed: " + progressObj.bytesPerSecond;
  log_message = log_message + ' - Downloaded ' + progressObj.percent + '%';
  log_message = log_message + ' (' + progressObj.transferred + "/" + progressObj.total + ')';
  console.log(log_message);
});

autoUpdater.on('update-downloaded', (info) => {
  console.log('Update downloaded');
  dialog.showMessageBox(mainWindow, {
    type: 'info',
    title: 'Update Ready',
    message: 'Update downloaded. The application will restart to apply the update.',
    buttons: ['Restart Now', 'Later']
  }).then((result) => {
    if (result.response === 0) {
      autoUpdater.quitAndInstall();
    }
  });
});

// Security: Prevent new window creation
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (event, navigationUrl) => {
    event.preventDefault();
    shell.openExternal(navigationUrl);
  });
});

// Handle certificate errors
app.on('certificate-error', (event, webContents, url, error, certificate, callback) => {
  if (url.startsWith('https://localhost') || url.startsWith('https://127.0.0.1')) {
    // Allow localhost certificates for development
    event.preventDefault();
    callback(true);
  } else {
    callback(false);
  }
});
