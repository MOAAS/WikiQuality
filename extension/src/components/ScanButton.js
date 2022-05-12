import axios from 'axios';

import { useState, useCallback } from 'react';
import styles from "./ScanButton.module.css";

const API_URL = "http://localhost:5000/evaluate/";

export default function ScanButton({ title, onScan }) {
    const [error, setError] = useState("");

    const [loading, setLoading] = useState(false);



    const scanTitle = useCallback(() => {
        setLoading(true);
        axios.get(API_URL + title).then(res => {
        
          console.log(res.data)
          onScan(res.data.quality);
        }).catch(err => {  
          console.log(err);
          setError("Error fetching Wikipedia Page.")
        }).finally(() => setLoading(false))
    }, [title, onScan])


    return (
        <div>
            <button onClick={scanTitle} className={styles.button} disabled={loading || title === null}>
                {loading ? "Scanning..." : "Scan"}
            </button>
            {error && <p>{error}</p>}
        </div>
    )
}
