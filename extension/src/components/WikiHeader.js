import styles from './WikiHeader.module.css';
import languages from '../lib/languages.json';

export default function WikiHeader({ isLoading, title, language }) {    
    if (isLoading)
        title = "Loading..."
    else if (!title)
        title = <span style={{color: "var(--error)"}}>Not on a Wikipedia page.</span>

    return (
        <header className={styles.header}>
            <h1>WikiQuality</h1>
            <h2>{title} {language && ` (${languages[language]} Wiki)`}</h2>
        </header>
    )
}
