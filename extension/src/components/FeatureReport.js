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
    const [p25, p33, p50, p75, p99] = iqrs[feature].range;

    const mediumMin = p25;
    const goodMin = p50;

    const min = 0;
    const max = goodMin * 2;

    const range = max - min;


    let color = "var(--color-bad)"
    if (value >= goodMin)
        color = "var(--color-good)";
    else if (value >= mediumMin)
        color = "var(--color-medium)";

    let mediumMinStep = (mediumMin - min) / range;
    let goodMinStep = (goodMin - min) / range;

    const steps = [mediumMinStep, goodMinStep];
    const stepColors = ["var(--color-medium)", "var(--color-good)"];
        
    return (
        <Meter min={min} max={max} title={iqrs[feature].name} value={value} color={color} 
            //steps={[0.05, 0.33, 0.67, 0.95]}
            steps={steps}
            stepColors={stepColors}
        />
    )
}



function GetCategories(features, validList, match) {
    let keys = []
    if (typeof match === "string")
        keys = validList.filter(key => key.startsWith(match));
    else if (Array.isArray(match))
        keys = validList.filter(key => match.includes(key));

    const filtered = {};
    keys.forEach(key => {
        filtered[key] = features[key]
    });
    return filtered;
}
