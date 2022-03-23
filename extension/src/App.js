import './App.css';
import { useCallback, useState } from 'react';
import axios from 'axios';
import { getTabURL } from './ExtensionTest';


const API_URL = "http://localhost:5000/evaluate/";

function App() {
  //const [titleInput, setTitleInput] = useState("")

  const [quality, setQuality] = useState("")
  const [title, setTitle] = useState("")

  const scanTitle = useCallback(() => {
    setTitle("")
  
    setQuality("")
    getTabURL().then(url => {

      
      const [href, title] = url.split("/wiki/")



      if (href.includes("wikipedia.org")) {
        const decodedTitle = decodeURIComponent(title).replace(/_/g, " ")
        setTitle("Calculating Quality...");

        axios.get(API_URL + title).then(res => {
          setTitle(decodedTitle)
          setQuality(res.data.quality);

        }).catch(err => {
          console.log(err);
          setTitle("Error fetching Wikipedia Page.")
        })
      }
      else {
        setTitle("Not a wikipedia page")
      }
    });   
  })
  

  
  return (
    <div className="App">
      <div style={{ display: "flex", justifyContent: "center", flexDirection: "column", gap: "8px"}}>
        {/* <input name="title" value={titleInput} onChange={e => setTitleInput(e.target.value)}/>     */}

        <button onClick={scanTitle}>Do Wiki</button>

        {/* <button onClick={extensionUpdatePageBackgroundColor}>Change Color (test)</button> */}
      </div>

        <div>
          <h2>{title}</h2>
          {quality && (<p>Quality: {quality}</p>)}
        </div>
    </div>
  );
}

export default App;
