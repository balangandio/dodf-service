import AppForm from './AppForm.js';
import DataRender from './DataRender.js';
import Api from '../Api.js';
import { parseDate } from '../util/date.js';
import ControlPanel from './ControlPanel.js';

export default class HomeApp {

    api = new Api();

    init = () => {
        const controlsContainer = document.querySelector('.field-filter');
        const dataContainer = document.querySelector('.data-container');

        this.controlPanel = new ControlPanel(controlsContainer);
        this.dataRender = new DataRender(dataContainer, this.controlPanel);

        const form = document.querySelector('form');
        this.onFormSubmit(form);
    }

    async onFormSubmit(formElement, event) {
        event && event.preventDefault();

        const form = new AppForm(formElement);

        form.setEnabled(false);
        this.dataRender.setVisibility(false);
        try {
            const data = this.validateFormData(form.getData());

            const requestResult = await this.api.search(data);

            this.dataRender.setResults(requestResult);
        } catch(err) {
            console.error(err);
            alert(err);
        } finally {
            form.setEnabled(true);
            this.dataRender.setVisibility(true);
        }
    }

    validateFormData({ termo, dtInicial, dtFinal }) {
        if (!termo) {
            throw 'Termo não informado';
        }

        dtInicial = parseDate(dtInicial);
        dtFinal = parseDate(dtFinal);
        
        return { termo, dtInicial, dtFinal };
    }

}