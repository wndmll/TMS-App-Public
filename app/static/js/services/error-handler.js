// services/error-handler.js
import { ERROR_MESSAGES } from '../constants.js';

export class ErrorHandlingService {
    constructor(domHandler) {
        this.domHandler = domHandler;
    }

    handleDOMError(message, element) {
        const errorMessage = typeof message === 'string' ? message : ERROR_MESSAGES.DOM.UPDATE_FAILED;
        console.error(`DOM Error: ${errorMessage}`);
        if (element) {
            this.domHandler.updateFileNameDisplay(errorMessage, true);
        }
    }

    handleSubmissionError(error) {
        const message = error.message || ERROR_MESSAGES.FORM.SUBMISSION_FAILED;
        console.error('Form Submission Error:', error);
        return this.handleUpdateError(message);
    }

    handleUpdateError(message) {
        const errorMessage = typeof message === 'string' ? message : ERROR_MESSAGES.UPDATE.FAILED('update');
        console.error('Update Error:', errorMessage);
        return this.domHandler.updateElementHTML(
            this.domHandler.elements.statusUpdates,
            `<p>Error: ${errorMessage}</p>`
        );
    }

    handleConnectionError(error) {
        console.error('Connection Error:', error);
        return this.handleUpdateError(ERROR_MESSAGES.CONNECTION.LOST);
    }

    handleParsingError(error, data) {
        console.warn('Parsing Error:', error);
        return { message: ERROR_MESSAGES.PARSE.INVALID_FORMAT };
    }
}

export function createErrorHandler(domHandler) {
    return new ErrorHandlingService(domHandler);
}