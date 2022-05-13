import classNames from 'classnames'
import styles from './QualityReport.module.css'
import qualityToLetter from '../langs/qualityToLetter'
const classnames = require('classnames')

export default function QualityReport({ quality }) {

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
