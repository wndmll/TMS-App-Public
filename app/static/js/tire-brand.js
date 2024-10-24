///tire-brand.js
import { initializeFileInput } from './file-input-handler.js';
import { initializeDOMElements } from './dom-handler.js';
import { EventHandler } from './event-handlers.js';

document.addEventListener('DOMContentLoaded', function () {
    console.log("Tire brand page loaded.");

    const domHandler = initializeDOMElements();
    const elements = domHandler.elements;

    // Update button text for tire brand upload
    if (elements.uploadButton) {
        elements.uploadButton.textContent = 'Upload Tire Brand Image';
    }

    // Initialize with stored license and brand data
    const uploadMeta = document.getElementById('upload-meta');
    if (uploadMeta) {
        const licenseInfo = uploadMeta.dataset.license;
        const brandInfo = uploadMeta.dataset.brand;
        
        if (elements.licenseInfo && licenseInfo) {
            elements.licenseInfo.textContent = licenseInfo;
        }
        if (elements.brandInfo && brandInfo) {
            elements.brandInfo.textContent = brandInfo;
        }
    }

    initializeFileInput(
        elements.fileInput, 
        elements.uploadButton, 
        elements.fileNameDisplay, 
        elements.chooseFileButton
    );

    if (!elements.uploadMeta) {
        console.error("Upload meta element is missing.");
        return;
    }

    const uploadActionUrl = elements.uploadMeta.dataset.uploadUrl;
    const statusActionUrl = elements.uploadMeta.dataset.statusUrl;

    const eventHandler = new EventHandler(domHandler, uploadActionUrl, statusActionUrl);
    eventHandler.setupEventListeners();
});