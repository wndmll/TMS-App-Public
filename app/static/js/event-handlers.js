// event-handlers.js
import { submitForm } from './form-submission-handler.js';
import { MESSAGES } from './constants.js';
import { createErrorHandler } from './services/error-handler.js';

export class EventHandler {
    constructor(domHandler, uploadActionUrl, statusActionUrl) {
        this.domHandler = domHandler;
        this.uploadActionUrl = uploadActionUrl;
        this.statusActionUrl = statusActionUrl;
        this.elements = domHandler.elements;
        this.errorHandler = createErrorHandler(domHandler);
        
        // Store initial data
        this.initialData = {
            license: this.elements.licenseInfo?.textContent || '',
            carBrand: this.elements.brandInfo?.textContent || ''
        };
    }

    handleFormSubmission(event) {
        event.preventDefault();

        try {
            if (!this.elements.fileInput.files.length) {
                this.errorHandler.handleSubmissionError(new Error(MESSAGES.NO_FILE_SELECTED));
                return;
            }

            const selectedFile = this.elements.fileInput.files[0];
            this.domHandler.updateFileNameDisplay(selectedFile.name);
            
            // Don't reset the license and car brand info
            this.domHandler.updateElement(this.elements.statusUpdates, MESSAGES.SUBMITTING);

            submitForm(this.elements.form, this.uploadActionUrl, this.statusActionUrl, this.domHandler)
                .catch(error => {
                    console.error('Form submission error:', error);
                    this.domHandler.updateFileNameDisplay(`Error: ${error.message}`, true);
                });

        } catch (error) {
            this.errorHandler.handleSubmissionError(error);
        }
    }

    /**
     * Sets up event listeners for form interactions.
     * Should be called after instance creation.
     * @returns {void}
     */
    setupEventListeners() {
        this.elements.form.addEventListener('submit', 
            (event) => this.handleFormSubmission(event)
        );
    }
}

export function handleFormSubmission(event, domHandler, uploadActionUrl, statusActionUrl) {
    const handler = new EventHandler(domHandler, uploadActionUrl, statusActionUrl);
    handler.handleFormSubmission(event);
}