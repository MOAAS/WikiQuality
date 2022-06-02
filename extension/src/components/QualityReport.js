import classNames from 'classnames'
import styles from './QualityReport.module.css'
import qualityToLetter from '../lib/qualityToLetter'

import ReactTooltip from 'react-tooltip'

const classnames = require('classnames')

export default function QualityReport({ quality }) {

    const percentage = qualityToPercentage(quality)
    const letter = qualityToLetter(quality) || "?"

    return (
        <div className={classnames(styles.quality, styles[letter.charAt(0)], { [styles.hasQuality]: !!quality })}>
            <strong className={classnames(styles.letter)}>{letter}</strong>
            <small className={classNames(styles.percentage)}>{"(" + percentage + "%)"}</small>

            <a className={styles.disclaimer} data-tip='custom show' data-for="disclaimer" data-event='click focus'>What is this?</a>


            <ReactTooltip id="disclaimer" type="info" effect="solid" className={styles.tooltip} arrowColor="#fff">
                <strong>Disclaimer:</strong> This meter does not aim to assess accuracy of facts stated in Wikipedia articles, but instead measures quality using a Machine Learning approach that combines multiple predefined metrics. This model predicts quality with a mean error of 9%, worse on non-English articles, so these results are meant to be indicators of quality and are not to be taken as flawless ratings. Definitions of quality are based on Wikipedia's <a href='https://en.wikipedia.org/wiki/Wikipedia:Content_assessment'>quality scale</a>.
                {/* Cite paper */}
            </ReactTooltip>
        </div>
    )
}

function qualityToPercentage(quality) {
    return Math.round(quality * 100)
}

