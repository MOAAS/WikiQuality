import styles from './WikiHeader.module.css';
import languages from '../lib/languages.json';

export default function WikiHeader({ isLoading, title, language }) {

    if (isLoading)
        title = "Loading..."
    else if (!title)
        title = "Not on a Wikipedia page."

    return (
        <header className={styles.header}>
            <h1>WikiQuality</h1>
            <h2>{title} {language && ` (${languages[language]} Wiki)`}</h2>
        </header>
    )
}
