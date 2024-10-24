import { UpdateHandler } from './base-update-handler.js';

export class TireBrandHandler extends UpdateHandler {
    handle(data) {
        try {
            console.log("Updating tire brand info:", data);
            if (!data) {
                throw new Error('No data provided for tire brand update');
            }

            // Update tire brand info
            const tireBrandElement = document.getElementById('tire-brand-info');
            if (tireBrandElement && data.tire_brand) {
                this.domHandler.updateElement(tireBrandElement, data.tire_brand);
            }

            // Update license and car brand info if provided
            if (data.license_plate) {
                this.domHandler.updateElement(this.domHandler.elements.licenseInfo, data.license_plate);
            }
            if (data.car_brand) {
                this.domHandler.updateElement(this.domHandler.elements.brandInfo, data.car_brand);
            }

            if (data.message) {
                this.domHandler.updateElementHTML(
                    this.domHandler.elements.statusUpdates,
                    `<p>${data.message}</p>`
                );
            }
        } catch (error) {
            this.errorHandler.handleUpdateError(
                `Tire brand update failed: ${error.message}`
            );
        }
    }
}