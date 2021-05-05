export default class AppForm {
    
    constructor(formElement) {
        this.formElement = formElement;
    }

    getInputs() {
        return {
            termo: this.formElement.termo,
            dtInicial: this.formElement.dtInicial,
            dtFinal: this.formElement.dtFinal
        };
    }

    getData() {
        const inputs = this.getInputs();

        return Object.keys(inputs).reduce((obj, key) => (
            { ...obj, [key]: inputs[key].value }
        ), {});
    }

    setEnabled(enabled) {
        enabled
            ? this.formElement.classList.remove('disabled')
            : this.formElement.classList.add('disabled');

        const buttons = this.formElement.getElementsByTagName('button');

        Object.values(this.getInputs())
            .concat(Array.from(buttons))
            .forEach(input => input.disabled = !enabled);
    }
}