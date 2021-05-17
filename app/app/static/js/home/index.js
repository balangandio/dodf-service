import HomeApp from './HomeApp.js';

window.app = new HomeApp();

document.addEventListener('DOMContentLoaded', window.app.init);