

var req = new XMLHttpRequest();
const url = "http://127.0.0.1:5000/GetVenueSessions"

req.open("GET", url, false);
req.send(null);
const venue_sess = JSON.parse(req.responseText);

var tBodyRef = document.getElementById('ven-sess');
// console.log(venue_sess)




for (var i = 0; i < venue_sess.length; i++) {
    const session = venue_sess[i]
    var r = tBodyRef.insertRow();
    for (var [key, value] of Object.entries(session)) {
        var c = r.insertCell();
        if (key == "date") {
            var dt = new Date(value * 1000)
            const dayNames = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
            var value = dayNames[dt.getDay()]+", "+dt.getDate()+"/"+dt.getMonth()+"/"+dt.getFullYear()
        } else if (key == "start" || key == "end") {
            var ts = new Date(value * 1000*60)
            var value = ts.getHours()+":"+(ts.getMinutes() < 10 ? '0' : '') + ts.getMinutes()
        }
        var content = document.createTextNode(value)
        c.appendChild(content);
    }
}

const startInput = document.getElementById('tbl-src-strt');
const venueNameInput = document.getElementById('tbl-src-vn-nm')
const dateInput = document.getElementById('tbl-src-dt')
const endInput = document.getElementById('tbl-src-end')

function filterTable() {
    const venueName = venueNameInput.value
    const date = dateInput.value
    const res = venue_sess.filter((row) => {
        if (venueName.length>0) {
            return row['venue_name'].startsWith(venueName)
        } else {
            return true
        }
        return false
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
                var value = dayNames[dt.getDay()]+", "+dt.getDate()+"/"+dt.getMonth()+"/"+dt.getFullYear()
            } else if (key == "start" || key == "end") {
                var ts = new Date(value * 1000*60)
                var value = ts.getHours()+":"+(ts.getMinutes() < 10 ? '0' : '') + ts.getMinutes()
            }
            var content = document.createTextNode(value)
            c.appendChild(content);
        }
    }
}
startInput.addEventListener("input", filterTable);
venueNameInput.addEventListener("input", filterTable);