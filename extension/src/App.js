import styles from './App.module.css';

import { useState } from 'react';

import useWikipediaTitle from './hooks/useWikipediaTitle';
import ScanButton from './components/ScanButton';
import WikiHeader from './components/WikiHeader';
import QualityReport from './components/QualityReport';
import FeatureReport from './components/FeatureReport';
import InfoTitle from './components/InfoTitle';
import classNames from 'classnames';
import ReadabilityReport from "./components/ReadabilityReport";

function App() {
  const [quality, setQuality] = useState(null)
  const [features, setFeatures] = useState({})
  const [isLoading, title, language] = useWikipediaTitle()

  const onScanComplete = (quality, features) => {
    setQuality(quality)
    setFeatures(features)
  }

  return (
    <div className={classNames(styles.app, {[styles.hasQuality]: quality })} >
      <WikiHeader isLoading={isLoading} title={title} language={language} />

      <div>
        <InfoTitle title="Quality" infoFile="quality.txt"/>
        {quality ?
          <QualityReport quality={quality}/> :
          <ScanButton title={title} language={language} onScanComplete={onScanComplete}/>
        }
      </div>

      <div className={styles.reports}>
        <ReadabilityReport features={features}/>
        <FeatureReport features={features}/>
      </div>
    </div>
  );
}

export default App;
