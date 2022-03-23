/*global chrome*/

export async function extensionUpdatePageBackgroundColor() {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
          chrome.storage.sync.get("color", ({ color }) => {
            document.body.style.backgroundColor = color;
          });
        },
      });  
  }
  
export async function getTabURL() {
  let [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  return tab.url;
}