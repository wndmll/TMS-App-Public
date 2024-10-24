// event-source-processor.js
import { handleUpdate } from './update-handlers/index.js';
import { createErrorHandler } from './services/error-handler.js';

/**
 * Processes parsed server-sent events and coordinates update handlers.
 * Manages different types of updates (FTP, progress, completion) and their specific handling.
 * @class
 */
export class EventSourceProcessor {
    /**
     * Creates an EventSourceProcessor instance.
     * @param {Object} [options] - Optional configuration for the processor
     * @param {boolean} [options.autoCloseOnComplete=true] - Whether to auto-close EventSource on completion
     */
    constructor(options = { autoCloseOnComplete: true }) {
        this.autoCloseOnComplete = options.autoCloseOnComplete;
    }

    /**
     * Processes event data and routes to appropriate handlers.
     * @param {Object} data - The parsed event data to process
     * @param {string} [data.type] - The type of update (ftp, progress, etc.)
     * @param {string} [data.status] - The status of the update
     * @param {string} [data.message] - The message content
     * @param {Object} elements - DOM elements needed for updates
     * @param {EventSource} eventSource - The active EventSource connection
     * @returns {void}
     * @throws {Error} If processing fails or handler is not found
     */
    process(data, elements, eventSource) {
        try {
            if (this.isFTPProgressUpdate(data)) {
                this.handleProgressUpdate(data, elements);
            } else if (this.isFTPUpdate(data)) {
                this.handleFTPUpdate(data, elements);
            } else if (this.isCompletionUpdate(data)) {
                this.handleCompletionUpdate(data, elements, eventSource);
            } else {
                this.handleGenericUpdate(data, elements);
            }
        } catch (error) {
            console.error('Processing error:', error);
            handleUpdate('error', error.message, elements);
        }
    }

    /**
     * Checks if the update is an FTP progress update.
     * @private
     * @param {Object} data - The event data
     * @returns {boolean} True if this is an FTP progress update
     */
    isFTPProgressUpdate(data) {
        return data.type === 'ftp' && data.status === 'uploading';
    }

    /**
     * Checks if the update is an FTP-related update.
     * @private
     * @param {Object} data - The event data
     * @returns {boolean} True if this is an FTP update
     */
    isFTPUpdate(data) {
        return data.type === 'ftp';
    }

    /**
     * Checks if the update indicates process completion.
     * @private
     * @param {Object} data - The event data
     * @returns {boolean} True if this is a completion update
     */
    isCompletionUpdate(data) {
        return data.status === 'done';
    }

    /**
     * Handles progress-specific updates.
     * @private
     * @param {Object} data - The progress update data
     * @param {Object} elements - DOM elements
     * @returns {void}
     */
    handleProgressUpdate(data, elements) {
        handleUpdate('progress', data.message, elements);
    }

    /**
     * Handles FTP-specific updates.
     * @private
     * @param {Object} data - The FTP update data
     * @param {Object} elements - DOM elements
     * @returns {void}
     */
    handleFTPUpdate(data, elements) {
        handleUpdate('ftp', data, elements);
    }

    /**
     * Handles completion updates and manages EventSource closure.
     * @private
     * @param {Object} data - The completion update data
     * @param {Object} elements - DOM elements
     * @param {EventSource} eventSource - The active EventSource connection
     * @returns {void}
     */
    handleCompletionUpdate(data, elements, eventSource) {
        handleUpdate('complete', data, elements);
        console.log("Process completed. Closing EventSource...");
        if (this.autoCloseOnComplete && eventSource) {
            eventSource.close();
        }
    }

    /**
     * Handles generic updates that don't match specific types.
     * @private
     * @param {Object} data - The update data
     * @param {Object} elements - DOM elements
     * @returns {void}
     */
    handleGenericUpdate(data, elements) {
        handleUpdate(data.type || 'unknown', data, elements);
    }
}