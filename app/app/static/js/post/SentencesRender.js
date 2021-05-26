import SentenceList from "../home/SentenceList.js";

export default class SentencesRender {

    constructor(container) {
        this.container = container;
    }

    render(sentences) {
        const list = new SentenceList(sentences);

        this.container.innerHTML = '';
        this.container.append(this._renderHeader(sentences));
        this.container.append(list.renderList());
    }

    _renderHeader(sentences) {
        const total = sentences.length;

        const title = document.createElement('p');
        title.innerText = `Sentenças: ${total}`;

        return title;
    }
}