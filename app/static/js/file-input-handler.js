// file-input-handler.js
import { COLORS, MESSAGES } from './constants.js';

export class FileInputHandler {
    constructor(fileInput, uploadButton, fileNameDisplay, chooseFileButton) {
        this.fileInput = fileInput;
        this.uploadButton = uploadButton;
        this.fileNameDisplay = fileNameDisplay;
        this.chooseFileButton = chooseFileButton;
        
        this.initialize();
    }

    initialize() {
        this.hideUploadButton();
        this.fileInput.addEventListener('change', (event) => this.handleFileInputChange(event));
    }

    hideUploadButton() {
        this.uploadButton.classList.add('hidden');
    }

    showUploadButton() {
        this.uploadButton.classList.remove('hidden');
        this.uploadButton.style.backgroundColor = COLORS.UPLOAD_BUTTON_BACKGROUND;
    }

    updateFileName(name) {
        this.fileNameDisplay.textContent = name;
    }

    styleChooseFileButton(isInactive) {
        if (isInactive) {
            this.chooseFileButton.style.backgroundColor = COLORS.CHOOSE_FILE_INACTIVE;
            this.chooseFileButton.style.color = COLORS.CHOOSE_FILE_INACTIVE_TEXT;
            this.chooseFileButton.style.border = `1px solid ${COLORS.CHOOSE_FILE_INACTIVE_BORDER}`;
        } else {
            this.chooseFileButton.style.backgroundColor = COLORS.UPLOAD_BUTTON_BACKGROUND;
            this.chooseFileButton.style.color = 'white';
            this.chooseFileButton.style.border = 'none';
        }
    }

    handleFileInputChange(event) {
        const hasFiles = event.target.files.length > 0;
        
        if (hasFiles) {
            this.showUploadButton();
            this.updateFileName(event.target.files[0].name);
            this.styleChooseFileButton(true);
        } else {
            this.hideUploadButton();
            this.updateFileName(MESSAGES.NO_FILE_SELECTED);
            this.styleChooseFileButton(false);
        }
    }
}

// Factory function to maintain backward compatibility
export function initializeFileInput(fileInput, uploadButton, fileNameDisplay, chooseFileButton) {
    return new FileInputHandler(fileInput, uploadButton, fileNameDisplay, chooseFileButton);
}