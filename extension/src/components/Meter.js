import styles from './Meter.module.css';

import classNames from "classnames";

export default function Meter({ min, max, value, title, color, steps, stepColors = [] }) {
    const range = max - min;

    let percent = (value - min) / range;
    percent = Math.min(Math.max(percent, 0.0), 1);

    if (percent < 0.01)
        percent = 0; // hide the meter if it's too small
        
    return (
        <div className={styles.container} >

            <p className={styles.title}>{title}</p>

            <div className={styles.meter}>
                <MeterPointer color={color} percent={percent} value={value}/>

                <div style={{ width: percent * 100 + "%", background: color }}
                     className={classNames(styles.fillBar, {[styles.full]: percent >= 0.975})}
                />

                {steps.map((step, index) =>
                    <MeterSeparator key={step} percent={step} meterRange={[min, max]} color={stepColors[index]}/>
                )}
            </div>
        </div>
    )
}


function MeterPointer({ color, percent, value }) {
    return (
        <div className={classNames(styles.pointer)} style={{left: percent * 100 + "%", color: color }}>
            ▲
            <span>{FormatNumber(value)}</span>
        </div>
    )
}


function MeterSeparator({color, percent, meterRange}) {
    const [min, max] = meterRange;
    const range = max - min;
    const value = min + range * percent;

    return (
        <div className={classNames(styles.separator)} style={{left: percent * 100 + "%"}}>
            <div style={{borderColor: color || "transparent" }}/>
            <span style={{ color: color || "initial"}}>{FormatNumber(value)}</span>
        </div>
    )
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