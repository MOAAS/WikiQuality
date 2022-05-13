import classNames from 'classnames'
import styles from './QualityReport.module.css'

const classnames = require('classnames')

export default function QualityReport({ quality, features }) {

    const percentage = qualityToPercentage(quality)
    const letter = qualityToLetter(quality)

    return (
        <div className={classnames(styles.quality, styles[letter.charAt(0)], { [styles.hasQuality]: !!quality })}>
            <strong className={classnames(styles.letter)}>{letter}</strong>
            <small className={classNames(styles.percentage)}>{"(" + percentage + "%)"}</small>
        </div>
    )
}

function qualityToPercentage(quality) {
    return Math.round(quality * 100)
}

function qualityToLetter(quality) {
    if (quality < 0.4) return "F"
    if (quality < 0.6) return "D"
    if (quality < 0.7) return "C"
    if (quality < 0.85) return "B"
    if (quality < 0.95) return "A"
    return "A+"
}