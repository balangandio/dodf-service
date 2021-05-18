import * as DOMutil from '../util/dom.js';

export default class ContextList {
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
                DOMutil.toggleClassName(className, elem);
            } else {
                elem.classList.remove(className);
            }
        });
    }
}