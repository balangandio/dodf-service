import { replaceText } from '../util/text.js';

export default class DataList {

    constructor(containerElement) {
        this.containerElement = containerElement;
    }

    setResults(requestResult) {
        const documents = (requestResult.result && requestResult.result.documents) || [];
        const { term } = requestResult;
        
        const containerList = this.containerElement.querySelector('.data-container-list');
        containerList.innerHTML = '';

        documents.forEach(doc => {
            containerList.append(this._createDocument(doc, term));
        });

        this._setTotal(documents.length);
    }

    setVisibility(visible) {
        visible
            ? this.containerElement.classList.remove('hided')
            : this.containerElement.classList.add('hided');
    }

    _setTotal(total) {
        const totalContainer = this.containerElement.querySelector('.total-container');
        totalContainer.innerHTML = '';

        const span = document.createElement('span');
        span.innerText = total > 0 ? `Total: ${total}` : 'Nenhum registro encontrato!';
        totalContainer.append(span);
        totalContainer.setAttribute('data-total', total);
    }

    _createDocument(doc, term) {
        const docContainer = document.createElement('div');
        docContainer.className = 'document-container';

        const titleContainer = document.createElement('div');
        titleContainer.className = 'document-title';
        docContainer.append(titleContainer);
        titleContainer.insertAdjacentHTML(
            'beforeend',
            this._highlightedTerm(doc.document.titulo, term)
        );

        const contentContainer = document.createElement('div');
        contentContainer.className = 'document-content';
        docContainer.append(contentContainer);
        contentContainer.insertAdjacentHTML(
            'beforeend',
            this._highlightedTerm(doc.document.texto, term)
        );

        const sentences = this._createSentencesList(doc);
        docContainer.append(sentences);

        return docContainer;
    }

    _createSentencesList({ context }) {
        const { sentences, fields = {} } = context;
        const fieldsCount = Object.keys(fields).length;

        const container = document.createElement('div');
        container.className = 'document-sentences';

        const sentencesToggle = document.createElement('button');
        sentencesToggle.innerText = `Sentenças: ${sentences.length}`;
        sentencesToggle.addEventListener('click', this._onSentenceClick);
        container.append(sentencesToggle);

        if (fieldsCount) {
            const fieldsToggle = document.createElement('button');
            fieldsToggle.innerText = `Campos: ${Object.keys(fields).length }`;
            fieldsToggle.addEventListener('click', this._onFieldsClick);
            container.append(fieldsToggle);
        }

        const sentenceList = document.createElement('ul');
        sentenceList.setAttribute('data-list', 'sentences');
        sentenceList.style.display = 'none';
        sentences.forEach(sent => {
            sentenceList.append(this._createSentenceItem(sent));
        });
        container.append(sentenceList);

        if (fieldsCount) {
            const fieldsList = document.createElement('ul');
            fieldsList.setAttribute('data-list', 'fields');
            fieldsList.style.display = 'none';
            Object.keys(fields).forEach(key => {
                fieldsList.append(this._createFieldItem(key, fields[key]));
            });
            container.append(fieldsList);
        }

        return container;
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

    _createFieldItem(fieldName, fieldValue) {
        const item = document.createElement('li');

        const name = document.createElement('span');
        name.innerText = fieldName;
        item.append(name);

        const valueList = document.createElement('ul');

        if (fieldName === 'signatarios') {
            fieldValue.forEach(({ entity, agent }) => {
                const item = document.createElement('li');

                const desc = document.createElement('span');
                desc.innerText = entity;
                item.append(desc);

                const objList = document.createElement('ul');
                const subItem = document.createElement('li');
                subItem.innerText = agent;
                objList.append(subItem);

                item.append(objList);
                valueList.append(item);
            });
        } else if (fieldName === 'processo') {
            Object.keys(fieldValue).forEach(key => {
                const valueItem = document.createElement('li');
                valueItem.innerText = `[ ${key} ] = ${fieldValue[key]}`;
                valueList.append(valueItem);
            });
        }

        item.append(valueList);

        return item;
    }

    _onSentenceClick = (event) => {
        this._toggleDataList('sentences', event.target.parentElement);
    }

    _onFieldsClick = (event) => {
        this._toggleDataList('fields', event.target.parentElement);
    }

    _toggleDataList(name, parent) {
        const lists = Array.from(parent.querySelectorAll('ul[data-list]'));
        lists.forEach(list => {
            if (list.getAttribute('data-list') === name) {
                if (list.style.display === 'none') {
                    list.style.display = 'block';
                } else {
                    list.style.display = 'none';
                }
            } else {
                list.style.display = 'none';
            }
        });
    }

    _highlightedTerm(content, term) {
        return replaceText(content, term, term => {
            return `<span class="highlight">${term}</span>`;
        });
    }
}