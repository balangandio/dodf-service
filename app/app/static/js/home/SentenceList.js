import ContextList from './ContextList.js';

export default class SentenceList extends ContextList {
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