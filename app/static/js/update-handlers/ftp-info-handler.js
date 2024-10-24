// update-handlers/ftp-info-handler.js
import { UpdateHandler } from './base-update-handler.js';
import { sharedState } from './shared-state.js';

export class FtpInfoHandler extends UpdateHandler {
    handle(data) {
        try {
            if (!data) {
                throw new Error('No data provided for FTP info update');
            }
            if (data.status === 'uploaded' && data.link) {
                sharedState.ftpLink = data.link;
            }
            if (data.message) {
                this.domHandler.updateElementHTML(
                    this.domHandler.elements.statusUpdates, 
                    `<p>${data.message}</p>`
                );
            }
        } catch (error) {
            this.errorHandler.handleUpdateError(`FTP info update failed: ${error.message}`);
        }
    }
}