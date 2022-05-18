import qualityToLetter from '../langs/qualityToLetter';
import styles from './QualityMeter.module.css'

const classnames = require('classnames')

export default function QualityMeter({quality}) {
    let letter = qualityToLetter(quality)
    if (letter === "A+")
        letter = "Aplus"
    if (letter === null)
        letter = "none"

    return (
        <div className={styles.meter}>
            <QualityBlock letter="A+"/>
            <QualityBlock letter="A"/>
            <QualityBlock letter="B"/>
            <QualityBlock letter="C"/>
            <QualityBlock letter="D"/>
            <QualityBlock letter="F"/>

            <div style={{bottom: quality * 100 + "%"}} className={classnames(styles.pointer, styles[letter + "-pointer"])}>
                ➡
            </div>
        </div>
    )
}

function QualityBlock({letter}) {
    let className = letter === "A+" ? styles["Aplus-block"] : styles[letter + "-block"];

    return (
        <div className={classnames(className, styles.block)}>
            <div className={styles.letter}>{letter}</div>
        </div>
    )
}