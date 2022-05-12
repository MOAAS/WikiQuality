import styles from './App.module.css';

import { useState } from 'react';

import useWikipediaTitle from './hooks/useWikipediaTitle';
import ScanButton from './components/ScanButton';
import WikiTitle from './components/WikiTitle';
import QualityReport from './components/QualityReport';

function App() {
  const [quality, setQuality] = useState("")
  const [features, setFeatures] = useState({})
  const [isLoading, title, language] = useWikipediaTitle()

  const onScan = (quality, features) => {
    setQuality(quality)
    setFeatures(features)
  }

  return (
    <div className={styles.app}>
      <h1>WikiQuality</h1>

      <WikiTitle isLoading={isLoading} title={title} language={language} />
          

      <ScanButton title={title} onScan={onScan} />

      <QualityReport quality={quality} features={features} />
    </div>
  );
}

export default App;
