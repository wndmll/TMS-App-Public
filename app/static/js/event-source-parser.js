// event-source-parser.js
import { createErrorHandler } from './services/error-handler.js';

/**
 * Parses and validates server-sent events data.
 * Handles JSON parsing and data format validation with error recovery.
 * @class
 */
export class EventSourceParser {
    /**
     * Creates an EventSourceParser instance.
     * ErrorHandler will be initialized later via setErrorHandler.
     */
    constructor() {
        /** @private */
        this.errorHandler = null;
    }

    /**
     * Sets the error handler for the parser.
     * Must be called before parsing operations to enable error handling.
     * @param {Object} domHandler - DOM handler instance for error display
     * @returns {void}
     */
    setErrorHandler(domHandler) {
        this.errorHandler = createErrorHandler(domHandler);
    }

    /**
     * Parses event data from server-sent events.
     * Attempts multiple parsing strategies with error recovery.
     * @param {MessageEvent} event - The event object from EventSource
     * @returns {Object} Parsed data object or error message object
     * @throws {Error} If parsing completely fails and no recovery is possible
     */
    parse(event) {
        console.log("Parsing event data:", event.data);
        let data;

        try {
            // First parsing attempt - direct JSON parse
            data = this.attemptJSONParse(event.data);
        } catch (e) {
            console.warn("First parsing attempt failed:", e);
            if (this.errorHandler) {
                return this.errorHandler.handleParsingError(e, event.data);
            }
            return { message: event.data };
        }

        // Second attempt if data is not an object
        if (typeof data !== "object") {
            try {
                data = this.attemptJSONParse(data);
            } catch (e) {
                console.warn("Second parsing attempt failed:", e);
                if (this.errorHandler) {
                    return this.errorHandler.handleParsingError(e, data);
                }
                return { message: data };
            }
        }

        console.log("Final parsed data:", data);
        return data;
    }

    /**
     * Attempts to parse a string as JSON.
     * @private
     * @param {string} data - The string to parse
     * @returns {Object} Parsed JSON object
     * @throws {Error} If JSON parsing fails
     */
    attemptJSONParse(data) {
        if (typeof data !== 'string') {
            throw new Error('Input must be a string');
        }
        return JSON.parse(data);
    }
}