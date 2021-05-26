import PostApp from './PostApp.js';

window.app = new PostApp();

document.addEventListener('DOMContentLoaded', window.app.init);