
const map = L.map('map').setView([51.505, 0.024873357726036438], 13);

var Stadia_AlidadeSmooth = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.{ext}', {
	minZoom: 0,
	maxZoom: 20,
	attribution: '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	ext: 'png'
}).addTo(map);

var MarkerIcon = L.icon({
    iconUrl: 'static/css/location-pin.svg',
    iconSize: [36, 36],
    iconAnchor: [18, 35],
    tooltipAnchor: [13, -23],
});
var venues = [];
function retrieveMarkerData(){
    var req = new XMLHttpRequest();
        var url = new URL("/markerData", location.origin)
        
        req.open("GET", url, false);
        req.send(null);
        return JSON.parse(req.responseText);
}

venues = retrieveMarkerData()
var favs = JSON.parse(localStorage.getItem("favouriteVenues"))

for (var i=0; i<venues.length; i++){
    let  marker = L.marker(venues[i].latlng, {icon: MarkerIcon})
    .addTo(map)
    .bindTooltip(venues[i].venue_name,{permanent:true})
    .openTooltip()
    .on("click", selectVenue);
    const markerId = "mrkr-"+i
    
    marker.getElement().setAttribute("id",markerId)
    const enabled = favs.find(o => o.venue_id === venues[i]["venue_id"]).enabled
    if (enabled){
        marker.getElement().classList.add("marker-select")
    }

}


var tBodyRef = document.getElementById('ven-select');
function renderTable(rows){
    for (var i = 0; i < rows.length; i++) {
        const row = rows[i]
        var r = tBodyRef.insertRow();
        const fav = favs.find(o => o.venue_id === row["venue_id"])


        const isChecked = favs.find(o => o.venue_id === row["venue_id"]).enabled
        var checkbox = document.createElement("INPUT")
        checkbox.setAttribute("type", "checkbox");
        checkbox.setAttribute("id", "slct-"+i);
        checkbox.checked = isChecked
        checkbox.addEventListener("change", selectVenue)
        var values = [row["venue_name"]]
        for (var j = 0; j<values.length; j++) {
            var c = r.insertCell();
            c.appendChild(document.createTextNode(values[j]));
        }
        var c = r.insertCell();
        c.appendChild(checkbox)
    }
}
renderTable(venues)

function selectVenue(e){
    const itemId = e.originalEvent!=undefined ? e.originalEvent.target : e.target
    const intId = itemId.id.split("-")[1]

    var favs = JSON.parse(localStorage.getItem("favouriteVenues"))
    let venue = favs.find(o => o.venue_id === venues[intId].venue_id);

    var checkbox = document.getElementById("slct-"+intId);
    checkbox.checked = !venue.enabled
    venue.enabled = checkbox.checked
    localStorage.setItem("favouriteVenues", JSON.stringify(favs))


    var marker = document.getElementById("mrkr-"+intId);
    if (venue.enabled) {

        marker.classList.add("marker-select");
    } else {
        marker.classList.remove("marker-select");
    }


}