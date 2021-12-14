import styles from './OldReadabilityReport.module.css';

import InfoTitle from '../components/InfoTitle';

const adjustment = {
    'RARI': -0.5,
    'RCL': 1.5,
    'RFK': 0,
    'RGFI': -3.5,
    'RSG': -1.5,
    'RLWF': -2.5
}

// widths of each grade level group (percentage)
const widths = {
    0: 0,
    1: 12.5,
    5: 35,
    10: 60,
    13: 75,
    14: 85,
    15: 100
}

export default function OldReadabilityReport({ features }) {
    const adjusted = Object.keys(features).reduce((acc, key) => {
        if (!(key in adjustment))
            return acc;
        const value = features[key];
        const adjustedValue = value + adjustment[key];
        return { ...acc, [key]: adjustedValue };
    }, {});

    const average = Object.keys(adjusted).reduce((acc, key) => {
        const value = adjusted[key];
        return acc + value;
    }, 0) / Object.keys(adjusted).length;
    
    

    return (
        <div className={styles.readability}>
            <InfoTitle title="Readability" infoFile="readability.txt" />
            
            <div className={styles.grades}>
                <GradeLevel minLevel={0} maxLevel={1} description="Pre-school"/>
                <GradeLevel minLevel={1} maxLevel={5} description="Elementary School"/>
                <GradeLevel minLevel={5} maxLevel={10} description="Middle School"/>
                <GradeLevel minLevel={10} maxLevel={13} description="High School"/>
                <GradeLevel minLevel={13} maxLevel={14} description="College"/>
                <GradeLevel minLevel={14} maxLevel={15} description="Graduate"/>

                <FillBar readability={average}/>
            </div>
        </div>


    )

}



const FillBar = ({ readability }) => {
    const width = readabilityToPercentage(readability) + "%";
    const background = readabilityToColor(readability);
    
    return (
        <div className={styles.fillBar} style={{ width, background, color: background }}>
            {!isNaN(readability) && (
                <span>
                    <strong>▲</strong> 
                    <strong>{Math.round(readability * 10) / 10}</strong>
                </span>
            )}
        </div>
    )
}

const GradeLevel = ({minLevel, maxLevel, description}) => {
    const from = readabilityToPercentage(minLevel);
    const to = readabilityToPercentage(maxLevel);
    const width = `${to - from}%`;


    let range = `${minLevel} - ${maxLevel - 1}`
    if (maxLevel - 1 === minLevel)
        range = minLevel;
    if (maxLevel === 15)
        range = `${minLevel}+`

    return (
        <div className={styles.level} style={{ width }}>
            <strong className={styles.range}>{range}</strong>
            <small className={styles.description}>{description}</small>

            {minLevel > 0 && (
                <>
                    <small className={styles.up}>{minLevel} <br/> |</small>
                    <small className={styles.down}>|</small>
                </>
            )}
        </div>       
    )
}

function readabilityToPercentage(readability) {
    if (isNaN(readability))
        return 0;

    // keys sorted by numeric value
    let levels = Object.keys(widths).sort((a, b) => parseInt(a) - parseInt(b))
    
    for (let i = 1; i < levels.length; i++) {
        const level = levels[i];
        if (readability < level) {
            // interpolate between previous and this
            const prevLevel = levels[i - 1];
            const prevWidth = widths[prevLevel], currWidth = widths[level];
            const percentThroughLevel = (readability - prevLevel) / (level - prevLevel);
            return percentThroughLevel * (currWidth - prevWidth) + prevWidth;
        }

    }
    return 100;
}

function readabilityToColor(readability) {
    if (readability >= 14)
        return "var(--color-F)"
    if (readability >= 13)
        return "var(--color-D)"
    if (readability >= 10)
        return "var(--color-C)"
    if (readability >= 5)
        return "var(--color-B)"
    if (readability >= 1)
        return "var(--color-A)"
    return "var(--color-A-plus)"
}