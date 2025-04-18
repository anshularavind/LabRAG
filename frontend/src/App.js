import './App.css';
import Sources from './Sources';
import { useState } from 'react';

function App() {
  const [protocol, setProtocol] = useState('');
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
            <input
              id="protocol"
              className="input"
              value={protocol}
              onChange={e => setProtocol(e.target.value)}
            />
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
