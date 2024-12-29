import storage from '../utils/storage';

const API_BASE_URL = "http://localhost:8000/api";

const DEBUG = true;
const debugLog = (message, data) => {
  if (DEBUG) {
    console.log(`[Background ${new Date().toISOString()}] ${message}`, data || '');
  }
};

// Keep service worker alive
let keepAliveInterval;

function startKeepAlive() {
  if (keepAliveInterval) clearInterval(keepAliveInterval);
  keepAliveInterval = setInterval(() => {
    chrome.runtime.getPlatformInfo(() => {
      debugLog('Keeping service worker alive');
    });
  }, 25 * 1000);
}

function stopKeepAlive() {
  if (keepAliveInterval) {
    clearInterval(keepAliveInterval);
    keepAliveInterval = null;
  }
}

// Handle notification clicks
chrome.notifications.onClicked.addListener((notificationId) => {
  if (notificationId === 'analysis-complete') {
    chrome.action.openPopup();
    chrome.notifications.clear(notificationId);
  }
});

// Optional: Handle installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});

chrome.runtime.onStartup.addListener(() => {
  console.log("Extension started");
});

// Debug logging for all messages
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  debugLog("Received message in background:", message);
  
  if (message.type === "ANALYZE_URL") {
    debugLog("Starting analysis with:", message);
    const { url, analysisType } = message;
    
    // Start analysis and keep service worker alive
    waitUntil(analyzeUrl(url, analysisType))
      .catch(error => {
        debugLog('Analysis error:', error);
      });
    
    return true; // Keep message channel open for async response
  }
});

const logToBackground = (message, data) => {
  console.log(`[${new Date().toISOString()}] ${message}`, data);
};

// Add this helper function
async function waitUntil(promise) {
  const keepAlive = setInterval(chrome.runtime.getPlatformInfo, 25 * 1000);
  try {
    return await promise;
  } finally {
    clearInterval(keepAlive);
  }
}

const API_ENDPOINTS = {
  genres: '/genres/url',
  moodThemes: '/mood-themes/url',
  tags: '/tags/url'
};

async function analyzeUrl(url, analysisType) {
  try {
    debugLog(`Starting ${analysisType} analysis for URL:`, url);
    startKeepAlive(); // Start keeping service worker alive
    
    await chrome.storage.local.set({ 
      [`${analysisType}Loading`]: true,
      [`${analysisType}Error`]: null,
      [`${analysisType}Results`]: null
    });

    const endpoint = API_ENDPOINTS[analysisType];
    const apiUrl = `${API_BASE_URL}${endpoint}?url=${encodeURIComponent(url)}`;
    
    debugLog('Fetching from:', apiUrl);
    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    debugLog(`Received ${analysisType} data:`, data);
    
    // Store results
    await chrome.storage.local.set({
      [`${analysisType}Results`]: data,
      [`${analysisType}Loading`]: false
    });

    stopKeepAlive(); // Stop keeping service worker alive
    return data;

  } catch (error) {
    debugLog(`Error in ${analysisType} analysis:`, error);
    
    await chrome.storage.local.set({
      [`${analysisType}Loading`]: false,
      [`${analysisType}Error`]: error.message
    });
    
    stopKeepAlive(); // Stop keeping service worker alive
    throw error;
  }
}

async function analyzeAudioUrl(url) {
  try {
    await chrome.storage.local.set({ 
      analysisLoading: true, 
      error: null
    });

    // Create the promise first
    const analysisPromise = async () => {
      const apiUrl = `${API_BASE_URL}/genres/url?url=${encodeURIComponent(url)}`;
      const response = await fetch(apiUrl);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Format and store results
      const formattedData = {
        genres: data.genres.discogs400
      };

      // Store results
      await chrome.storage.local.set({
        analysisResults: formattedData,
        analysisLoading: false,
        lastUpdated: Date.now()
      });

      // Show notification
      chrome.notifications.create('analysis-complete', {
        type: 'basic',
        iconUrl: chrome.runtime.getURL('assets/audafact-temp.png'),
        title: 'Analysis Complete! 🎵',
        message: 'Click to view your results!',
        priority: 2,
        requireInteraction: true
      });
    };

    // Then pass the promise to waitUntil
    await waitUntil(analysisPromise());

  } catch (error) {
    await chrome.storage.local.set({
      analysisLoading: false,
      error: error.message,
      analysisResults: null
    });
    
    chrome.notifications.create('analysis-error', {
      type: 'basic',
      iconUrl: chrome.runtime.getURL('assets/audafact-temp.png'),
      title: 'Analysis Failed',
      message: 'There was an error analyzing the track.',
      priority: 2
    });
    
    throw error;
  }
}

async function broadcastResults(data) {
  try {
    debugLog("Broadcasting results:", data);

    const formattedData = {
      genres: data.genres.discogs400,
    };

    // Try to send to popup
    try {
      await chrome.runtime.sendMessage({
        type: "ANALYSIS_RESULTS",
        data: formattedData,
      });
      debugLog("Results sent to popup");
    } catch (err) {
      debugLog("Popup is closed, results already stored in storage");
    }

    // Show notification
    chrome.notifications.create("analysis-complete", {
      type: "basic",
      iconUrl: chrome.runtime.getURL("assets/audafact-temp.png"),
      title: "Analysis Complete! 🎵",
      message: "Your music analysis is ready. Click to view results!",
      priority: 2,
      requireInteraction: true,
    });
    debugLog("Notification created");
  } catch (err) {
    debugLog("Error in broadcastResults:", err);
  }
}

function broadcastError(errorMessage) {
  const errorData = {
    type: "ANALYSIS_ERROR",
    error: errorMessage
  };
  
  chrome.runtime.sendMessage(errorData)
    .catch(err => console.log("Popup might be closed:", err));

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]?.id) {
      chrome.tabs.sendMessage(tabs[0].id, errorData)
        .catch(err => console.log("Error sending to content script:", err));
    }
  });
}
