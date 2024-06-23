
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
var venues = [
    {venue_name:"Lyle Park Tennis Courts", venue_id:"lyle", latlng:[51.50191898205893, 0.024873357726036438]},
    {venue_name:"Stratford Park Tennis Courts", venue_id:"stratford", latlng:[51.53769599855995, 0.007150123322716152]},
    {venue_name:"Canning Town Recreation Ground Tennis Courts", venue_id:"canning", latlng:[51.51657938280687, 0.028048209830891513]},
    {venue_name:"Royal Victoria Park Tennis Courts", venue_id:"royalvictoria", latlng:[51.49978638111729, 0.06646199108841633]},
];

for (var i=0; i<venues.length; i++){
    let  marker = L.marker(venues[i].latlng, {icon: MarkerIcon})
    .addTo(map)
    .bindTooltip(venues[i].venue_name,{permanent:true})
    .openTooltip()
    .on("click", selectVenue);
    const markerId = "mrkr-"+i
    marker.getElement().setAttribute("id",markerId)

}
console.log(venues)

favs = JSON.parse(localStorage.getItem("favouriteVenues"))

var tBodyRef = document.getElementById('ven-select');
function renderTable(rows){
    for (var i = 0; i < rows.length; i++) {
        const row = rows[i]
        var r = tBodyRef.insertRow();
        const fav = favs.find(o => o.venue_id === row["venue_id"])
        console.log(fav)
        console.log(fav.enabled)
        const isChecked = favs.find(o => o.venue_id === row["venue_id"]).enabled
        var checkbox = document.createElement("INPUT")
        checkbox.setAttribute("type", "checkbox");
        checkbox.setAttribute("id", "slct-"+i);
        checkbox.checked = isChecked
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
    const itemId = e.originalEvent.target
    const intId = itemId.id.split("-")[1]
    console.log(intId)
    var checkbox = document.getElementById("slct-"+intId);
    checkbox.checked = !checkbox.checked 
    var favs = JSON.parse(localStorage.getItem("favouriteVenues"))
    let venue = favs.find(o => o.venue_id === venues[intId].venue_id);
    venue.enabled = checkbox.checked
    localStorage.setItem("favouriteVenues", JSON.stringify(favs))
    console.log(venue)

    // var checkbox = document.getElementById("slct-"+)
    // if (imagePath=="static/css/location-pin.svg"){
    //     e.originalEvent.target.src = "static/css/location-pin-selected.svg"   
    // } else{
    //     e.originalEvent.target.src = "static/css/location-pin.svg"
    // }

}