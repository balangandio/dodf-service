import FieldFilter from './FieldFilter.js';
import Switch, { SwitchOption } from './Switch.js';
import TableRender from './TableRender.js';
import ListRender from './ListRender.js';

export default class ControlPanel {

    listeners = [];

    constructor(container) {
        this.container = container;
        this.fieldFilter = new FieldFilter(container);
        this.fieldFilter.addListener(this._onFieldFilterEvent);

        this.renderSwitch = new Switch(container, {
            left: new SwitchOption('Lista', ListRender, false),
            right: new SwitchOption('Tabela', TableRender, true)
        });
        this.renderSwitch.addListener(this._onRenderSwitchEvent);
    }

    addListener(listener) {
        this.listeners.push(listener);
    }

    getState() {
        return new PanelState(this.fieldFilter.getState(), this.renderSwitch.getState());
    }

    _onFieldFilterEvent = (event, state) => {
        this._emitEvent({ type: 'filter' });
    }

    _onRenderSwitchEvent = (event, state) => {
        this._emitEvent({ type: 'render-switch' });
    }

    _emitEvent(event) {
        this.listeners.forEach(listener => {
            listener(event, this.getState());
        });
    }

}

class PanelState {
    constructor(filterState, renderSwitchState) {
        this.filterState = filterState;
        this.renderSwitchState = renderSwitchState;
    }

    getCurrentRender(container) {
        const Render = this.renderSwitchState.getValue();
        return new Render(container);
    }
}