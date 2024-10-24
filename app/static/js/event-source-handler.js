// event-source-handler.js
import { EventSourceParser } from './event-source-parser.js';
import { EventSourceProcessor } from './event-source-processor.js';
import { handleUpdate } from './update-handlers/index.js';
import { createErrorHandler } from './services/error-handler.js';

/**
 * Manages Server-Sent Events (SSE) connections and event processing.
 * Coordinates parsing and processing of server events for real-time updates.
 * @class
 */
export class EventSourceHandler {
    constructor(statusActionUrl, elements) {
        this.statusActionUrl = statusActionUrl;
        this.elements = elements;
        this.parser = new EventSourceParser();
        this.processor = new EventSourceProcessor();
        this.parser.setErrorHandler(elements);
        this.eventSource = null;
        this.errorHandler = createErrorHandler(elements);
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 3;
    }

    initialize() {
        console.log("Initializing EventSource...");
        try {
            this.eventSource = new EventSource(this.statusActionUrl);
            this.setupEventListeners();
            this.reconnectAttempts = 0;
            return this.eventSource;
        } catch (error) {
            console.error("Error initializing EventSource:", error);
            this.errorHandler.handleConnectionError(error);
            return null;
        }
    }

    setupEventListeners() {
        if (!this.eventSource) return;

        this.eventSource.onmessage = (event) => {
            try {
                this.handleMessage(event);
            } catch (error) {
                console.error("Error handling message:", error);
                this.errorHandler.handleParsingError(error);
            }
        };

        this.eventSource.onerror = (error) => {
            this.handleError(error);
        };

        this.eventSource.onopen = () => {
            console.log("EventSource connection opened");
            this.reconnectAttempts = 0;
        };
    }

    handleMessage(event) {
        try {
            const data = this.parser.parse(event);
            console.log("Parsed event data:", data);

            if (data && data.type === "heartbeat") {
                return; // Ignore heartbeat messages
            }

            if (typeof data === 'object' && data !== null) {
                this.processor.process(data, this.elements, this.eventSource);
            }
        } catch (error) {
            console.error("Error processing message:", error);
            this.errorHandler.handleParsingError(error);
        }
    }

    handleError(error) {
        console.error("EventSource error:", error);
        
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }

        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            setTimeout(() => this.initialize(), 1000 * this.reconnectAttempts);
        } else {
            this.errorHandler.handleConnectionError(error);
        }
    }

    close() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }
}

/**
 * Factory function to create and initialize an EventSource connection.
 * Maintains backward compatibility with previous implementation.
 * @param {string} statusActionUrl - URL endpoint for SSE connection
 * @param {object} elements - DOM elements needed for updates
 * @returns {EventSource} Initialized EventSource instance
 * @throws {Error} If initialization fails
 */
export function initializeEventSource(statusActionUrl, elements) {
    const handler = new EventSourceHandler(statusActionUrl, elements);
    return handler.initialize();
}