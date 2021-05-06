export function replaceText(content, text, fn_replace) {
    const lowerContent = content.toLowerCase();
    const lowerText = text.toLowerCase();

    let splits = lowerContent.split(lowerText);

    if (splits.length <= 1) {
        return content;
    }
    
    let lastPart = splits[splits.length - 1];
    lastPart = content.substr(content.length - lastPart.length);
    splits = splits.slice(0, splits.length - 1);

    let totalLength = 0;
    let replacedText = '';

    for (let i = 0; i < splits.length; i++) {
        let part = splits[i];

        let unformatedPart = content.substr(totalLength, part.length);

        totalLength += part.length;

        let unformatedText = content.substr(totalLength, text.length);

        totalLength += unformatedText.length;
        replacedText += unformatedPart;
        replacedText += fn_replace(unformatedText);
    }

    replacedText += lastPart;

    return replacedText;
}