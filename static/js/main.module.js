

var req = new XMLHttpRequest();
const url = "http://127.0.0.1:5000/GetVenueSessions"

req.open("GET", url, false);
req.send(null);
const venue_sess = JSON.parse(req.responseText);

var tBodyRef = document.getElementById('ven-sess');




for (var i = 0; i < venue_sess.length; i++) {
    const session = venue_sess[i]
    var r = tBodyRef.insertRow();
    for (var [key, value] of Object.entries(session)) {
        var c = r.insertCell();
        if (key == "date") {
            var dt = new Date(value * 1000)
            const dayNames = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
            var value = dayNames[dt.getDay()]+", "+dt.getDate()+"/"+(dt.getMonth()+1)+"/"+dt.getFullYear()
        } else if (key == "start" || key == "end") {
            var ts = new Date(value * 1000*60)
            var value = ts.getUTCHours()+":"+(ts.getUTCMinutes() < 10 ? '0' : '') + ts.getMinutes()
        }
        var content = document.createTextNode(value)
        c.appendChild(content);
    }
}

const startInput = document.getElementById('tbl-src-strt');
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
        console.log(rowTime, inpt, rowTime>=inpt)
        return rowTime>=inpt
    } else {
        return true
    }

}


function filterTable() {
    const inputVenue = venueNameInput.value
    const inputDate = dateInput.value
    const inputStartTime = startInput.value

    const res = venue_sess.filter((row) => {
        console.log(row)
        const isDate = filterDate(row['date'], inputDate)
        const isVenue = filterVenue(row['venue_name'], inputVenue)
        const afterTime = filterAfterTime(row['start'], inputStartTime)
        const condition = [isDate, isVenue, afterTime]
        return condition.every(v => v===true)
        
    })
    var Table = document.getElementById('ven-sess');
    Table.innerHTML = "";

    for (var i = 0; i < res.length; i++) {
        const session = res[i]
        var r = tBodyRef.insertRow();
        for (var [key, value] of Object.entries(session)) {
            var c = r.insertCell();
            if (key == "date") {
                var dt = new Date(value * 1000)
                const dayNames = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
                var value = dayNames[dt.getDay()]+", "+dt.getDate()+"/"+(dt.getMonth()+1)+"/"+dt.getFullYear()
            } else if (key == "start" || key == "end") {
                var ts = new Date(value * 1000 * 60)
                var value = ts.getUTCHours()+":"+(ts.getUTCMinutes() < 10 ? '0' : '') + ts.getMinutes()
            }
            var content = document.createTextNode(value)
            c.appendChild(content);
        }
    }
}
startInput.addEventListener("input", filterTable);
dateInput.addEventListener("input", filterTable);
venueNameInput.addEventListener("input", filterTable);