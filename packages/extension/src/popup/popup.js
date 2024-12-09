import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import './popup.css';
import storage from '../utils/storage';

function GenreList({ genres, showAll }) {
  const threshold = showAll ? 0 : 0.1;
  
  return Object.entries(genres)
    .filter(([_, confidence]) => confidence >= threshold)
    .sort(([_a, a], [_b, b]) => b - a)
    .map(([genre, confidence]) => (
      <li key={genre}>
        <span className="genre">{genre}</span>
        <span className={`confidence ${confidence < 0.1 ? 'low-confidence' : ''}`}>
          {(confidence * 100).toFixed(0)}%
        </span>
      </li>
    ));
}

function DiscogsList({ genres, showAll }) {
  const threshold = showAll ? 0 : 0.1;
  
  return Object.entries(genres).map(([category, subGenres]) => {
    const filteredGenres = Object.entries(subGenres)
      .filter(([_, confidence]) => confidence >= threshold)
      .sort(([_a, a], [_b, b]) => b - a);
      
    if (filteredGenres.length === 0) return null;
    
    return (
      <div key={category} className="category">
        <h3>{category}</h3>
        <ul>
          {filteredGenres.map(([genre, confidence]) => (
            <li key={genre}>
              <span className="genre">{genre}</span>
              <span className={`confidence ${confidence < 0.1 ? 'low-confidence' : ''}`}>
                {(confidence * 100).toFixed(0)}%
              </span>
            </li>
          ))}
        </ul>
      </div>
    );
  }).filter(Boolean);
}

function Popup() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAll, setShowAll] = useState(false);
  const [currentUrl, setCurrentUrl] = useState('');

  useEffect(() => {
    console.log("Popup mounted");
    
    // Force reset loading state on popup open
    chrome.storage.local.set({ analysisLoading: false });
    
    // Load initial state
    chrome.storage.local.get(['analysisResults'], (data) => {
      console.log("Initial storage data:", data);
      if (data.analysisResults) {
        console.log("Setting initial results:", data.analysisResults);
        setResults(data.analysisResults);
      }
      setLoading(false);
    });

    // Get current tab URL
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.url) {
        setCurrentUrl(tabs[0].url);
      }
    });

    // Listen for messages
    const messageListener = (message) => {
      console.log('Popup received message:', message);
      
      if (message.type === "ANALYSIS_RESULTS") {
        console.log("Setting results from message:", message.data);
        setResults(message.data);
        setLoading(false);
        setError(null);
        chrome.storage.local.set({ 
          analysisLoading: false,
          analysisResults: message.data 
        });
      } else if (message.type === "ANALYSIS_ERROR") {
        console.log("Setting error from message:", message.error);
        setError(message.error);
        setLoading(false);
        setResults(null);
        chrome.storage.local.set({ 
          analysisLoading: false,
          error: message.error,
          analysisResults: null
        });
      }
    };

    chrome.runtime.onMessage.addListener(messageListener);

    // Debug current state
    chrome.storage.local.get(null, (items) => {
      console.log('Current storage state:', items);
    });

    // Always check storage when popup opens
    chrome.storage.local.get(
      ['analysisResults', 'analysisLoading', 'error'],
      (data) => {
        if (data.analysisResults) setResults(data.analysisResults);
        setLoading(!!data.analysisLoading);
        setError(data.error || null);
      }
    );

    const handleStorageChange = (changes) => {
      if (changes.analysisResults?.newValue) {
        setResults(changes.analysisResults.newValue);
      }
      if (changes.analysisLoading?.newValue !== undefined) {
        setLoading(changes.analysisLoading.newValue);
      }
      if (changes.error?.newValue !== undefined) {
        setError(changes.error.newValue);
      }
    };

    chrome.storage.onChanged.addListener(handleStorageChange);
    return () => {
      console.log("Popup unmounting");
      chrome.runtime.onMessage.removeListener(messageListener);
      chrome.storage.onChanged.removeListener(handleStorageChange);
    };
  }, []);

  const handleReset = async () => {
    setResults(null);
    setLoading(false);
    setError(null);
    setShowAll(false);
    
    try {
      await chrome.storage.local.clear(); // Clear all stored data
      console.log('Storage cleared successfully');
    } catch (err) {
      console.error('Error clearing stored results:', err);
    }
  };

  const handleManualAnalyze = async () => {
    await handleReset(); // Reset before starting new analysis
    setLoading(true);
    
    try {
      await chrome.storage.local.set({
        analysisLoading: true
      });
      
      chrome.runtime.sendMessage({
        type: 'ANALYZE_URL',
        url: currentUrl,
        manual: true
      });
    } catch (err) {
      console.error('Error storing analysis state:', err);
      setError('Failed to start analysis');
      setLoading(false);
    }
  };

  const modelNames = {
    discogs400: 'Discogs 400',
    mtg_general: 'MTG General',
    mtg_track: 'MTG Track'
  };

  return (
    <div className="popup">
      <div className="header">
        <img 
          src="../assets/audafact-temp.png"
          alt="Audafact Logo"
          className="logo"
        />
        <div className="title-container">
          <h1>Audafact Music Intelligence</h1>
        </div>
        <label className="toggle-container">
          <input
            type="checkbox"
            checked={showAll}
            onChange={(e) => setShowAll(e.target.checked)}
          />
          <span className="toggle-label">Show all results</span>
        </label>
      </div>

      {results && (
        <div className="results-actions">
          <button 
            onClick={handleReset}
            className="reset-button"
          >
            New Analysis
          </button>
        </div>
      )}
      
      {!results && !loading && (
        <button 
          onClick={handleManualAnalyze} 
          disabled={loading}
          className="analyze-button"
        >
          Analyze Current Page
        </button>
      )}
      
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          Analyzing audio...
        </div>
      )}

      {error && (
        <div className="error">{error}</div>
      )}

      {results && results.genres && (
        <div className="results">
          {Object.entries(results.genres).map(([model, genres]) => (
            <div key={model} className="model-results">
              <h2>{modelNames[model] || model}</h2>
              {model === 'discogs400' ? (
                <DiscogsList genres={genres} showAll={showAll} />
              ) : (
                <ul>
                  <GenreList genres={genres} showAll={showAll} />
                </ul>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<Popup />);
