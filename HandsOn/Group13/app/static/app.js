async function loadLocations() {
    try {
        const response = await fetch("http://localhost:5000/api/locations");
        const locations = await response.json();
        const locationSelect = document.getElementById("locationSelect");

        locations.forEach(location => {
            const option = document.createElement("option");
            option.value = location;  // Asegúrate de que esto es el valor correcto
            option.textContent = location;  // Asegúrate de que esto es el texto correcto
            locationSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error al cargar las ubicaciones:", error);
    }
}

async function loadCameras(location) {
    try {
        const response = await fetch(`http://localhost:5000/api/cameras?location=${encodeURIComponent(location)}`);
        const data = await response.json();
        const cameras = data.cameras;  // Obtener las cámaras
        const typeCount = data.type_count;  // Obtener recuentos por tipo
        const resolutionCount = data.resolution_count;  // Obtener recuentos por resolución
        const zoomCount = data.zoom_count;  // Obtener recuentos por zoom

        const cameraTableBody = document.getElementById("cameraTable").getElementsByTagName("tbody")[0];
        const summaryTableBody = document.getElementById("summaryTable").getElementsByTagName("tbody")[0];

        // Limpiar tablas
        cameraTableBody.innerHTML = "";
        summaryTableBody.innerHTML = "";

        // Añadir cámaras a la tabla
        cameras.forEach(camera => {
            const row = cameraTableBody.insertRow();
            row.insertCell(0).textContent = camera.id;
            row.insertCell(1).textContent = camera.type;
            row.insertCell(2).textContent = camera.resolution;
            row.insertCell(3).textContent = camera.zoom;
            row.insertCell(4).textContent = camera.year;
        });

        // Actualizar resumen
        const cameraCount = cameras.length;
        const level = cameraCount > 10 ? "Alto" : cameraCount > 5 ? "Medio" : "Bajo";

        // Insertar fila del recuento de cámaras
        const summaryRow = summaryTableBody.insertRow();
        summaryRow.insertCell(0).textContent = "Recuento de cámaras";
        summaryRow.insertCell(1).textContent = cameraCount;
        summaryRow.insertCell(2).textContent = level;

        // Función para determinar el nivel
        function getLevel(count) {
            return count > 10 ? "Alto" : count > 5 ? "Medio" : "Bajo";
        }

        // Añadir recuentos por tipo
        Object.entries(typeCount).forEach(([type, count]) => {
            const row = summaryTableBody.insertRow();
            row.insertCell(0).textContent = "Tipo: " + type;
            row.insertCell(1).textContent = count;
            row.insertCell(2).textContent = getLevel(count);  // Determinar el nivel
        });

        // Añadir recuentos por resolución
        Object.entries(resolutionCount).forEach(([resolution, count]) => {
            const row = summaryTableBody.insertRow();
            row.insertCell(0).textContent = "Resolución: " + resolution;
            row.insertCell(1).textContent = count;
            row.insertCell(2).textContent = getLevel(count);  // Determinar el nivel
        });

        // Añadir recuentos por zoom
        Object.entries(zoomCount).forEach(([zoom, count]) => {
            const row = summaryTableBody.insertRow();
            row.insertCell(0).textContent = "Zoom Óptico: " + zoom;
            row.insertCell(1).textContent = count;
            row.insertCell(2).textContent = getLevel(count);  // Determinar el nivel
        });

    } catch (error) {
        console.error("Error al cargar las cámaras:", error);
    }
}




// Cambiar evento para cargar cámaras al cambiar el selector de ubicación
document.getElementById("locationSelect").addEventListener("change", (event) => {
    const selectedLocation = event.target.value;
    loadCameras(selectedLocation);
});

// Cargar ubicaciones al inicio
loadLocations();

