// static/js/map.js

// Initialize the map centered on Madrid
const map = L.map('map').setView([40.4168, -3.7038], 12);

let selectedDistrictVar = "";

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Custom icons for charging points and parkings
const svgIcon = L.icon({
    iconUrl: './static/images/location-dot-solid.svg',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30]
});

const svgIcon2 = L.icon({
    iconUrl: './static/images/location-blue.svg',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30]
});

// Arrays to store markers
let chargingMarkers = [];
let parkingMarkers = [];

// Function to fetch and add charging points to the map
async function fetchChargingPoints(district = null, neighborhood = null) {
    try {
        let url;
        if (neighborhood) {
            url = `/api/neighborhoods-chargepoints?neighborhood=${encodeURIComponent(neighborhood)}`;
        } else if (district) {
            url = `/api/districts-chargepoints?district=${encodeURIComponent(district)}`;
        } else {
            url = '/api/charging_points';
        }
        
        const response = await axios.get(url);
        const data = response.data.results.bindings;

        const coordinatesResponse = await axios.get('/charging-points-coords');
        const coordinatesData = coordinatesResponse.data;

        // Clear previous markers from the map
        chargingMarkers.forEach(marker => map.removeLayer(marker));
        chargingMarkers = [];

        data.forEach(item => {
            const nameCP = item.nameCP.value;
            const nameSt = item.nameSt.value;
            const coordinates = coordinatesData[nameSt];

            if (coordinates) {
                const marker = L.marker([coordinates.latitude, coordinates.longitude], { icon: svgIcon })
                    .bindPopup(`<strong>${nameCP}</strong><br/>${nameSt}`)
                    .on('click', () => showChargingPointDetail(nameCP)); // Click event to show details
                chargingMarkers.push(marker);
            }
        });
        toggleChargingPoints();
    } catch (error) {
        console.error('Error fetching charging points:', error);
    }
}

// Function to fetch and add parkings to the map
async function fetchParking(district = null, neighborhood = null) {
    try {
        let url;
        if (neighborhood) {
            url = `/api/neighborhoods-parkings?neighborhood=${encodeURIComponent(neighborhood)}`;
        } else if (district) {
            url = `/api/districts-parkings?district=${encodeURIComponent(district)}`;
        } else {
            url = '/api/parkings';
        }
        
        const response = await axios.get(url);
        const data = response.data.results.bindings;
    

        const coordinatesResponse = await axios.get('/parking-coords');
        const coordinatesData = coordinatesResponse.data;

        // Clear previous markers from the map
        parkingMarkers.forEach(marker => map.removeLayer(marker));
        parkingMarkers = [];

        data.forEach(item => {
            const nameP = item.nameP ? item.nameP.value : "Unknown Parking";
            const nameSt = item.nameSt ? item.nameSt.value : null;
            const coordinates = coordinatesData[nameSt];

            if (nameSt && coordinates) {
                const marker = L.marker([coordinates.latitude, coordinates.longitude], { icon: svgIcon2 })
                    .bindPopup(`<strong>${nameP}</strong><br/>${nameSt}`)
                    .on('click', () => showParkingDetail(nameP)); // Click event to show details
                parkingMarkers.push(marker);
            }
        });
        toggleParkings();
    } catch (error) {
        console.error('Error fetching parking data:', error);
    }
}

// Function to toggle charging points visibility
function toggleChargingPoints() {
    const showCharging = document.getElementById('show-charging-points').checked;
    chargingMarkers.forEach(marker => {
        if (showCharging) {
            marker.addTo(map);
        } else {
            map.removeLayer(marker);
        }
    });
}

// Function to toggle parking visibility
function toggleParkings() {
    const showParkings = document.getElementById('show-parkings').checked;
    parkingMarkers.forEach(marker => {
        if (showParkings) {
            marker.addTo(map);
        } else {
            map.removeLayer(marker);
        }
    });
}

// Event listeners for checkboxes
document.getElementById('show-charging-points').addEventListener('change', toggleChargingPoints);
document.getElementById('show-parkings').addEventListener('change', toggleParkings);

// Fetches district data for dropdown
async function fetchDistricts() {
    try {
        const response = await axios.get('/api/districts');
        const districts = response.data.results;

        if (Array.isArray(districts)) {
            const districtSelect = document.getElementById('district-select');
            districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district.name;
                option.textContent = district.name;
               
                districtSelect.appendChild(option);
            });

            // Event listener for district selection
            districtSelect.addEventListener('change', async (event) => {
                const selectedDistrict = event.target.value;
                selectedDistrictVar = selectedDistrict;
                
                // Fetch neighborhoods, charging points, and parkings for the selected district
                await fetchNeighborhoods(selectedDistrict);
                await fetchChargingPoints(selectedDistrict);
                await fetchParking(selectedDistrict);
            });
        } else {
            console.error('Error: District response is not an array.', districts);
        }
    } catch (error) {
        console.error('Error fetching districts:', error);
    }
}

// Fetches neighborhoods for a selected district and updates the neighborhood dropdown
async function fetchNeighborhoods(selectedDistrict) {
    try {
        let url;
        if (selectedDistrict != null && selectedDistrict != "") {
            url = `/api/neighborhoods_districts?district_name=${encodeURIComponent(selectedDistrict)}`;
        } else {
            url = `/api/neighborhoods`;
        }
    
        const response = await axios.get(url);
        const neighborhoods = response.data; // This is now an array of neighborhood names

        const neighborhoodSelect = document.getElementById('neighborhood-select');

        // Check if the `select` element exists before modifying it
        if (!neighborhoodSelect) {
            console.error('Error: Neighborhood select element not found in the DOM.');
            return;
        }

        // Clear the `select` options before refilling
        neighborhoodSelect.innerHTML = '<option value="">Select Neighborhood (optional)</option>';

        if (Array.isArray(neighborhoods)) {
            neighborhoods.forEach(neighborhood => {
                const option = document.createElement('option');
                option.value = neighborhood; // Neighborhood name
                option.textContent = neighborhood; // Display text for the option
                neighborhoodSelect.appendChild(option);
            });

            // Event listener for neighborhood selection
            neighborhoodSelect.addEventListener('change', async (event) => {
                const selectedNeighborhood = event.target.value;
                
                if (selectedNeighborhood == "") {
                    // If no neighborhood is selected, reset to district-level data
                    await fetchNeighborhoods(selectedDistrictVar);
                    await fetchChargingPoints(selectedDistrictVar, null);
                    await fetchParking(selectedDistrictVar, null);
                } else {
                    // Fetch data specific to the selected neighborhood
                    await fetchChargingPoints(null, selectedNeighborhood);
                    await fetchParking(null, selectedNeighborhood);
                }
            });
        } else {
            console.error('Error: Neighborhood response is not an array.', neighborhoods);
        }
    } catch (error) {
        console.error('Error fetching neighborhoods:', error);
    }
}

// Function to display details of a selected charging point
async function showChargingPointDetail(chargepointName) {
    try {
        const response = await axios.get(`/api/chargepoint-detail?chargepoint=${encodeURIComponent(chargepointName)}`);
        console.log("Data received for the charging point:", response.data);

        const data = response.data.results.bindings[0]; // Get the first result from the response

        // Assign each field or show "Not available" if data is missing
        const location = data.locationCP ? data.locationCP.value : "Not available";
        const dischargeDate = data.dischargeDate ? data.dischargeDate.value : "Not available";
        const numEquipments = data.numberOfEquipments ? data.numberOfEquipments.value : "Not available";
        const listMennekesKw = data.listMennekesKw ? data.listMennekesKw.value : "Not available";
        const listChademoKw = data.listChademoKw ? data.listChademoKw.value : "Not available";
        const listCcsKw = data.listCcsKw ? data.listCcsKw.value : "Not available";
        const nMennekesConnectors = data.nMennekesConnectors ? data.nMennekesConnectors.value : "Not available";
        const nChademoConnectors = data.nChademoConnectors ? data.nChademoConnectors.value : "Not available";
        const nCcsConnectors = data.nCcsConnectors ? data.nCcsConnectors.value : "Not available";

        // Update the detail box content
        document.getElementById('detail-title').innerText = `Details for ${chargepointName}`;
        document.getElementById('detail-content').innerHTML = `
            <p><strong>Location:</strong> ${location}</p>
            <p><strong>Discharge Date:</strong> ${dischargeDate}</p>
            <p><strong>Number of Equipments:</strong> ${numEquipments}</p>
            <p><strong>Mennekes Power (kW):</strong> ${listMennekesKw}</p>
            <p><strong>Chademo Power (kW):</strong> ${listChademoKw}</p>
            <p><strong>CCS Power (kW):</strong> ${listCcsKw}</p>
            <p><strong>Mennekes Connectors:</strong> ${nMennekesConnectors}</p>
            <p><strong>Chademo Connectors:</strong> ${nChademoConnectors}</p>
            <p><strong>CCS Connectors:</strong> ${nCcsConnectors}</p>
        `;

        document.getElementById('detail-container').style.display = 'block'; // Show the detail box
    } catch (error) {
        console.error('Error fetching chargepoint details:', error);
    }
}

// Function to display details of a selected parking
async function showParkingDetail(parkingName) {
    try {
        const response = await axios.get(`/api/parking-detail?parking=${encodeURIComponent(parkingName)}`);
        console.log("Data received for the parking:", response.data);

        const data = response.data.results.bindings[0]; // Get the first result from the response

        // Assign each field or show "Not available" if data is missing
        const nameP = data.nameP ? data.nameP.value : "Not available";
        const nameSt = data.nameSt ? data.nameSt.value : "Not available";
        const numberOfTotalPlaces = data.numberOfTotalPlaces ? data.numberOfTotalPlaces.value : "Not available";
        const accessibility = data.accessibility ? data.accessibility.value : "Not available";
        const openingHours = data.openingHours ? data.openingHours.value : "Not available";

        // Update the detail box content
        document.getElementById('detail-title').innerText = `Details for ${nameP}`;
        document.getElementById('detail-content').innerHTML = `
            <p><strong>Location:</strong> ${nameSt}</p>
            <p><strong>Total Places:</strong> ${numberOfTotalPlaces}</p>
            <p><strong>Accessibility:</strong> ${accessibility}</p>
            <p><strong>Opening Hours:</strong> ${openingHours}</p>
        `;

        document.getElementById('detail-container').style.display = 'block'; // Show the detail box
    } catch (error) {
        console.error('Error fetching parking details:', error);
    }
}

// Calls fetch functions when the page is fully loaded
window.onload = () => {
    fetchDistricts();
    fetchNeighborhoods();
    fetchChargingPoints();
    fetchParking();
};
