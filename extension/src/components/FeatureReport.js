import styles from './FeatureReport.module.css';

import iqrs from '../lib/iqrs.json'; // not iqr

const classnames = require("classnames")

export default function FeatureReport({ features }) {
    if (Object.keys(features).length === 0)
        return null;

    const validFeatures = Object.keys(features).filter(key => iqrs[key]);
    
    const content = GetCategories(features, validFeatures, 'C');
    const style = GetCategories(features, validFeatures, 'S');
    const readability = GetCategories(features, validFeatures, 'R');
    const history = GetCategories(features, validFeatures, 'H');   

    const relevantFeatures = GetCategories(features, validFeatures, ["CC", "CW", "CCC", "CSN", "HA", "HR"])

    return (
        <div className={styles.report}>
            {/* <h2>Features</h2> */}
            <div>
                <MeterGroup header="Features" features={relevantFeatures}/>
                {/* <MeterGroup header="Content" features={content} />
                <MeterGroup header="Style" features={style}/>
                <MeterGroup header="History" features={history}/> */}
            </div>
        </div>
    );
}

function MeterGroup({ header, features}) {
    return (
        <ul className={styles.category}>
            <h3>{header}</h3>
            {Object.keys(features).map(key => <FeatureMeter key={key} feature={key} value={features[key]} />)}
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

    const [mediumMin, mediumMax] = [goodMin - 1 * goodRange, goodMax + 1 * goodRange]; // mediumMin->mediumMax will be 3 * goodRange
    const [min, max] = [goodMin - 1.5 * goodRange, goodMax + 1.5 * goodRange]; // min->max will be 4 * goodRange

    const range = max - min;

    let pointerStyle = "bad"
    if (value >= goodMin && value <= goodMax)
        pointerStyle = "good";
    else if (value >= mediumMin && value <= mediumMax)
        pointerStyle = "medium";

    let percent = (value - min) / range;    
    percent = Math.min(Math.max(percent, 0.05), 0.95); // minimum of 0.05 and maximum of 0.95



    return (
        <li className={styles.meterWrapper} >

            <p className={styles.featureDesc}>{iqrs[feature].name}</p>

            <div className={styles.meter}>
                <MeterPointer style={pointerStyle} percent={percent} value={value}/>
                <div className={styles.q1}/>
                <div className={styles.q2}/>
                <div className={styles.q3}/>
                <div className={styles.q4}/>
                <div className={styles.q5}/>
                <div className={styles.q6}/>

                <MeterSeparator percent={0.125} value={min + 0.125 * range} good={false}/>
                <MeterSeparator percent={0.250} />
                <MeterSeparator percent={0.375} value={goodMin} good={true}/>
                <MeterSeparator percent={0.500} />
                <MeterSeparator percent={0.625} value={goodMax} good={true}/>
                <MeterSeparator percent={0.750} />
                <MeterSeparator percent={0.875} value={max - 0.125 * range} good={false}/>
            </div>
        </li>
    )
}

function MeterPointer({ style, percent, value }) {
    return (
        <div className={classnames(styles.pointer, styles[style])} style={{left: percent * 100 + "%"}}>
            ▲
            <span>{FormatNumber(value)}</span>
        </div>
    )
}




function MeterSeparator({ percent, value, good }) {
        
    return (
        <div className={classnames(styles.separator, {[styles.good]: good, [styles.bad]: !good })} style={{left: percent * 100 + "%"}}>
            {value !== undefined ? <span>{FormatNumber(value)}</span> : null}
        </div>
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

function FormatNumber(value) {
    if (Math.abs(value) > 1000000)
        return Math.round(value / 100000) / 10 + "M";

    if (Math.abs(value) > 1000)
        return Math.round(value / 1000 * 10) / 10 + "k";

    if (Math.abs(value) > 100)
        return Math.round(value)
    if (Math.abs(value) > 10)
        return Math.round(value * 10) / 10;
    if (Math.abs(value) > 1)
        return Math.round(value * 100) / 100;
    return Math.round(value * 1000) / 1000;
}