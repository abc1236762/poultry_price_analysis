'use strict';

import { app, protocol, BrowserWindow, Menu } from 'electron';
import {
  createProtocol,
  installVueDevtools,
} from 'vue-cli-plugin-electron-builder/lib';

const isDevelopment = process.env.NODE_ENV !== 'production';

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win;
const [contentWidth, contentHeight] = [360, 640];

// Scheme must be registered before the app is ready.
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } },
]);

function createWindow() {
  win = new BrowserWindow({
    width: contentWidth,
    height: contentHeight,
    useContentSize: true,
    center: true,
    show: false,
    webPreferences: {
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
    },
  });

  if (process.platform !== 'darwin') {
    win.removeMenu();
  } else {
    win.setMenu(Menu.buildFromTemplate([]));
  }

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    win.loadURL(process.env.WEBPACK_DEV_SERVER_URL);
    if (!process.env.IS_TEST) win.webContents.openDevTools({ mode: 'detach' });
  } else {
    createProtocol('app');
    // Load the index.html when not in development
    win.loadURL('app://./index.html');
  }

  win.once('ready-to-show', () => {
    if (win) {
      const bounds = win.getContentBounds();
      const [winWidth, winHeight] = win.getSize();
      const [widthErr, heightErr] = [
        bounds.width - contentWidth,
        bounds.height - contentHeight,
      ];
      win.setMinimumSize(winWidth - widthErr, winHeight - heightErr);
      bounds.x = Math.round(bounds.x + widthErr);
      bounds.y = Math.round(bounds.y + heightErr);
      bounds.width = contentWidth - widthErr;
      bounds.height = contentHeight - heightErr;
      win.setContentBounds(bounds);
      win.show();
    }
  });
  win.on('closed', () => {
    win = null;
  });
}

app.on('window-all-closed', () => {
  app.quit();
});

app.on('activate', () => {
  if (win === null) {
    createWindow();
  }
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installVueDevtools();
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString());
    }
  }
  createWindow();
});

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit();
      }
    });
  } else {
    process.on('SIGTERM', () => {
      app.quit();
    });
  }
}
