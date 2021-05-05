import HomeApp from './HomeApp.js';

window.app = new HomeApp();

document.addEventListener('DOMContentLoaded', e => {
    window.app.onFormSubmit(document.querySelector('form'))
});