import axios from 'axios';

import { useState, useCallback } from 'react';
import styles from "./ScanButton.module.css";

const classnames = require("classnames")

const API_URL = "http://localhost:5000/evaluate";

export default function ScanButton({ title, language, onScanComplete }) {
    const [error, setError] = useState("");

    const [loading, setLoading] = useState(false);



    const scanTitle = useCallback(() => {
        setLoading(true);
        axios.get(`${API_URL}/${title}/${language}`).then(res => {
          console.log(res.data)
          onScanComplete(res.data.quality, res.data.features);
        }).catch(err => {  
          console.log(err);
          setError("Error fetching Wikipedia Page.")
        }).finally(() => setLoading(false))
    }, [title, language, onScanComplete])

    return (
        <div style={{display: "flex"}}>
            <button onClick={scanTitle} className={classnames(styles.button, { [styles.active]: loading })} disabled={loading || !title}>
                {loading ? "Scanning..." : "Scan"}
            </button>
            {error && <p>{error}</p>}
        </div>
    )
}
