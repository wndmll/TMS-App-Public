// update-handlers/process-completion-handler.js
import { UpdateHandler } from './base-update-handler.js';
import { createFTPButton } from '../dom-handler.js';
import { sharedState } from './shared-state.js';

export class ProcessCompletionHandler extends UpdateHandler {
    handle(data) {
        try {
            this.domHandler.updateElementHTML(
                this.domHandler.elements.statusUpdates,
                'Process completed'
            );
            
            if (sharedState.ftpLink) {
                const ftpButton = createFTPButton(sharedState.ftpLink);
                const parentElement = this.domHandler.elements.statusUpdates.parentElement;
                
                if (!parentElement) {
                    throw new Error('Could not find parent element for status-updates');
                }
                parentElement.insertBefore(ftpButton, this.domHandler.elements.statusUpdates.nextSibling);
            }
        } catch (error) {
            this.errorHandler.handleUpdateError(`Process completion failed: ${error.message}`);
        }
    }
}