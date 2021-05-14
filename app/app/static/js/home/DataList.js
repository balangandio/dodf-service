import { replaceText } from '../util/text.js';
import SentenceList from './SentenceList.js';
import FieldList from './FieldList.js';

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

        docContainer.append(this._createDocumentContext(doc));

        return docContainer;
    }

    _createDocumentContext({ context }) {
        const { sentences, fields } = context;

        const container = document.createElement('div');
        container.className = 'document-sentences';

        const listRenders = [ new SentenceList(sentences), new FieldList(fields) ];

        listRenders.forEach(render => {
            container.append(render.renderToggle());
        });

        listRenders.forEach(render => {
            container.append(render.renderList());
        });

        return container;
    }

    _highlightedTerm(content, term) {
        return replaceText(content, term, term => {
            return `<span class="highlight">${term}</span>`;
        });
    }
}