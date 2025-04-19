import './App.css';
import Sources from './Sources';
import React, { useState } from 'react';

function App() {
  const [protocol, setProtocol] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [query, setQuery] = useState('');
  const [k, setK] = useState(3);
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);

  const handleAsk = async () => {
    try {
      const params = new URLSearchParams({ protocol, query, k: k.toString() });
      const res = await fetch(`http://localhost:8000/answer?${params}`);
      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText);
      }
      const data = await res.json();
      let text = data.answer;
      if (typeof text === "object" && text !== null) {
        text = text.content ?? text.message?.content ?? JSON.stringify(text);
      }
      setAnswer(text);
      setSources(data.sources);
    } catch (err) {
      console.error(err);
      alert('Error: ' + err.message);
    }
  };

  const handleProtocolChange = async (e) => {
    const search = e.target.value;
    setProtocol(search);

    if (!search) {
      setSuggestions([]);
      return;
    }

    try {
      const params = new URLSearchParams({ search });
      const res = await fetch(`http://localhost:8000/keywords?${params}`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();

      // Expect `data` to be an array of strings:
      setSuggestions(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error fetching suggestions:', err);
      setSuggestions([]);
    }
  };

  // --- Clear protocol + suggestions on form submit ---
  const handleSubmit = (e) => {
    e.preventDefault();
    if (protocol.trim()) {
      console.log('Protocol submitted:', protocol);
      setProtocol('');
      setSuggestions([]);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>LabRAG</p>
      </header>
      <subheader className="App-description">
        <p>AI platform that acts as a basic biology/biotech laboratory assistant that allows users to ask questions about a particular lab procedure and modify lab procedures based on available equipment. All sources are thoughtfully cited, with the author and the university/laboratory that created the base protocol, making LabRAG a project that maintains the highest standard of ethical and responsible AI.</p>
      </subheader>
      <main className="App-main">
        <div className="sidebar">
          <div className="field">
            <label htmlFor="protocol">Protocol Keyword</label>
            {/* Autocomplete form */}
            <form onSubmit={handleSubmit} autoComplete="off">
              <div
                className="autocomplete"
                style={{ position: 'relative', width: 300 }}
              >
                <input
                  className="input"
                  value={protocol}
                  onChange={handleProtocolChange}
                />

                {/* Suggestions dropdown */}
                {suggestions.length > 0 && (
                  <div
                    className="autocomplete-items"
                    style={{
                      position: 'absolute',
                      top: '100%',
                      left: 0,
                      right: 0,
                      border: '1px solid #ccc',
                      background: '#fff',
                      zIndex: 10,
                      maxHeight: 200,
                      overflowY: 'auto',
                    }}
                  >
                    {suggestions.map((item, idx) => (
                      <div
                        key={idx}
                        onMouseDown={(e) => e.preventDefault()} // keep focus
                        onClick={() => {
                          setProtocol(item);
                          setSuggestions([]);
                        }}
                        style={{ padding: '8px', cursor: 'pointer' }}
                      >
                        {item}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </form>
          </div>

          <div className="field">
            <label htmlFor="query">Query</label>
            <input
              id="query"
              className="input"
              value={query}
              onChange={e => setQuery(e.target.value)}
            />
          </div>

          <div className="field">
            <label htmlFor="k">Source Count</label>
            <input
              id="k"
              type="number"
              className="input k-input"
              min={1}
              value={k}
              onChange={e => setK(Number(e.target.value))}
            />
          </div>

          <button className="btn" onClick={handleAsk}>
            Ask
          </button>
        </div>

        <section className="response">
          <h3>Answer</h3>
          <p>{answer}</p>
          <Sources sources={sources} />
        </section>
      </main>
      <footer className="App-footer">
          <p>© 2025 LabRAG. All rights reserved.</p>
          <nav>
            <a href="#">About</a> | 
            <a href="#">Docs</a> | 
            <a href="#">Contact</a>
          </nav>
      </footer>
    </div>
  );
}

export default App;