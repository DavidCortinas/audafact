import storage from '../utils/storage';

const API_BASE_URL = "http://localhost:8000/api";

// Debug logging for all messages
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Background script received message:", message);
  
  if (message.type === "ANALYZE_URL") {
    console.log("Starting analysis for URL:", message.url);
    analyzeAudioUrl(message.url);
  }
});

async function analyzeAudioUrl(url) {
  try {
    await storage.set({ analysisLoading: true, error: null });
    
    const apiUrl = `${API_BASE_URL}/genres/url?url=${encodeURIComponent(url)}`;
    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Store results immediately when received
    await storage.set({
      analysisResults: data,
      analysisLoading: false,
      error: null
    });

    // Try to notify any open popups, but don't depend on it
    try {
      chrome.runtime.sendMessage({
        type: "ANALYSIS_COMPLETE",
        data: data
      }).catch(() => {
        // Ignore errors from closed popups
      });
    } catch (e) {
      // Ignore messaging errors
    }

    return data;
  } catch (error) {
    await storage.set({
      analysisLoading: false,
      error: error.message,
      analysisResults: null
    });
    throw error;
  }
}

async function broadcastResults(data) {
  try {
    // Store results
    await storage.set({
      analysisResults: data,
      analysisLoading: false
    });

    // Send to popup
    chrome.runtime.sendMessage({
      type: "ANALYSIS_RESULTS",
      data: data
    }).catch(err => console.log("Popup might be closed:", err));

    // Send to active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.tabs.sendMessage(tabs[0].id, {
          type: "ANALYSIS_RESULTS",
          data: data
        }).catch(err => console.log("Error sending to content script:", err));
      }
    });

    // Show notification
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'assets/icon128.png',
      title: 'Audafact Analysis Complete',
      message: 'Your audio analysis results are ready to view!'
    });
  } catch (err) {
    console.error('Error storing results:', err);
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
