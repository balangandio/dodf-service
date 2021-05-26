import FieldList from "../home/FieldList.js";

export default class FieldsRender {

    constructor(container) {
        this.container = container;
    }

    render(fields) {
        const list = new FieldList(fields);

        this.container.innerHTML = '';
        this.container.append(this._renderHeader(fields));
        this.container.append(list.renderList());
    }

    _renderHeader(fields = {}) {
        const total = Object.keys(fields).length;

        const title = document.createElement('p');
        title.innerText = `Campos: ${total}`;

        return title;
    }
}