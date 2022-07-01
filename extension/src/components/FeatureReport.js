import styles from './FeatureReport.module.css';

import iqrs from '../lib/iqrs.json'; // not iqr
import InfoTitle from './InfoTitle';
import Meter from "./Meter";

export default function FeatureReport({ features }) {
    if (Object.keys(features).length === 0)
        return null;

    const validFeatures = Object.keys(features).filter(key => iqrs[key]);
    
    //const content = GetCategories(features, validFeatures, 'C');
    //const style = GetCategories(features, validFeatures, 'S');
    //const readability = GetCategories(features, validFeatures, 'R');
    //const history = GetCategories(features, validFeatures, 'H');   

    const relevantFeatures = GetCategories(features, validFeatures, ["CC", "CCC", "CIL", "CI", "CW", "CSN", "HA", "HR"])

    return (
        <div>
            <InfoTitle title="Relevant Features" infoFile="features.txt" />
            
            <div>
                <MeterGroup features={relevantFeatures}/>
                {/* <MeterGroup header="Content" features={content} />
                <MeterGroup header="Style" features={style}/>
                <MeterGroup header="History" features={history}/> */}
            </div>
        </div>
    );
}

function MeterGroup({ features }) {
    return (
        <ul className={styles.category}>
            {Object.keys(features).map(key => (
                <li key={key}>
                    <FeatureMeter feature={key} value={features[key]} />
                </li>
            ))}
        </ul>
    )
}


function FeatureMeter({ feature, value }) {
    if (!iqrs[feature]) {
        console.warn("Feature not found: " + feature);
        return null;
    }
    const [goodMin, goodMax] = iqrs[feature].range;
    const goodRange = goodMax - goodMin;

    const min = Math.max(goodMin - 2 * goodRange, 0);
    const max = goodMax + 0.1 * goodRange;
    const range = max - min;



    const [mediumMin, mediumMax] = [(min + goodMin) / 2, (max + goodMax) / 2];

    let color = "var(--color-bad)"
    if (value >= goodMin && value <= goodMax)
        color = "var(--color-good)";
    else if (value >= mediumMin && value <= mediumMax)
        color = "var(--color-medium)";

    let goodMinStep = (goodMin - min) / range;
    let goodMaxStep = (goodMax - min) / range;



    return (
        <Meter min={min} max={max} title={iqrs[feature].name} value={value} color={color} 
            //steps={[0.05, 0.33, 0.67, 0.95]}
            steps={[goodMinStep, goodMaxStep]}
            stepColors={["var(--color-good)", "var(--color-good)"]}
        />
    )
}



function GetCategories(features, validList, match) {
    let keys = []
    if (typeof match === "string")
        keys = validList.filter(key => key.startsWith(match));
    else if (Array.isArray(match))
        keys = validList.OUTter(key => match.includes(key));

    const filtered = {};
    keys.forEach(key => {
        filtered[key] = features[key]
    });
    return filtered;
}
