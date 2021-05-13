class ContextList {
    constructor(listName) {
        this.listName = listName;
    }

    renderToggle() {
        const toggle = document.createElement('button');
        toggle.setAttribute('data-list', this.listName);
        toggle.innerText = 'Toggle';
        toggle.addEventListener('click', evt => 
            this._toggleList(evt));
        
        return toggle;
    }

    renderList() {
        const list = document.createElement('ul');
        list.setAttribute('data-list', this.listName);

        return list;
    }

    _toggleList(evt) {
        const button = evt.target;
        const { parentElement } = button;
        const className = 'active';

        const btnElements = Array.from(parentElement.querySelectorAll('button[data-list]'));
        const listElements = Array.from(parentElement.querySelectorAll('ul[data-list]'));

        btnElements.concat(listElements).forEach(elem => {
            if (elem.getAttribute('data-list') === this.listName) {
                this._toggleClassName(elem, className);
            } else {
                elem.classList.remove(className);
            }
        });
    }

    _toggleClassName(element, className) {
        element.classList.contains(className)
            ? element.classList.remove(className)
            : element.classList.add(className);
    }
}

export class SentenceList extends ContextList {
    constructor(sentences) {
        super('sentences');
        this.sentences = sentences;
    }
    
    renderToggle() {
        const total = this.sentences.length;
        const toggle = super.renderToggle();
        toggle.innerText = `Sentenças: ${total}`;
        if (!total) {
            toggle.setAttribute('disabled', 'true');
        }
        return toggle;
    }

    renderList() {
        const list = super.renderList();

        this.sentences.forEach(sent => {
            list.append(this._createSentenceItem(sent));
        });

        return list;
    }

    _createSentenceItem({ sentence, field, value }) {
        const item = document.createElement('li');

        const sentParagraph = document.createElement('p');
        sentParagraph.innerText = sentence;
        item.append(sentParagraph);

        if (field || value) {
            const fieldList = document.createElement('ul');
            fieldList.className = 'document-sentences-field-list';

            if (field) {
                const fiedItem = document.createElement('li');
                const span = document.createElement('span');
                span.innerText = field;
                fiedItem.append(span);
                fieldList.append(fiedItem);
            }

            if (value) {
                const valueItem = document.createElement('li');
                const span = document.createElement('span');
                span.innerText = value;
                valueItem.append(span);
                fieldList.append(valueItem);
            }

            item.append(fieldList);
        }

        return item;
    }
}

export class FieldList extends ContextList {
    constructor(fields = {}) {
        super('fields');
        this.fields = fields;
    }
    
    renderToggle() {
        const total = Object.keys(this.fields).length;
        const toggle = super.renderToggle();
        toggle.innerText = `Campos: ${total}`;
        if (!total) {
            toggle.setAttribute('disabled', 'true');
        }
        return toggle;
    }

    renderList() {
        const list = super.renderList();

        Object.keys(this.fields).forEach(key => {
            list.append(this._createFieldItem(key, this.fields[key]));
        });

        return list;
    }

    _createFieldItem(fieldName, fieldValue) {
        const item = document.createElement('li');

        const name = document.createElement('span');
        name.innerText = fieldName;
        item.append(name);

        const valueList = document.createElement('ul');

        const renders = {
            'processo': this._renderProcessoItem,
            'signatarios': this._renderSignatarioItem
        };

        Object.keys(renders).forEach(key => {
            if (key === fieldName) {
                renders[key](fieldValue, valueList);
                item.classList.add(key);
            }
        });

        item.append(valueList);

        return item;
    }

    _renderProcessoItem(obj, list) {
        Object.keys(obj).forEach(key => {
            const valueItem = document.createElement('li');
            valueItem.innerText = `[ ${key} ] = ${obj[key]}`;
            list.append(valueItem);
        });
    }

    _renderSignatarioItem(signatarios, list) {
        signatarios.forEach(({ entity, agent }) => {
            const item = document.createElement('li');

            const desc = document.createElement('span');
            desc.innerText = entity;
            item.append(desc);

            const objList = document.createElement('ul');
            const subItem = document.createElement('li');
            subItem.innerText = agent;
            objList.append(subItem);

            item.append(objList);
            list.append(item);
        });
    }
}