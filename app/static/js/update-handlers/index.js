import { LicenseInfoHandler } from './license-info-handler.js';
import { FtpInfoHandler } from './ftp-info-handler.js';
import { ProgressBarHandler } from './progress-bar-handler.js';
import { ErrorHandler } from './error-handler.js';
import { ProcessCompletionHandler } from './process-completion-handler.js';
import { TireBrandHandler } from './tire-brand-handler.js';

export function createUpdateHandler(type, domHandler) {
    switch (type) {
        case 'license':
            return new LicenseInfoHandler(domHandler);
        case 'ftp':
            return new FtpInfoHandler(domHandler);
        case 'progress':
            return new ProgressBarHandler(domHandler);
        case 'error':
            return new ErrorHandler(domHandler);
        case 'complete':
            return new ProcessCompletionHandler(domHandler);
        case 'tire_brand':
            return new TireBrandHandler(domHandler);
        default:
            console.warn(`Unknown update type: ${type}`);
            return new UpdateHandler(domHandler);
    }
}

export function handleUpdate(type, data, domHandler) {
    console.log(`Handling update of type: ${type}`, data);
    const handler = createUpdateHandler(type, domHandler);
    return handler.handle(data);
}