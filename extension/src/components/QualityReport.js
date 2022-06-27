import styles from './QualityReport.module.css'
import classNames from "classnames";

import {
    letterToColor,
    percentageToQuality,
    qualityToColor,
    qualityToLetter,
    qualityToPercentage
} from '../lib/qualityUtils'
import {useEffect, useState} from "react";

export default function QualityReport({ quality }) {

    const percentage = qualityToPercentage(quality)
    const letter = qualityToLetter(quality)

    const [pointerRotation, setPointerRotation] = useState(0)
    const pointerPercentage = pointerRotation / 3.6

    useEffect(() => {
        const desiredRotation = percentage * 3.6
        const difference = desiredRotation - pointerRotation
        const durationMs = 1500;
        const rotationPerMS = difference / durationMs

        let currRotation = pointerRotation
        let currTime = performance.now()
        let goUp = difference > 0;

        const interval = setInterval(() => {
            if (currRotation === desiredRotation) {
                clearInterval(interval)
                return
            }
            currRotation += rotationPerMS * (performance.now() - currTime)
            currTime = performance.now()
            if ((goUp && currRotation >= desiredRotation) || (!goUp && currRotation <= desiredRotation))
                currRotation = desiredRotation

            setPointerRotation(currRotation)
        }, 10)

        return () => clearInterval(interval)
    }, [quality])



    return (
        <div className={styles.container}>
            <svg className={classNames(styles[letter])} width="100%" height="100%" viewBox="0 0 40 40">
                <CircleSegment fill="#fff"/> {/* hole */}
                <CircleSegment stroke="#d2d3d4"/> {/* backdrop */}

                <CircleSegment stroke={letterToColor('F')} from="0" to="40" dontGoOver={percentage}/>
                <CircleSegment stroke={letterToColor('D')} from="40" to="60" dontGoOver={percentage}/>
                <CircleSegment stroke={letterToColor('C')} from="60" to="70" dontGoOver={percentage}/>
                <CircleSegment stroke={letterToColor('B')} from="70" to="85" dontGoOver={percentage}/>
                <CircleSegment stroke={letterToColor('A')} from="85" to="95" dontGoOver={percentage}/>
                <CircleSegment stroke={letterToColor('A-plus')} from="95" to="100" dontGoOver={percentage}/>



                <g>
                    <text x="50%" y="50%" className={styles.letter}>
                        {letter === "A-plus" ? "A+" : letter}
                    </text>
                    <text x="50%" y="50%" className={styles.percentage}>
                        {percentage + "%"}
                    </text>
                </g>
                <CircleSegment className={styles.mask} stroke="#d2d3d4" from={pointerPercentage} to="100"/> {/* mask */}

                <Pointer color={qualityToColor(percentageToQuality(pointerPercentage))} rotation={pointerRotation} />

            </svg>
        </div>
    )
}


function Pointer({ rotation, color }) {

    return (
        <polygon className={styles.pointer} points="18.5,0 21.5,0 20,2.25" fill={color}
                 style={{transform: `rotate(${rotation}deg)`}}/>
    )
}
function CircleSegment({from = 0, to = 100, dontGoOver, ...props}) {
    // radius for circumference of 100
    // https://heyoka.medium.com/scratch-made-svg-donut-pie-charts-in-html5-2c587e935d72
    if (dontGoOver) {
        to = Math.min(to, dontGoOver)
        from = Math.min(from, dontGoOver)
    }
    return (
        <circle {...props} cx="50%" cy="50%" r="15.91549430918954"
                fill={props.fill || "transparent"}
                strokeWidth="3"
                strokeDasharray={`0 ${from} ${to - from} ${100 - to}`}
                strokeDashoffset="25"
        />
    )
}

