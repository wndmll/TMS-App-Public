// dom-manipulation/element-initializer.js
import { CSS_CLASSES } from '../constants.js';
import { createErrorHandler } from '../services/error-handler.js';

export function getElement(selector, domHandler) {
    try {
        const element = document.querySelector(selector);
        if (!element) {
            const errorHandler = createErrorHandler(domHandler);
            errorHandler.handleDOMError(`Element not found: ${selector}`);
            throw new Error(`Element not found: ${selector}`);
        }
        return element;
    } catch (error) {
        const errorHandler = createErrorHandler(domHandler);
        errorHandler.handleDOMError(`Error finding element: ${error.message}`);
        throw error;
    }
}

export function getElementById(id, domHandler) {
    try {
        const element = document.getElementById(id);
        if (!element) {
            const errorHandler = createErrorHandler(domHandler);
            errorHandler.handleDOMError(`Element not found with ID: ${id}`);
            throw new Error(`Element not found with ID: ${id}`);
        }
        return element;
    } catch (error) {
        const errorHandler = createErrorHandler(domHandler);
        errorHandler.handleDOMError(`Error finding element by ID: ${error.message}`);
        throw error;
    }
}