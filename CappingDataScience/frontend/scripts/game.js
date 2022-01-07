const APIURL = "http://nicholasblaskey.com:8080/api";

function cleanseUndefined(val) {
    if (val === undefined) {
        return "";
    }
    return val;
}

$.get(APIURL + "/game/2019-07-1/2019-12-01", function(data) {
    for (let i = 0; i < data.length; i++) {
        let gameURL = "player_game_details.html?id=" + data[i].game_id;
        let rows = "<tr>";

        rows += "<td><a href='" + gameURL + "'>" + data[i].game_id + "</a></td>" +
            "<td>" + data[i].game_date + "</td>"+
            "<td>" + data[i].season + "</td>" +
            "<td>" + data[i].home_team_id + "</td>"+
            "<td>" + data[i].away_team_id + "</td>"+
            "<td>" + data[i].home_team_won + "</td>"+
            "<td>" + cleanseUndefined(data[i].away_close) + "</td>" +
            "<td>" + cleanseUndefined(data[i].away_first) + "</td>" +
            "<td>" + cleanseUndefined(data[i].away_fourth) + "</td>"+
            "<td>" + cleanseUndefined(data[i].away_ml) + "</td>"+
            "<td>" + cleanseUndefined(data[i].away_open) + "</td>"+
            "<td>" + cleanseUndefined(data[i].away_second) + "</td>"+
            "<td>" + cleanseUndefined(data[i].away_third) + "</td>"+
            "<td>" + cleanseUndefined(data[i].away_two_h) + "</td>"+
            "<td>" + data[i].away_won_last + "</td>"+
            "<td>" + cleanseUndefined(data[i].home_first) + "</td>"+
            "<td>" + cleanseUndefined(data[i].home_fourth) + "</td>"+
            "<td>" + cleanseUndefined(data[i].home_ml) + "</td>"+
            "<td>" + cleanseUndefined(data[i].home_open) + "</td>"+
            "<td>" + cleanseUndefined(data[i].home_second) + "</td>"+
            "<td>" + cleanseUndefined(data[i].home_third) + "</td>"+
            "<td>" + cleanseUndefined(data[i].home_two_h) + "</td>"+
            "<td>" + cleanseUndefined(data[i].home_won_last) + "</td>";
    
        rows += "</tr>";
        $('#gameTable').append(rows);
    }
    $(document).ready(function() {
        $('#gameTable').DataTable();
    });
});
