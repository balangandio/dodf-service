export function isParentInTree(targetElem, parentElem, LOOP_LIMIT = 999999) {
    let element = targetElem;
    let count = 0;

    do {
        if (count++ === LOOP_LIMIT) {
            throw 'Loop limit reached';
        }

        element = element.parentElement;

        if (element === parentElem) {
            return true;
        }
    } while(element !== null);

    return false;
}

export function toggleClassName(className, element) {
    element.classList.contains(className)
        ? element.classList.remove(className)
        : element.classList.add(className);
}