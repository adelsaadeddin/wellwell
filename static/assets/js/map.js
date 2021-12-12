const map = L.map('map').setView([39.53793974517628, -117.20214843750001], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const marker = L.marker([39.53793974517628, -117.20214843750001]);
marker.addTo(map)

map.on('click', function (ev) {
    const coordinates = map.mouseEventToLatLng(ev.originalEvent);
    console.log(coordinates);
    marker.setLatLng(coordinates);
    $('#coordinates').html(coordinates.lat + ", " + coordinates.lng);
});

const coordinates = marker._latlng;
$('#coordinates').html(coordinates.lat + ", " + coordinates.lng);

let wells = [];
$("#submit-button").on('click', async function (e) {
    $(this).addClass('submitting');

    const coordinates = marker._latlng;
    const response = await predict(coordinates.lat, coordinates.lng);

    response.result.forEach(cor => {
        L.circle(cor, 512.00, {
            color: 'blue',
            fillColor: 'blue'
        }).addTo(map);
    })

    setTimeout(() => $(this).removeClass('submitting'), 100);
});