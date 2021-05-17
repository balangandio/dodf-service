import { replaceText } from '../util/text.js';
import SentenceList from './SentenceList.js';
import FieldList from './FieldList.js';

export default class DataList {

    documents = [];
    term = undefined;

    constructor(containerElement, fieldFilter) {
        this.containerElement = containerElement;
        this.fieldFilter = fieldFilter;
        this.fieldFilter.addListener(this._onFieldFilterEvent);
    }

    _onFieldFilterEvent = (event, state) => {
        this._updateDocumentList(state);
    }

    setResults(requestResult) {
        this.documents = (requestResult.result && requestResult.result.documents) || [];
        this.term = requestResult.term;
        
        this._updateDocumentList(this.fieldFilter.getState());
    }

    setVisibility(visible) {
        visible
            ? this.containerElement.classList.remove('hided')
            : this.containerElement.classList.add('hided');
    }

    _updateDocumentList(filterState) {
        const containerList = this.containerElement.querySelector('.data-container-list');
        containerList.innerHTML = '';

        const documents = this.documents.filter(doc => filterState.isDocumentAccepted(doc));

        const total = this.documents.length;
        const totalVisible = documents.length;

        documents.forEach(doc => {
            containerList.append(this._createDocument(doc, this.term));
        });

        this._updateTotalIndicator(total, totalVisible);
    }

    _updateTotalIndicator(total, totalVisible) {
        const totalContainer = this.containerElement.querySelector('.total-container');
        totalContainer.innerHTML = '';

        let label = total;

        if (totalVisible < total) {
            label = `${totalVisible} / ${total}`;
        }

        const span = document.createElement('span');
        span.innerText = total > 0 ? `Total: ${label}` : 'Nenhum registro encontrato!';
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