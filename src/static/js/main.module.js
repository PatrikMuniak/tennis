
    
function renderPreferences(favs){
    var select = document.getElementById('tbl-src-vn-nm');
    for (var i=0; i<favs.length;i++){
        if (favs[i].enabled){
            var opt = document.createElement('option');
            opt.value = favs[i].venue_id;
            opt.innerHTML = favs[i].venue_name;
            select.appendChild(opt);
        }
    }

}


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

if (! isFavsValid()){
    // take what you have and check if there are keys that are not there

    var req = new XMLHttpRequest();
    var url = new URL("/venues", location.origin)
    
    req.open("GET", url, false);
    req.send(null);
    venues_available = JSON.parse(req.responseText);
    for (var i=0; i<venues_available.length; i++){
        venues_available[i]["enabled"] = true
    }
    favs = JSON.stringify(venues_available)
    
    localStorage.setItem("favouriteVenues", favs)
} else {
    // compare both
}
// validation for session storage
favs = JSON.parse(localStorage.getItem("favouriteVenues"))
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
        a.innerHTML = "Book&nbsp;"
        a.title = "Book"
        a.href = row["booking_url"]
        a.target = "_blank"
        a.classList.add("link-body-emphasis", "link-offset-2", "link-underline-opacity-25", "link-underline-opacity-75-hover")

        c.appendChild(a)
    }
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
        return rowVal == inputVal
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
        const isVenue = filterVenue(row['venue_id'], inputVenue)
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
