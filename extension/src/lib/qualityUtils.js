export function qualityToPercentage(quality) {
    return Math.round(quality * 100)
}

export function percentageToQuality(percentage) {
    return percentage / 100
}

export function qualityToLetter(quality) {
    if (quality === null)
        return "?";
    const percentage = qualityToPercentage(quality)

    if (percentage < 40) return "F"
    if (percentage < 60) return "D"
    if (percentage < 70) return "C"
    if (percentage < 85) return "B"
    if (percentage < 95) return "A"
    return "A-plus"
}

export function letterToColor(letter) {
    switch (letter) {
        case "F": return "var(--color-F)"
        case "D": return "var(--color-D)"
        case "C": return "var(--color-C)"
        case "B": return "var(--color-B)"
        case "A": return "var(--color-A)"
        case "A-plus": return "var(--color-A-plus)"
        default: return "black"
    }
}

export function qualityToColor(quality) {
    return letterToColor(qualityToLetter(quality));
}