// Function to check if URL is a direct audio file
function isAudioUrl(url) {
  // Skip blob URLs as they can't be processed
  if (url.startsWith('blob:')) return false;
  
  const audioExtensions = ['.mp3', '.wav', '.ogg', '.m4a', '.aac'];
  return audioExtensions.some(ext => url.toLowerCase().endsWith(ext));
}

// Function to handle audio elements
function handleAudioElements() {
  // Get all audio and video elements
  const mediaElements = [...document.getElementsByTagName('audio'), 
                        ...document.getElementsByTagName('video')];
  
  if (mediaElements.length > 0 && !document.querySelector('.audafact-prompt')) {
    showAnalysisPrompt();
  }
}

// Special handling for known streaming sites
const streamingSites = {
  'youtube.com': url => url.includes('watch?v='),
  'soundcloud.com': url => true  // Accept any soundcloud URL for now
};

// Check if current page is a known streaming site
function checkStreamingSite() {
  const currentUrl = window.location.href;
  const hostname = window.location.hostname;
  
  console.log('Checking site:', hostname, currentUrl);
  
  for (const [site, validator] of Object.entries(streamingSites)) {
    if (hostname.includes(site) && validator(currentUrl)) {
      console.log(`Audafact detected ${site} track:`, currentUrl);
      showAnalysisPrompt();
      break;
    }
  }
}

// Run check when script loads
checkStreamingSite();

// Watch for URL changes
let lastUrl = window.location.href;
new MutationObserver(() => {
  const currentUrl = window.location.href;
  if (lastUrl !== currentUrl) {
    lastUrl = currentUrl;
    checkStreamingSite();
  }
}).observe(document.querySelector('body'), { subtree: true, childList: true });

// Listen for page load
document.addEventListener('DOMContentLoaded', handleAudioElements);

// Watch for dynamic changes that might add audio elements
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.addedNodes.length) {
      handleAudioElements();
    }
  });
});

observer.observe(document.body, { 
  childList: true, 
  subtree: true 
});

function showAnalysisPrompt() {
  // Remove existing prompt if any
  const existingPrompt = document.querySelector('.audafact-prompt');
  if (existingPrompt) {
    existingPrompt.remove();
  }

  const prompt = document.createElement('div');
  prompt.className = 'audafact-prompt';
  prompt.innerHTML = `
    <div class="audafact-prompt-content">
      <h3>Audafact</h3>
      <p>Would you like to analyze this audio?</p>
      <div class="audafact-prompt-buttons">
        <button class="audafact-analyze">Analyze</button>
        <button class="audafact-dismiss">Not Now</button>
      </div>
    </div>
  `;

  document.body.appendChild(prompt);

  prompt.querySelector('.audafact-analyze').addEventListener('click', () => {
    chrome.runtime.sendMessage({
      type: 'ANALYZE_URL',
      url: window.location.href
    });
    prompt.remove();
    showAnalysisProgress();
  });

  prompt.querySelector('.audafact-dismiss').addEventListener('click', () => {
    prompt.remove();
  });
}

function showAnalysisProgress() {
  const progress = document.createElement('div');
  progress.className = 'audafact-progress';
  progress.innerHTML = `
    <div class="audafact-progress-content">
      <div class="audafact-spinner"></div>
      <p>Analyzing audio content...</p>
    </div>
  `;

  document.body.appendChild(progress);

  // Listen for completion
  chrome.runtime.onMessage.addListener((message) => {
    console.log('Content script received message:', message);
    if (message.type === 'ANALYSIS_RESULTS') {
      const progress = document.querySelector('.audafact-progress');
      if (progress) {
        progress.remove();
      }
    }
  });
}
