// update-handlers/base-update-handler.js
import { createErrorHandler } from '../services/error-handler.js';

export class UpdateHandler {
    constructor(domHandler) {
        this.domHandler = domHandler;
        this.errorHandler = createErrorHandler(domHandler);
    }

    handle(data) {
        this.errorHandler.handleUpdateError("Handler method must be implemented");
        throw new Error("handle method must be implemented");
    }
}