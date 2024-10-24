// form-submission-handler.js
import { initializeEventSource } from './event-source-handler.js';
import { createErrorHandler } from './services/error-handler.js';

/**
 * Handles form submission operations and manages the submission lifecycle.
 * Coordinates file uploads and initializes event source connections.
 * @class
 */
export class FormSubmissionHandler {
    /**
     * Creates a FormSubmissionHandler instance.
     * @param {HTMLFormElement} form - The form element to handle
     * @param {string} uploadActionUrl - Endpoint URL for file uploads
     * @param {string} statusActionUrl - Endpoint URL for status updates
     * @param {DOMHandler} domHandler - Handler for DOM operations
     * @throws {Error} If required parameters are missing or invalid
     */
    constructor(form, uploadActionUrl, statusActionUrl, domHandler) {
        this.form = form;
        this.uploadActionUrl = uploadActionUrl;
        this.statusActionUrl = statusActionUrl;
        this.domHandler = domHandler;
        this.errorHandler = createErrorHandler(domHandler);
    }

    /**
     * Submits the form and initializes event source monitoring.
     * @async
     * @returns {Promise<EventSource>} EventSource instance for status monitoring
     * @throws {Error} If form submission fails or event source initialization fails
     */
    async submit() {
        try {
            await this.uploadFormData();
            return initializeEventSource(this.statusActionUrl, this.domHandler);
        } catch (error) {
            this.errorHandler.handleSubmissionError(error);
        }
    }

    /**
     * Uploads form data to the server.
     * @async
     * @private
     * @returns {Promise<void>}
     * @throws {Error} If network request fails or server responds with an error
     */
    async uploadFormData() {
        console.log("Submitting form...");
        console.log("uploadActionUrl:", this.uploadActionUrl);
        
        const formData = new FormData(this.form);
        const response = await fetch(this.uploadActionUrl, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        console.log("Form submitted successfully");
    }

    /**
     * Handles submission errors and updates UI accordingly.
     * @private
     * @param {Error} error - The error that occurred during submission
     * @returns {void}
     */
    handleSubmissionError(error) {
        console.error('Error:', error);
        const errorMessage = error.message || 'An unknown error occurred';
        this.errorHandler.handleSubmissionError(error);
    }
}

/**
 * Factory function to create and submit a form.
 * Maintains backward compatibility with previous implementation.
 * @async
 * @param {HTMLFormElement} form - The form element to submit
 * @param {string} uploadActionUrl - Endpoint URL for file uploads
 * @param {string} statusActionUrl - Endpoint URL for status updates
 * @param {DOMHandler} domHandler - Handler for DOM operations
 * @returns {Promise<EventSource>} EventSource instance for status monitoring
 * @throws {Error} If form submission fails
 */
export async function submitForm(form, uploadActionUrl, statusActionUrl, domHandler) {
    const handler = new FormSubmissionHandler(form, uploadActionUrl, statusActionUrl, domHandler);
    return handler.submit();
}