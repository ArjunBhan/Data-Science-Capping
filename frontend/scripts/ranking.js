const APIURL = "http://nicholasblaskey.com:8080/api";

$.get(APIURL + "/ranking/2019-07-1/2019-08-01", function(data) {
    for (let i = 0; i < data.length; i++) {
        let rows = "<tr>";

        let teamURL = "specificTeam.html?id=" + data[i].team_id;
        console.log(teamURL);
        rows += "<td>" + data[i].ranking_id + "</td>" +
            "<td><a href='" + teamURL + "'>" + data[i].team_id + "</a></td>" +
            "<td>" + data[i].conference + "</td>" +
            "<td>" + data[i].standings_date + "</td>" +
            "<td>" + data[i].away_record_loses + "</td>" +
            "<td>" + data[i].away_record_wins + "</td>" +
            "<td>" + data[i].home_record_loses + "</td>" +
            "<td>" + data[i].home_record_wins + "</td>" +
            "<td>" + data[i].games_played_season + "</td>" +
            "<td>" + data[i].improved_since_last + "</td>" +
            "<td>" + data[i].losing_games_seasons + "</td>" +
            "<td>" + data[i].winning_games_season + "</td>";

        rows += "</tr>";
        $('#rankingTable').append(rows);
    }
    $(document).ready(function() {
        $('#rankingTable').DataTable();
    });
});


