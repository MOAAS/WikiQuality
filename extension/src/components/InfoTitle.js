import styles from "./InfoTitle.module.css";

import ReactTooltip from 'react-tooltip';
import useTextFile from "../hooks/useTextFile";


export default function InfoTitle({ title, infoFile }) {
    const [text] = useTextFile("info/" + infoFile);

    const tooltipId = "info-title-" + title;

    return (
        <div>
            <h3 className={styles.title}>
                <a data-tip data-for={tooltipId}>{title} <img src="/info/icon.svg" alt="info icon" /></a>
            </h3>
            <ReactTooltip id={tooltipId} type="info" effect="solid" className={styles.tooltip} html={true}>
                {text}
            </ReactTooltip>
        </div>
    );
}