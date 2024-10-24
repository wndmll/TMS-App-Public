// update-handlers/license-info-handler.js
import { UpdateHandler } from './base-update-handler.js';

export class LicenseInfoHandler extends UpdateHandler {
    handle(data) {
        try {
            console.log("Updating license info:", data);
            if (!data) {
                throw new Error('No data provided for license info update');
            }
            if (data.license_plate) {
                this.domHandler.updateElement(this.domHandler.elements.licenseInfo, data.license_plate);
            }
            if (data.car_brand) {
                this.domHandler.updateElement(this.domHandler.elements.brandInfo, data.car_brand);
            }
        } catch (error) {
            this.errorHandler.handleUpdateError(`License info update failed: ${error.message}`);
        }
    }
}