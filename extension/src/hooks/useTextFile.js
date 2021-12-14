import { useState, useEffect } from "react";

export default function useTextFile(fileName) {
    const [text, setText] = useState("");
    const [isLoading, setLoading] = useState(true);


    useEffect(() => {
        setLoading(true);
        fetch(fileName).then(res => res.text()).then(text => {
            setText(text);
        }).catch(err => {
            console.log(err);
            setText("");
        }).finally(() => setLoading(false));
    }, [fileName]);

    return [text, isLoading];
}