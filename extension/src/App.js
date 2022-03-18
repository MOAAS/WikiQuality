
import './App.css';
import { useState } from 'react';
import { getPageContent } from './WikiAPI';
import { extensionUpdatePageBackgroundColor } from './ExtensionTest';

function App() {
  const [title, setTitle] = useState("")

  const [text, setText] = useState("")

  function doWikipediaStuff() {    
    getPageContent(title).then(res => {

      setText("Quality: Very good! " + res.parse.wikitext)
      console.log(res);
    })

  }
  
  return (
    <div className="App">
     {/*  <div style="width: 300px;height: 300px;text-align: center; font-size: 2.5em;display: flex;flex-direction:column;align-items: center;justify-content: center;">
        This is like the best Wikipedia page ever
      
        <strong style="font-weight: bold; font-size: 2em;">A+</strong>
      </div> */}

      <div style={{ display: "flex", justifyContent: "center", flexDirection: "column", gap: "8px"}}>
        <input name="title" value={title} onChange={e => setTitle(e.target.value)}/>    

        <button onClick={doWikipediaStuff}>Do Wiki</button>

        {/* <button onClick={extensionUpdatePageBackgroundColor}>Change Color (test)</button> */}
      </div>

      <p>{text}</p>

    </div>
  );
}

export default App;
