export default class DataRender {

    documents = [];
    term = undefined;

    constructor(containerElement, controlPanel) {
        this.containerElement = containerElement;
        this.controlPanel = controlPanel;
        this.controlPanel.addListener(this._onControlPanelEvent);
    }

    _onControlPanelEvent = (event, state) => {
        this._updateDocumentList(state);
    }

    setResults(requestResult) {
        this.documents = (requestResult.result && requestResult.result.documents) || [];
        this.term = requestResult.term;
        
        this._updateDocumentList(this.controlPanel.getState());
    }

    setVisibility(visible) {
        visible
            ? this.containerElement.classList.remove('hided')
            : this.containerElement.classList.add('hided');
    }

    _updateDocumentList(state) {
        const { filterState } = state;

        const containerList = this.containerElement.querySelector('.data-container-list');

        const documents = this.documents.filter(doc => filterState.isDocumentAccepted(doc));

        const total = this.documents.length;
        const totalVisible = documents.length;

        const render = state.getCurrentRender(containerList);
        render.renderDocuments(documents, this.term);

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

        if (total === 0) {
            totalContainer.parentElement.setAttribute('data-total', total);
        }
    }

}