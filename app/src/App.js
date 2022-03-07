/*global chrome*/

import logo from './logo.svg';
import './App.css';


function setPageBackgroundColor() {
  chrome.storage.sync.get("color", ({ color }) => {
    document.body.style.backgroundColor = color;
  });
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>

     {/*  <div style="width: 300px;height: 300px;text-align: center; font-size: 2.5em;display: flex;flex-direction:column;align-items: center;justify-content: center;">
        This is like the best Wikipedia page ever
      
        <strong style="font-weight: bold; font-size: 2em;">A+</strong>
      </div> */}
    
      <button id="changeColor" onClick={async () => { 
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          function: setPageBackgroundColor,
        });
      }}></button>
    </div>
  );
}

export default App;
