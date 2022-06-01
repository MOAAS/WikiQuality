import styles from './WikiTitle.module.css';
import languages from '../lib/languages.json';

export default function WikiTitle({ isLoading, title, language }) {

    if (isLoading)
        title = "Loading..."
    else if (!title)
        title = "Not on a Wikipedia page."

    return (
        <h2 className={styles.title}>
            {title} {language && (<small>{`(${languages[language]} Wiki)`}</small>)}
        </h2>
    )
}
