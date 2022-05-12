

import { useState, useEffect } from "react"
import languages from '../langs/languages.json'

export default function useWikipediaTitle() {
    const [isLoading, setLoading] = useState(true)
    const [title, setTitle] = useState(null)
    const [language, setLanguage] = useState(null)

    useEffect(() => {
        setLoading(true)
        getTabURL().then(url => {
            const [href, urltitle] = url.split("/wiki/")
            const language = href.split("://")[1].split(".")[0]

            if (href.includes("wikipedia.org")) {
                setTitle(urltitle)
                setLanguage(languages[language])
            }
            else {
                setTitle(null)
                setLanguage(null)
            }

            setLoading(false)
        })
    }, [])

    const cleanTitle = title.replace(/_/g, " ")



    return [isLoading, cleanTitle, language]  

}

/*global chrome*/
async function getTabURL() {
    return "https://en.wikipedia.org/wiki/Nicolas_Cage"
    let [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    return tab.url;
}
