import styles from './App.module.css';

import { useState } from 'react';

import useWikipediaTitle from './hooks/useWikipediaTitle';
import ScanButton from './components/ScanButton';
import WikiTitle from './components/WikiTitle';
import QualityReport from './components/QualityReport';
import QualityMeter from './components/QualityMeter';
import FeatureReport from './components/FeatureReport';

function App() {
  const [quality, setQuality] = useState(null)
  const [features, setFeatures] = useState({})
  const [isLoading, title, language] = useWikipediaTitle()

  const onScanComplete = (quality, features) => {
    setQuality(quality)
    setFeatures(features)
  }

  return (
    <div className={styles.app}>
      <h1>WikiQuality</h1>

      <div className={styles.main}>
        <WikiTitle isLoading={isLoading} title={title} language={language} />


        <ScanButton title={title} language={language} onScanComplete={onScanComplete}/>

        <QualityReport quality={quality}/>
      </div>

      <div className={styles.meter}>
        <QualityMeter quality={quality}/>
      </div>

      <div className={styles.footer}>
        <FeatureReport features={features}/>
        {/* Put feature report here */}
      </div>
    </div>
  );
}

export default App;
