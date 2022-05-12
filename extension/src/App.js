import styles from './App.module.css';

import { useState } from 'react';

import useWikipediaTitle from './hooks/useWikipediaTitle';
import ScanButton from './components/ScanButton';

function App() {
  const [quality, setQuality] = useState("")

  const [isLoading, title, language] = useWikipediaTitle()

  return (
    <div className={styles.app}>
      <h1>WikiQuality</h1>

      <h2 className={styles.title}>
        {isLoading || title ? title : "Not on a Wikipedia page."}  {<small>{`(${language} Wiki)`}</small>}
      </h2>

          

      <ScanButton title={title} onScan={setQuality} />

      {quality && <p>Quality: {quality}</p>}
    </div>
  );
}

export default App;
