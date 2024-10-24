// dom-handler.js
import { DOM_ELEMENT_IDS, CSS_CLASSES, COLORS, MESSAGES } from './constants.js';
import { ElementUpdater } from './dom-manipulation/element-updater.js';
import { ElementAppender } from './dom-manipulation/element-appender.js';
import { getElement, getElementById } from './dom-manipulation/element-initializer.js';

/**
 * Creates and initializes a DOMHandler instance with required DOM elements.
 * @returns {DOMHandler} A new DOMHandler instance with initialized elements
 * @throws {Error} If required DOM elements are not found
 */
export function initializeDOMElements() {
    const elements = {
        chooseFileButton: getElement(`.${CSS_CLASSES.FILE_INPUT_LABEL}`, this),
        uploadButton: getElementById(DOM_ELEMENT_IDS.UPLOAD_BUTTON, this),
        fileNameDisplay: getElementById(DOM_ELEMENT_IDS.FILE_NAME, this),
        fileInput: getElementById(DOM_ELEMENT_IDS.FILE_INPUT, this),
        statusUpdates: getElementById(DOM_ELEMENT_IDS.STATUS_UPDATES, this),
        licenseInfo: getElementById(DOM_ELEMENT_IDS.LICENSE_INFO, this),
        brandInfo: getElementById(DOM_ELEMENT_IDS.BRAND_INFO, this),
        progressBarFill: getElement(`.${CSS_CLASSES.PROGRESS_BAR_FILL}`, this),
        uploadMeta: getElementById(DOM_ELEMENT_IDS.UPLOAD_META, this),
        form: getElementById(DOM_ELEMENT_IDS.UPLOAD_FORM, this)
    };

    return new DOMHandler(elements);
}

/**
 * Handles DOM manipulation operations and element state management.
 * @class
 */
class DOMHandler {
    /**
     * Creates a DOMHandler instance.
     * @param {Object} elements - Object containing required DOM elements
     * @param {HTMLElement} elements.chooseFileButton - File selection button
     * @param {HTMLElement} elements.uploadButton - Form submission button
     * @param {HTMLElement} elements.fileNameDisplay - Element displaying selected filename
     * @param {HTMLInputElement} elements.fileInput - File input element
     * @param {HTMLElement} elements.statusUpdates - Status message display element
     * @param {HTMLElement} elements.licenseInfo - License information display
     * @param {HTMLElement} elements.brandInfo - Brand information display
     * @param {HTMLElement} elements.progressBarFill - Progress bar element
     * @param {HTMLElement} elements.uploadMeta - Upload metadata container
     * @param {HTMLFormElement} elements.form - Main form element
     */
    constructor(elements) {
        this.elements = elements;
        this.updater = new ElementUpdater(this);
        this.appender = new ElementAppender(this);
    }

    /**
     * Updates the file name display with optional error styling.
     * @param {string} message - Message to display
     * @param {boolean} [isError=false] - Whether to apply error styling
     * @returns {void}
     */
    updateFileNameDisplay(message, isError = false) {
        if (!this.elements.fileNameDisplay) {
            console.error('File name display element is missing');
            return;
        }
        this.updater.updateContent(this.elements.fileNameDisplay, message);
        if (isError) {
            this.updater.updateStyle(this.elements.fileNameDisplay, 'backgroundColor', COLORS.ERROR_BACKGROUND);
        } else {
            this.updater.updateStyle(this.elements.fileNameDisplay, 'backgroundColor', '');
        }
    }

    /**
     * Resets all info fields to their default state.
     * @returns {void}
     */
    resetInfoFields() {
        this.updateElement(this.elements.licenseInfo, '');
        this.updateElement(this.elements.brandInfo, '');
        this.updateElement(this.elements.statusUpdates, MESSAGES.SUBMITTING);
    }

    /**
     * Updates an element's text content.
     * @param {HTMLElement} element - Element to update
     * @param {string} content - New content
     * @returns {void}
     */
    updateElement(element, content) {
        this.updater.updateContent(element, content);
    }

    /**
     * Updates an element's HTML content.
     * @param {HTMLElement} element - Element to update
     * @param {string} content - New HTML content
     * @returns {void}
     */
    updateElementHTML(element, content) {
        this.updater.updateHTML(element, content);
    }

    /**
     * Updates an element's style property.
     * @param {HTMLElement} element - Element to update
     * @param {string} property - CSS property name
     * @param {string} value - New property value
     * @returns {void}
     */
    updateElementStyle(element, property, value) {
        this.updater.updateStyle(element, property, value);
    }

    /**
     * Appends a child element to a parent element.
     * @param {HTMLElement} parentElement - Parent element
     * @param {HTMLElement} childElement - Child element to append
     * @returns {void}
     */
    appendChildElement(parentElement, childElement) {
        this.appender.appendChild(parentElement, childElement);
    }
}

/**
 * Creates an FTP button element with the provided link.
 * @param {string} ftpLink - URL for the FTP link
 * @returns {HTMLAnchorElement} Anchor element containing the FTP button
 */
export function createFTPButton(ftpLink) {
    console.log('Creating FTP button');

    const ftpButton = document.createElement('button');
    ftpButton.textContent = 'Go to FTP';
    ftpButton.classList.add(CSS_CLASSES.BUTTON);

    const ftpLinkElement = document.createElement('a');
    ftpLinkElement.href = ftpLink;
    ftpLinkElement.target = '_blank';
    ftpLinkElement.rel = 'noopener noreferrer';
    ftpLinkElement.appendChild(ftpButton);
    ftpLinkElement.classList.add(CSS_CLASSES.NO_UNDERLINE);

    return ftpLinkElement;
}