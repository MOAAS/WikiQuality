export default function qualityToLetter(quality) {
    if (quality === null)
        return "?";
    if (quality < 0.4) return "F"
    if (quality < 0.6) return "D"
    if (quality < 0.7) return "C"
    if (quality < 0.85) return "B"
    if (quality < 0.95) return "A"
    return "A-plus"
}