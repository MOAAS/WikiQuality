export default function QualityReport({ quality, features }) {

    const percentage = qualityToPercentage(quality)
    const letter = qualityToLetter(percentage)
    const color = letterToColor(quality)


    return (
        <p>
            Quality: {quality}
        </p>


    )
}

function qualityToPercentage(quality) {
    return Math.round(quality * 100)
}

function qualityToLetter(quality) {
    if (quality < 1)
        return "F"
    if (quality < 2)
        return "D"
    if (quality < 3)
        return "C"
    if (quality < 4)
        return "B"
    if (quality < 4.5)
        return "A"
    return "A+"
}


    


function letterToColor(quality) {

}