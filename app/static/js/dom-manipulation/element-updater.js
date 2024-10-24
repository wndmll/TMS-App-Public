// dom-manipulation/element-updater.js
import { createErrorHandler } from '../services/error-handler.js';

export class ElementUpdater {
    constructor(domHandler) {
        this.errorHandler = createErrorHandler(domHandler);
    }

    updateContent(element, content) {
        if (element) {
            element.textContent = content;
        } else {
            this.errorHandler.handleDOMError('Attempted to update undefined element');
        }
    }

    updateHTML(element, content) {
        if (element) {
            element.innerHTML = content;
        } else {
            this.errorHandler.handleDOMError('Attempted to update undefined element');
        }
    }

    updateStyle(element, property, value) {
        if (element && element.style) {
            element.style[property] = value;
        } else {
            this.errorHandler.handleDOMError(`Attempted to update style of undefined element or property`);
        }
    }
}