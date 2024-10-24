// constants.js
export const DOM_ELEMENT_IDS = {
    UPLOAD_BUTTON: 'upload-button',
    FILE_NAME: 'file-name',
    FILE_INPUT: 'file-input',
    STATUS_UPDATES: 'status-updates',
    LICENSE_INFO: 'license-info',
    BRAND_INFO: 'brand-info',
    UPLOAD_META: 'upload-meta',
    UPLOAD_FORM: 'upload-form'
};

export const CSS_CLASSES = {
    FILE_INPUT_LABEL: 'file-input-label',
    PROGRESS_BAR_FILL: 'progress-bar-fill',
    HIDDEN: 'hidden',
    BUTTON: 'button',
    NO_UNDERLINE: 'no-underline'
};

export const COLORS = {
    ERROR_BACKGROUND: 'orange',
    UPLOAD_BUTTON_BACKGROUND: '#001233',
    CHOOSE_FILE_INACTIVE: '#ccc',
    CHOOSE_FILE_INACTIVE_TEXT: '#666',
    CHOOSE_FILE_INACTIVE_BORDER: '#999'
};

export const MESSAGES = {
    NO_FILE_SELECTED: 'No file selected',
    SUBMITTING: 'Submitting...',
    CONNECTION_ERROR: 'Connection error. Reconnecting...'
};

export const ERROR_MESSAGES = {
    DOM: {
        ELEMENT_NOT_FOUND: (identifier) => `Element not found: ${identifier}`,
        UPDATE_FAILED: 'Failed to update element',
        INVALID_ELEMENT: 'Invalid or undefined element',
        STYLE_UPDATE_FAILED: 'Failed to update element style'
    },
    FORM: {
        SUBMISSION_FAILED: 'Form submission failed',
        UPLOAD_FAILED: 'File upload failed',
        NO_FILE: 'No file selected',
        INVALID_RESPONSE: (status) => `Server responded with status: ${status}`
    },
    CONNECTION: {
        LOST: 'Connection lost. Attempting to reconnect...',
        FAILED: 'Failed to establish connection',
        TIMEOUT: 'Connection timed out'
    },
    PARSE: {
        INVALID_JSON: 'Invalid JSON data received',
        INVALID_FORMAT: 'Invalid data format',
        MISSING_DATA: 'Required data is missing'
    },
    UPDATE: {
        FAILED: (type) => `Failed to process ${type} update`,
        INVALID_TYPE: 'Invalid update type',
        MISSING_HANDLER: 'No handler available for this update type'
    }
};