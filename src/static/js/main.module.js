
    
function renderPreferences(favs){
    var prefDiv = document.getElementById('preferences');
    for (var i=0; i<favs.length;i++){
        var input_element = document.createElement('input');
        input_element.type = "checkbox"
        input_element.value = favs[i]["venue_id"]
        input_element.id = "ven-"+i
        input_element.checked = favs[i]["enabled"]
        var label_element = document.createElement('label');
        label_element.for = input_element.id 
        label_element.innerText = favs[i]["venue_name"]
        prefDiv.appendChild(input_element)
        prefDiv.appendChild(label_element)
        input_element.addEventListener("change", updateSS);
    }

}
// if unselected just hide the rows but on next reload don't load the 
function updateSS(e){
    var favs = JSON.parse(localStorage.getItem("favouriteVenues"))
    for (var i=0; i<favs.length; i++){
        if (favs[i]["venue_id"]==e.target.value){
            favs[i]["enabled"] = e.target.checked
        }
    }

}

console.log(preferences)
function isFavsValid(){
    try {
        favs = JSON.parse(localStorage.getItem("favouriteVenues"))
    } catch (e){
        return false;
    }
    if ( favs == null && favs == undefined){
        return false
    }
    return true
}

console.log(isFavsValid())
if (! isFavsValid()){
    // take what you have and check if there are keys that are not there
    // var favs = JSON.parse(localStorasessionStoragege.getItem("favouriteVenues"))
    var req = new XMLHttpRequest();
    var url = new URL("/venues", location.origin)
    
    req.open("GET", url, false);
    req.send(null);
    venues_available = JSON.parse(req.responseText);
    for (var i=0; i<venues_available.length; i++){
        venues_available[i]["enabled"] = false
    }
    favs = JSON.stringify(venues_available)
    
    localStorage.setItem("favouriteVenues", favs)
} else {
    // compare both
}
// validation for session storage
favs = JSON.parse(localStorage.getItem("favouriteVenues"))
console.log(favs)
renderPreferences(favs)

var tBodyRef = document.getElementById('ven-sess');
var venue_sess = []


for (var i=0; i< favs.length; i++){
    if (favs[i]["enabled"]){
        var req = new XMLHttpRequest();
        var url = new URL("/GetVenueSessions?venueId="+favs[i]["venue_id"], location.origin)
        
        req.open("GET", url, false);
        req.send(null);
        venue_sess = venue_sess.concat(JSON.parse(req.responseText));
    }

}


function getDateString(value){
    var dt = new Date(value * 1000)
    const dayNames = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
    var dateString = dayNames[dt.getDay()]+", "+dt.getDate()+"/"+(dt.getMonth()+1)+"/"+dt.getFullYear()
    return dateString
}

function getTimeString(startTime, endTime){
    var startTs = new Date(startTime * 1000*60)
    var endTs = new Date(endTime * 1000*60)
    var start = startTs.getUTCHours()+":"+(startTs.getUTCMinutes() < 10 ? '0' : '') + startTs.getMinutes()
    var end = endTs.getUTCHours()+":"+(endTs.getUTCMinutes() < 10 ? '0' : '') + endTs.getMinutes()
    return start + " - " + end
}

function renderTable(rows){
    for (var i = 0; i < rows.length; i++) {
        const row = rows[i]
        var r = tBodyRef.insertRow();
        var values = [row["venue_name"], getDateString(row["date"]),row["court_name"], getTimeString(row["start"], row["end"])]
        for (var j = 0; j<values.length; j++) {
            var c = r.insertCell();
            c.appendChild(document.createTextNode(values[j]));
        }
        var c = r.insertCell();
        var a = document.createElement('a');
        a.innerText = "Book"
        a.title = "Book"
        a.href = row["booking_url"]
        a.target = "_blank"
        // var frm = document.createElement("FORM")
        // frm.action = 
        // var btn = document.createElement("INPUT")
        // btn.type = "submit"
        // btn.target = "_blank"
        // btn.name = "Book"
        // btn.value = "Book"
        // btn.addEventListener("click",openBooking)
        // frm.appendChild(btn)
        c.appendChild(a)
    }
}
{/* <form action="https://google.com">
    <input type="submit" value="Go to Google" />
</form> */}

function openBooking(){
    url = "https://www.google.com"
    window.open(url, "_blank");
}

renderTable(venue_sess)

const startInput = document.getElementById('tbl-src-strt');
const startInputBefore = document.getElementById('tbl-src-strt-bfr');
const venueNameInput = document.getElementById('tbl-src-vn-nm')
const dateInput = document.getElementById('tbl-src-dt')

function filterDate(date, targetDate){
    if (targetDate.length>0) {
        const date1 = new Date(date*1000).toDateString()
        const date2 = new Date(targetDate).toDateString()
        return date1 == date2
    } else {
        return true
    }

}

function filterVenue(rowVal, inputVal){
    if (inputVal.length>0) {
        return rowVal.startsWith(inputVal)
    } else {
        return true
    }

}

function filterAfterTime(rowTime, inputTime){
    
    if (inputTime.length>0) {
        const inpt = Number(inputTime)*60
        return rowTime>=inpt
    } else {
        return true
    }

}

function filterBeforeTime(rowTime, inputTime){
    
    if (inputTime.length>0) {
        const inpt = Number(inputTime)*60
        return rowTime<inpt
    } else {
        return true
    }

}


function filterTable() {
    const inputVenue = venueNameInput.value
    const inputDate = dateInput.value
    const inputStartTime = startInput.value
    const inputStartTimeBefore = startInputBefore.value

    const res = venue_sess.filter((row) => {
        const isDate = filterDate(row['date'], inputDate)
        const isVenue = filterVenue(row['venue_name'], inputVenue)
        const afterTime = filterAfterTime(row['start'], inputStartTime)
        const beforeTime = filterBeforeTime(row['start'], inputStartTimeBefore)
        const condition = [isDate, isVenue, afterTime, beforeTime]
        return condition.every(v => v===true)
        
    })
    var Table = document.getElementById('ven-sess');
    Table.innerHTML = "";

    renderTable(res)
}
startInput.addEventListener("input", filterTable);
startInputBefore.addEventListener("input", filterTable);
dateInput.addEventListener("input", filterTable);
venueNameInput.addEventListener("input", filterTable);
