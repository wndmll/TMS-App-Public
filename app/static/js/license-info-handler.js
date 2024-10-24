// license-info-handler.js

export class LicenseInfoHandler {
    constructor(elements) {
        this.elements = elements;
    }

    handle(data) {
        console.log("Updating license info:", data);
        if (data.license_plate) {
            this.elements.licenseInfo.textContent = data.license_plate;
        }
        if (data.car_brand) {
            this.elements.brandInfo.textContent = data.car_brand;
        }
    }
}