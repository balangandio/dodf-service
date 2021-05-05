export default class DataList {

    constructor(containerElement) {
        this.containerElement = containerElement;
    }

    setResults(requestResult) {
        const documents = (requestResult.result && requestResult.result.documents) || [];
        
        this.containerElement.innerHTML = '';

        documents.forEach(doc => {
            this.containerElement.append(this._createDocument(doc));
        });
    }

    setVisibility(visible) {
        visible
            ? this.containerElement.classList.remove('hided')
            : this.containerElement.classList.add('hided');
    }

    _createDocument(doc) {
        const docContainer = document.createElement('div');
        docContainer.className = 'document-container';

        const titleContainer = document.createElement('div');
        titleContainer.className = 'document-title';
        docContainer.append(titleContainer);
        titleContainer.innerText = doc.document.titulo;

        const contentContainer = document.createElement('div');
        contentContainer.className = 'document-content';
        docContainer.append(contentContainer);
        contentContainer.insertAdjacentHTML('beforeend', doc.document.texto);

        const sentences = this._createSentencesList(doc);
        docContainer.append(sentences);

        return docContainer;
    }

    _createSentencesList({ context }) {
        const { sentences } = context;

        const container = document.createElement('div');
        container.className = 'document-sentences';

        const sentencesToggle = document.createElement('button');
        sentencesToggle.innerText = `Sentenças: ${sentences.length}`;
        sentencesToggle.addEventListener('click', this._onSentenceClick);
        container.append(sentencesToggle);

        const sentenceList = document.createElement('ul');
        sentenceList.style.display = 'none';
        sentences.forEach(sent => {
            sentenceList.append(this._createSentenceItem(sent));
        });
        container.append(sentenceList);

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

    _onSentenceClick(event) {
        const btn = event.target;
        const list =  btn.parentElement.lastElementChild;
        
        if (list.style.display === 'none') {
            list.style.display = 'block';
        } else {
            list.style.display = 'none';
        }
    }
}