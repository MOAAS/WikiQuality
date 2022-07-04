import styles from './ReadabilityReport.module.css';

import InfoTitle from '../components/InfoTitle';
import Meter from "./Meter";

const adjustment = {
    'RARI': -0.5,
    'RCL': 1.5,
    'RFK': 0,
    'RGFI': -3.5,
    'RSG': -1.5,
    'RLWF': -2.5
}

export default function ReadabilityReport({ features }) {
    const adjusted = Object.keys(features).reduce((acc, key) => {
        if (!(key in adjustment))
            return acc;
        const value = features[key];
        const adjustedValue = value + adjustment[key];
        return { ...acc, [key]: adjustedValue };
    }, {});

    let average = Object.keys(adjusted).reduce((acc, key) => {
        const value = adjusted[key];
        return acc + value;
    }, 0) / Object.keys(adjusted).length;

    if (isNaN(average))
        average = 0;

    const { color, level } = getReadabilityInfo(average);


    return (
        <div className={styles.container}>
            <InfoTitle title="Readability" infoFile="readability.txt" />

            <strong className={styles.score} style={{color}}>{Math.round(average * 10) / 10}</strong>
            <small className={styles.description}>{level}</small>

            <div style={{ width: "50%" }}>
                <Meter min={0} max={15} value={average} steps={[1/15, 5/15, 10/15, 14/15]} color={color}/>
            </div>
        </div>


    )

}
function getReadabilityInfo(readability) {
    if (readability >= 14)
        return {color: "var(--color-F)", level: "Graduate Level"};
    if (readability >= 13)
        return {color: "var(--color-D)", level: "College Level"};
    if (readability >= 10)
        return {color: "var(--color-D)", level: "High School Level"};
    if (readability >= 5)
        return {color: "var(--color-A)", level: "Middle School Level"};
    if (readability >= 1)
        return {color: "var(--color-A)", level: "Elementary School Level"};
    return {color: "var(--color-A)", level: "Pre-school Level"};
}