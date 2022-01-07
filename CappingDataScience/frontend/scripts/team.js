const APIURL = "http://nicholasblaskey.com:8080/api";

$.get(APIURL + "/team", function(data) {
    for (let i = 0; i < data.length; i++) {
        let rows = "<tr>";

        let teamURL = "specificTeam.html?id=" + data[i].team_id;
        console.log(teamURL);
        rows += "<td><a href='" + teamURL + "'>" + data[i].team_id + "</a></td>" +
            "<td>" + data[i].city + "</td>"+
            "<td>" + data[i].nickname + "</td>" +
            "<td>" + data[i].abbreviation + "</td>" +
            "<td>" + data[i].head_coach + "</td>"+
            "<td>" + data[i].manager + "</td>"+
            "<td>" + data[i].owner + "</td>"+
            "<td>" + data[i].max_year_in_nba_champ + "</td>"+
            "<td>" + data[i].min_year_in_nba_champ + "</td>"+
            "<td>" + data[i].players_been_on_team + "</td>";
            
        rows += "</tr>";
        $('#teamTable').append(rows);
    }

    
    $(document).ready(function() {
        $('#teamTable').DataTable();
    } );
});
