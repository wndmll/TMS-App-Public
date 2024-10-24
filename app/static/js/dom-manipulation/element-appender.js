// dom-manipulation/element-appender.js
import { createErrorHandler } from '../services/error-handler.js';

export class ElementAppender {
    constructor(domHandler) {
        this.errorHandler = createErrorHandler(domHandler);
    }

    appendChild(parentElement, childElement) {
        if (parentElement && childElement) {
            parentElement.appendChild(childElement);
        } else {
            this.errorHandler.handleDOMError('Attempted to append child to undefined element');
        }
    }
}