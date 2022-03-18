
import './App.css';
import { useState } from 'react';
import axios from 'axios';

const API_URL = "http://localhost:5000/evaluate/";
function App() {
  const [titleInput, setTitleInput] = useState("")

  const [quality, setQuality] = useState("")
  const [title, setTitle] = useState("")

  function doWikipediaStuff() { 
    axios.get(API_URL + titleInput).then(res => {
      setTitle(res.data.title);
      setQuality(res.data.quality);
    })

  }
  
  return (
    <div className="App">
     {/*  <div style="width: 300px;height: 300px;text-align: center; font-size: 2.5em;display: flex;flex-direction:column;align-items: center;justify-content: center;">
        This is like the best Wikipedia page ever
      
        <strong style="font-weight: bold; font-size: 2em;">A+</strong>
      </div> */}

      <div style={{ display: "flex", justifyContent: "center", flexDirection: "column", gap: "8px"}}>
        <input name="title" value={titleInput} onChange={e => setTitleInput(e.target.value)}/>    

        <button onClick={doWikipediaStuff}>Do Wiki</button>

        {/* <button onClick={extensionUpdatePageBackgroundColor}>Change Color (test)</button> */}
      </div>

      {quality && (
        <div>
          <h2>{title}</h2>
          <p>Quality: {quality}</p>
        </div>
      )}


    </div>
  );
}

export default App;
