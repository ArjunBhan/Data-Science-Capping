const APIURL = "http://nicholasblaskey.com:8080/api";

function cleanseUndefined(val) {
    if (val === undefined) {
        return "";
    }
    return val;
}

$.get(APIURL + "/player/season/2019", function(data) {
    for (let i = 0; i < data.length; i++) {
        let rows = "<tr>";

        let playerURL = "specificPlayer.html?id=" + data[i].player_id;        
        let teamURL = "specificTeam.html?id=" + data[i].team_id;
        rows += "<td><a href='" + playerURL + "'>" + data[i].player_id + "</a></td>" +
            "<td>" + data[i].player_name + "</td>"+
            "<td>" + data[i].age + "</td>" +
            "<td>" + data[i].college + "</td>" +
            "<td>" + cleanseUndefined(data[i].draft_round) + "</td>" +
            "<td>" + cleanseUndefined(data[i].draft_number) + "</td> "+
            "<td>" + cleanseUndefined(data[i].draft_year) + "</td>" +
            "<td><a href='" + teamURL + "'>" + data[i].team_id + "</a></td>" +
            "<td>" + data[i].height + "</td>" +
            "<td>" + data[i].weight + "</td>" +
            "<td>" + data[i].player_auto_key + "</td>" +
            "<td>" + data[i].season + "</td>"+
            "<td>" + data[i].season_range + "</td>";
            "<td>" + data[i].season_range + "</td>";
            "<td>" + data[i].season_range + "</td>"+
            "<td><a href='" + teamURL + "'>" + data[i].team_id + "</a></td>" +
            "<td>" + data[i].weight + "</td>";                    
        rows += "</tr>";
        $('#playerTable').append(rows);
    }
    $(document).ready(function() {
            $('#playerTable').DataTable();
        });
    
});

