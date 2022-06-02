

import { useState, useEffect } from "react"

export default function useWikipediaTitle() {
    const [isLoading, setLoading] = useState(true)
    const [title, setTitle] = useState(null)
    const [language, setLanguage] = useState(null)

    useEffect(() => {
        setLoading(true)
        getTabURL().then(url => {
            const [href, urltitle] = url.split("/wiki/")
            const language = href?.split("://")[1]?.split(".")[0]

            if (href.includes("wikipedia.org")) {
                setTitle(urltitle)
                setLanguage(language)
            }
            else {
                setTitle(null)
                setLanguage(null)
            }

            setLoading(false)
        })
    }, [])



    const cleanTitle = decodeURIComponent((title || "").replace(/_/g, " "))

    return [isLoading, cleanTitle || null, language || null] 

}

/*global chrome*/
async function getTabURL() {
    if (process.env.NODE_ENV === "development") {
        return "https://en.wikipedia.org/wiki/Baby_(Clean_Bandit_song)"
    }
    else {
        let [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
        return tab.url;
    }
}
