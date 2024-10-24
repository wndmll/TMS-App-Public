import { UpdateHandler } from './base-update-handler.js';

export class ProgressBarHandler extends UpdateHandler {
    handle(data) {
        console.log("Handling progress update:", data);
        try {
            let progress = 0;
            
            // Handle different progress data formats
            if (typeof data === 'object') {
                if (data.type === 'progress' && typeof data.progress === 'number') {
                    progress = data.progress;
                } else if (typeof data.message === 'number') {
                    progress = data.message;
                }
            } else if (typeof data === 'number') {
                progress = data;
            }

            // Ensure progress is a valid number between 0 and 100
            progress = Math.min(Math.max(0, progress), 100);

            const progressBar = this.domHandler.elements.progressBarFill;
            if (progressBar) {
                this.domHandler.updateElementStyle(
                    progressBar,
                    'width',
                    `${progress}%`
                );
                console.log(`Progress updated to ${progress}%`);
            } else {
                console.error("Progress bar element not found");
            }
        } catch (error) {
            console.error("Progress update error:", error);
            this.errorHandler.handleUpdateError(`Progress bar update failed: ${error.message}`);
        }
    }
}