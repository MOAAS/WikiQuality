import styles from './App.module.css';
import { useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import { getTabURL } from './ExtensionTest';
import languages from './languages.json'


const API_URL = "http://localhost:5000/evaluate/";

function App() {
  const [isWikipedia, setIsWikipedia] = useState(false)
  const [title, setTitle] = useState("")
  const [language, setLanguage] = useState("")

  const [quality, setQuality] = useState("")
  const [error, setError] = useState("")

  useEffect(() => {
    getTabURL().then(url => {
      const [href, urltitle] = url.split("/wiki/")
      const language = href.split("://")[1].split(".")[0]

      setIsWikipedia(href.includes("wikipedia.org"))
      setTitle(urltitle)
      setLanguage(languages[language])
    })
  }, [])


  const scanTitle = useCallback(() => {
    axios.get(API_URL + title).then(res => {
      console.log(res.data)
      setTitle(title)
      setQuality(res.data.quality);
    }).catch(err => {  
      console.log(err);
      setError("Error fetching Wikipedia Page.")
    })
  }, [title])


  return (
    <div className={styles.app}>
      <h1>WikiQuality</h1>

      <h2>{isWikipedia ? title : "Not on a Wikipedia page."}</h2>

      <h2>{isWikipedia ? `Language: ${language}` : ""} </h2>


      <button onClick={scanTitle} className={styles.button} disabled={!isWikipedia}>SCAN</button>

      {quality && <p>Quality: {quality}</p>}

      {error && <p>{error}</p>}
    </div>
  );
}

export default App;
