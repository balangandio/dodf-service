export function parseDate(data) {
    if (!data || typeof data !== 'string') {
        throw `Invalid date value [${data}]`;
    }

    const groups = /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/.exec(data);

    if (groups == null) {
        throw `Invalid date value [${data}]`;
    }

    const [_, day, month, year] = groups;

    return `${year}-${month}-${day}`;
}