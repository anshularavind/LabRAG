import { useState, useEffect } from 'react';

const Sources = ({ sources }) => {
    async function cite(fileName) {
        try {
            const params = new URLSearchParams({ fileName });
            const apiUrl = `http://localhost:8000/cite?${params}`;
            return fetch(apiUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Citation API error: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    return data;
                })
                .catch(error => {
                    console.error('Error:', error);
                    return error;
                }); 
        } catch (err) {
            console.error(err);
            alert('Error: ' + err.message);
        }
    }

    const [citations, setCitations] = useState([]);

    useEffect(() => {
        // 2. When `sources` changes (or on mount), fetch citations in parallel
        async function loadCitations() {
            const fetched = await Promise.all(
                sources.map(s => cite(s.source))
            );
            setCitations(fetched);
        }

        loadCitations();
    }, [sources]);

    // Don’t even try to render the list until we have every citation
    if (citations.length !== sources.length) {
        return <div>Loading citations…</div>;
    }

    return (
        <div>
            <h4>Sources</h4>
            <ul>
                {sources.map((s, i) => (
                    <li key={i}>
                        <a href={citations[i].url}>{citations[i].citation}</a> (chunk {s.chunk_index})
                    </li>
                // <li key={i}>{s.source} (chunk {s.chunk_index})</li>
                ))}
            </ul>
        </div>
    );
  };
  
  export default Sources;