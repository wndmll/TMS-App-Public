// updateHandlers/ErrorHandler.js
import { UpdateHandler } from './base-update-handler.js';

export class ErrorHandler extends UpdateHandler {
    handle(message) {
        this.domHandler.updateElementHTML(
            this.domHandler.elements.statusUpdates,
            `<p>Error: ${message}</p>`
        );
    }
}