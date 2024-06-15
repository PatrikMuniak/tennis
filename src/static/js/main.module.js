

const venues = ["lyle", "stratford", "royalvictoria", "canning"]
var tBodyRef = document.getElementById('ven-sess');
var venue_sess = []


for (var i=0; i< venues.length; i++){
    var req = new XMLHttpRequest();
    var url = new URL("/GetVenueSessions?venueId="+venues[i], location.origin)
    
    req.open("GET", url, false);
    req.send(null);
    console.log(venue_sess.length)
    venue_sess = venue_sess.concat(JSON.parse(req.responseText));

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
    console.log(rows.length)
    for (var i = 0; i < rows.length; i++) {
        const row = rows[i]
        var r = tBodyRef.insertRow();
        var values = [row["venue_name"], getDateString(row["date"]),row["court_name"], getTimeString(row["start"], row["end"])]
        for (var j = 0; j<values.length; j++) {
            var c = r.insertCell();
            c.appendChild(document.createTextNode(values[j]));
        }
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
