// license-refactor.js
import { initializeFileInput } from './file-input-handler.js';
import { initializeDOMElements } from './dom-handler.js';
import { EventHandler } from './event-handlers.js';  // Updated import

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM content loaded.");

    const domHandler = initializeDOMElements();
    const elements = domHandler.elements;

    initializeFileInput(elements.fileInput, elements.uploadButton, elements.fileNameDisplay, elements.chooseFileButton);

    if (!elements.uploadMeta) {
        console.error("Upload meta element is missing.");
        return;
    }

    const uploadActionUrl = elements.uploadMeta.dataset.uploadUrl;
    const statusActionUrl = elements.uploadMeta.dataset.statusUrl;

    console.log("Upload action URL:", uploadActionUrl);
    console.log("Status action URL:", statusActionUrl);

    // Create and setup event handler
    const eventHandler = new EventHandler(domHandler, uploadActionUrl, statusActionUrl);
    eventHandler.setupEventListeners();
});