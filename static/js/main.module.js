

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
    for (val of Object.values(session)) {
        var c = r.insertCell();
        var content = document.createTextNode(val)
        c.appendChild(content);
    }
}

const startInput = document.getElementById('tbl-src-strt');
const venueNameInput = document.getElementById('tbl-src-vn-nm')
const dateInput = document.getElementById('tbl-src-dt')
const endInput = document.getElementById('tbl-src-end')

function filterTable() {
    const venueName = venueNameInput.value
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
        for (val of Object.values(session)) {
            var c = r.insertCell();
            var content = document.createTextNode(val)
            c.appendChild(content);
        }
    }
}
startInput.addEventListener("input", filterTable);
venueNameInput.addEventListener("input", filterTable);