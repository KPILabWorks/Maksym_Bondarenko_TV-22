import axios from 'axios';
import { ChangeEvent, useMemo, useRef, useState } from 'react';

const styles = {
  container: {
    fontFamily: 'sans-serif',
    maxWidth: 600,
    margin: '2rem auto',
    padding: '1rem',
    border: '1px solid #ddd',
    borderRadius: '8px',
    backgroundColor: '#fafafa'
  },
  addButton: {
    padding: '10px 15px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    marginBottom: '1rem'
  },
  fileGroup: {
    marginBottom: '1.5rem',
    padding: '0.5rem',
    backgroundColor: '#fff',
    borderRadius: '6px',
    boxShadow: '0 0 4px rgba(0,0,0,0.1)'
  },
  fileType: {
    fontWeight: 'bold',
    fontSize: '1.1rem',
    marginBottom: '0.5rem'
  },
  fileList: {
    listStyle: 'none',
    paddingLeft: 0
  },
  fileItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '6px 0',
    borderBottom: '1px solid #eee'
  },
  removeButton: {
    backgroundColor: '#dc3545',
    color: '#fff',
    border: 'none',
    padding: '4px 8px',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  mergeButton: {
    marginTop: '1rem',
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer'
  },
  resultBox: {
    marginTop: '2rem',
    padding: '1rem',
    backgroundColor: '#f4f4f4',
    borderRadius: '8px',
    border: '1px solid #ccc',
    boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
    maxHeight: '300px'
  },
  resultTitle: {
    marginBottom: '0.75rem',
    fontSize: '1.2rem',
    fontWeight: 'bold'
  },
  resultList: {
    listStyle: 'none',
    padding: 0,
    margin: 0
  },
  resultItem: {
    backgroundColor: '#fff',
    padding: '0.5rem',
    marginBottom: '0.5rem',
    borderRadius: '6px',
    border: '1px solid #ddd',
    fontFamily: 'monospace',
    fontSize: '0.9rem'
  },
  resultJson: {
    margin: '0',
    whiteSpace: 'pre-wrap'
  }
};

interface IFileView {
  filename: string;
  ext: string;
}

function App() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<File[]>([]);
  const [result, setResult] = useState<Record<string, string>[]>([]);

  const sortedFiles = useMemo(() => {
    const data: Record<string, IFileView[]> = {};
    let name: string, ext: string;

    for (const file of files) {
      [name, ext] = file.name.split('.');
      if (!data[ext]) data[ext] = [];
      data[ext].push({ filename: name, ext });
    }

    return data;
  }, [files]);

  const handleAddFile = () => {
    if (fileInputRef && fileInputRef.current) fileInputRef.current?.click();
  };

  const handleSaveFile = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    const file = e.target.files.item(0);
    if (!file) return;
    if (files.find((f) => f.name === file.name)) return;
    setFiles((prev) => [file, ...prev]);
    fileInputRef.current!.value = '';
  };

  const handleRemoveFile = (filename: string) => () => {
    console.log(filename);

    setFiles((prev) => prev.filter((f) => f.name !== filename));
  };

  const handleMergeFiles = async () => {
    const fd = new FormData();

    for (const file of files) {
      fd.append('files', file);
    }

    const res = await axios.post('http://localhost:8000/', fd);
    setResult(res.data);
  };

  return (
    <>
      <div style={styles.container}>
        <input
          accept=".csv,.json,.db"
          onChange={handleSaveFile}
          ref={fileInputRef}
          type="file"
          hidden
        />

        <button style={styles.addButton} onClick={handleAddFile}>
          📁 Add File
        </button>

        {sortedFiles &&
          Object.keys(sortedFiles).map((ext) => (
            <div key={ext} style={styles.fileGroup}>
              <p style={styles.fileType}>{ext.toUpperCase()} Files</p>
              <ul style={styles.fileList}>
                {sortedFiles[ext].map((file) => (
                  <li key={file.filename} style={styles.fileItem}>
                    <span>{file.filename}</span>
                    <button
                      style={styles.removeButton}
                      onClick={handleRemoveFile(`${file.filename}.${ext}`)}>
                      ❌ Remove
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}

        {!!files.length && (
          <button style={styles.mergeButton} onClick={handleMergeFiles}>
            🔀 Merge Files
          </button>
        )}
      </div>

      {result.length > 0 && (
        <div style={styles.resultBox}>
          <h3 style={styles.resultTitle}>🧾 Merged Result</h3>
          <ul style={styles.resultList}>
            {result.map((r, i) => (
              <li key={i} style={styles.resultItem}>
                <pre style={styles.resultJson}>
                  {JSON.stringify(r, null, 2)}
                </pre>
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}

export default App;
