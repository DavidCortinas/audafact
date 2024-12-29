import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import './popup.css';
import storage from '../utils/storage';

const DEBUG = true;
const debugLog = (message, data) => {
  if (DEBUG) {
    console.log(`[Popup ${new Date().toISOString()}] ${message}`, data || '');
  }
};

// Results display components
function GenreResults({ data }) {
  return (
    <div className="results-container">
      <h3>Genre Analysis</h3>
      {Object.entries(data).map(([mainGenre, subGenres]) => (
        <div key={mainGenre} className="genre-section">
          <h4>{mainGenre}</h4>
          <ul className="results-list">
            {Object.entries(subGenres)
              .sort(([, a], [, b]) => b - a)
              .map(([subGenre, confidence]) => (
                <li key={`${mainGenre}-${subGenre}`} className="result-item">
                  <span className="genre">{subGenre}</span>
                  <span className="confidence">
                    {Math.round(confidence * 100)}%
                  </span>
                </li>
              ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

function MoodThemeResults({ data }) {
  const { general, track_level } = data.mood_themes;

  return (
    <div className="results-container">
      <div className="mood-section">
        <h3>General Moods & Themes</h3>
        <ul className="results-list">
          {Object.entries(general)
            .sort(([_a, a], [_b, b]) => b - a)
            .map(([mood, confidence]) => (
              <li key={mood} className="result-item">
                <span className="mood">{mood}</span>
                <span className="confidence">
                  {(confidence * 100).toFixed(0)}%
                </span>
              </li>
            ))}
        </ul>
      </div>

      <div className="mood-section">
        <h3>Track-Level Moods & Themes</h3>
        <ul className="results-list">
          {Object.entries(track_level)
            .sort(([_a, a], [_b, b]) => b - a)
            .map(([mood, confidence]) => (
              <li key={mood} className="result-item">
                <span className="mood">{mood}</span>
                <span className="confidence">
                  {(confidence * 100).toFixed(0)}%
                </span>
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
}

function TagResults({ data }) {
  return (
    <div className="results-container">
      {Object.entries(data.predictions).map(([category, tags]) => (
        <div key={category} className="tag-section">
          <h3>{category.replace(/_/g, ' ').toUpperCase()}</h3>
          <ul className="results-list">
            {Object.entries(tags)
              .sort(([_a, a], [_b, b]) => b - a)
              .map(([tag, confidence]) => (
                <li key={tag} className="result-item">
                  <span className="tag">{tag}</span>
                  <span className="confidence">
                    {(confidence * 100).toFixed(0)}%
                  </span>
                </li>
              ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

function Popup() {
  const [currentUrl, setCurrentUrl] = useState('');
  const [activeTab, setActiveTab] = useState('genres');
  const [results, setResults] = useState({
    genres: null,
    moodThemes: null,
    tags: null
  });
  const [loading, setLoading] = useState({
    genres: false,
    moodThemes: false,
    tags: false
  });
  const [error, setError] = useState({
    genres: null,
    moodThemes: null,
    tags: null
  });

  // Get current URL when popup opens
  useEffect(() => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.url) {
        setCurrentUrl(tabs[0].url);
        debugLog('Current URL set:', tabs[0].url);
      }
    });
  }, []);

  const handleAnalyze = async (type) => {
    debugLog(`Analyze ${type} clicked for URL:`, currentUrl);
    
    // Set loading state BEFORE sending the message
    setLoading(prev => ({
      ...prev,
      [type]: true
    }));

    // Also set loading state in storage
    await chrome.storage.local.set({
      [`${type}Loading`]: true,
      [`${type}Results`]: null,  // Clear previous results
      [`${type}Error`]: null     // Clear previous errors
    });

    // Send message to background script
    chrome.runtime.sendMessage({
      type: 'ANALYZE_URL',
      url: currentUrl,
      analysisType: type
    });
  };

  // Storage change listener
  useEffect(() => {
    const handleStorageChange = (changes, area) => {
      debugLog('Storage changes:', changes);
      
      for (const [key, { newValue }] of Object.entries(changes)) {
        // Handle loading state changes
        if (key.endsWith('Loading')) {
          const type = key.replace('Loading', '');
          setLoading(prev => ({
            ...prev,
            [type]: !!newValue  // Ensure boolean value
          }));
        }
        // Handle results
        if (key.endsWith('Results') && newValue) {
          const type = key.replace('Results', '');
          setResults(prev => ({
            ...prev,
            [type]: newValue
          }));
          // Set loading to false when results arrive
          setLoading(prev => ({
            ...prev,
            [type]: false
          }));
        }
        // Handle errors
        if (key.endsWith('Error') && newValue) {
          const type = key.replace('Error', '');
          setError(prev => ({
            ...prev,
            [type]: newValue
          }));
          // Set loading to false when error occurs
          setLoading(prev => ({
            ...prev,
            [type]: false
          }));
        }
      }
    };

    chrome.storage.onChanged.addListener(handleStorageChange);
    return () => chrome.storage.onChanged.removeListener(handleStorageChange);
  }, []);

  return (
    <div className="popup">
      <div className="header">
        <img src="../assets/audafact-temp.png" alt="Audafact Logo" className="logo" />
        <h1>Audafact Music Intelligence</h1>
      </div>

      <div className="tabs">
        <button 
          className={activeTab === 'genres' ? 'active' : ''} 
          onClick={() => setActiveTab('genres')}
        >
          Genres
        </button>
        <button 
          className={activeTab === 'moodThemes' ? 'active' : ''} 
          onClick={() => setActiveTab('moodThemes')}
        >
          Mood & Themes
        </button>
        <button 
          className={activeTab === 'tags' ? 'active' : ''} 
          onClick={() => setActiveTab('tags')}
        >
          Tags
        </button>
      </div>

      <div className="content">
        <div className="analysis-section">
          {activeTab === 'genres' && (
            <>
              <button 
                onClick={() => handleAnalyze('genres')} 
                disabled={loading.genres}
                className="analyze-button"
              >
                {loading.genres ? 'Analyzing...' : 'Analyze Genres'}
              </button>
              {loading.genres && (
                <div className="loading-container">
                  <div className="loading">Analyzing genres...</div>
                </div>
              )}
              {error.genres && <div className="error">{error.genres}</div>}
              {results.genres && <GenreResults data={results.genres} />}
            </>
          )}

          {activeTab === 'moodThemes' && (
            <>
              <button 
                onClick={() => handleAnalyze('moodThemes')} 
                disabled={loading.moodThemes}
                className="analyze-button"
              >
                {loading.moodThemes ? 'Analyzing...' : 'Analyze Mood & Themes'}
              </button>
              {loading.moodThemes && (
                <div className="loading-container">
                  <div className="loading">Analyzing mood & themes...</div>
                </div>
              )}
              {error.moodThemes && <div className="error">{error.moodThemes}</div>}
              {results.moodThemes && <MoodThemeResults data={results.moodThemes} />}
            </>
          )}

          {activeTab === 'tags' && (
            <>
              <button 
                onClick={() => handleAnalyze('tags')} 
                disabled={loading.tags}
                className="analyze-button"
              >
                {loading.tags ? 'Analyzing...' : 'Analyze Tags'}
              </button>
              {loading.tags && (
                <div className="loading-container">
                  <div className="loading">Analyzing tags...</div>
                </div>
              )}
              {error.tags && <div className="error">{error.tags}</div>}
              {results.tags && <TagResults data={results.tags} />}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<Popup />);
