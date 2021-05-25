export default class Switch {

    listeners = [];
    activeClassName = 'active';

    constructor(container, { left, right }) {
        this.container = container;
        this.options = { left, right };

        this.element = this._createContainer();
        this.container.append(this.element);

        this.bindOptions(this.options);
    }

    getState() {
        return new SwitchState(this.options);
    }

    addListener(listener) {
        this.listeners.push(listener);
    }

    bindOptions({ left, right }) {
        this.element.innerHTML = '';

        const leftContainer = document.createElement('div');
        leftContainer.setAttribute('data-side', 'left');
        if (left.active) {
            leftContainer.classList.add(this.activeClassName);
        }

        const leftLabel = document.createElement('label');
        leftLabel.innerText = left.name;

        leftContainer.append(leftLabel);
        this.element.append(leftContainer);

        const rightContainer = document.createElement('div');
        rightContainer.setAttribute('data-side', 'right');
        if (right.active) {
            rightContainer.classList.add(this.activeClassName);
        }

        const rightLabel = document.createElement('label');
        rightLabel.innerText = right.name;

        rightContainer.append(rightLabel);
        this.element.append(rightContainer);
    }

    _createContainer() {
        const container = document.createElement('div');
        container.className = 'switch-container';
        container.addEventListener('click', this._onContainerClick);
        return container;
    }

    _onContainerClick = (event) => {
        const left = this.element.querySelector('div[data-side="left"]');
        const right = this.element.querySelector('div[data-side="right"]');

        if (!this.options.left.active && !this.options.right.active) {
            this.options.right.active = true;
        }

        [ [ left, this.options.left ],
        [ right, this.options.right ] ].forEach(([elem, op]) => {
            op.active = !op.active;
            op.active
                ? elem.classList.add(this.activeClassName)
                : elem.classList.remove(this.activeClassName);
        });

        this._emitEvent({ type: 'option-selected' });
    }

    _emitEvent(event) {
        this.listeners.forEach(listener => {
            listener(event, this.getState());
        });
    }

}

export class SwitchOption {
    constructor(name, value, active) {
        this.name = name;
        this.value = value;
        this.active = active;
    }
}

export class SwitchState {
    constructor({ left, right }) {
        this.leftOption = left;
        this.rightOption = right;
    }

    getValue() {
        if (this.leftOption.active) {
            return this.leftOption.value;
        } else if (this.rightOption.active) {
            return this.rightOption.value;
        }

        return null;
    }
}