import axios from 'axios';

import { useState, useCallback } from 'react';
import styles from "./ScanButton.module.css";

const classnames = require("classnames")

function GET_API_URL() {
    if (process.env.NODE_ENV === "development")
        return "http://localhost:5000/evaluate"
    else return "https://wikiquality.fly.dev/evaluate"
}


export default function ScanButton({ title, language, onScanComplete }) {
    const [error, setError] = useState("");

    const [loading, setLoading] = useState(false);

    const scanTitle = useCallback(() => {
        setLoading(true);
        setError("");
        axios.get(`${GET_API_URL()}/${title}/${language}`).then(res => {
          console.log(res.data)
          onScanComplete(res.data.quality, res.data.features);
        }).catch(err => {  
          console.log(err);
          setError("Error fetching Wikipedia Page.")
        }).finally(() => setLoading(false))
    }, [title, language, onScanComplete])

    return (
        <div className={styles.container}>
            <button onClick={scanTitle} className={classnames(styles.button, { [styles.loading]: loading })} disabled={loading || !title}>
                {loading ? "Scanning..." : "Scan"}
            </button>
            {error && <p className={styles.error}>{error}</p>}
        </div>
    )
}
