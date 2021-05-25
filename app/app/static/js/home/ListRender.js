import { replaceText } from '../util/text.js';
import SentenceList from './SentenceList.js';
import FieldList from './FieldList.js';

export default class ListRender {

    constructor(container) {
        this.container = container;
    }

    renderDocuments(documents, term) {
        this.container.innerHTML = '';

        documents.forEach(doc => {
            this.container.append(this._createDocument(doc, term));
        });
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
        container.className = 'document-context';

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