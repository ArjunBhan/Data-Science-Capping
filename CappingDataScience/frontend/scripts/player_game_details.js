const APIURL = "http://nicholasblaskey.com:8080/api";
let searchParams = new URLSearchParams(window.location.search);
let gameID = searchParams.get('id');
let homeTeamName = "Home team";
let awayTeamName = "Away team";

function cleanseUndefined(val) {
    if (val === undefined) {
        return "";
    }
    return val;
}

function replaceBool(val) {
    if (val) {
        return "&#9989;";
    }
    return "";
}

// Add headers to our tables (we do this to avoid repeating
// ourself in the html).
let headers = `<th>Player ID</th>
              <th>Player name</th>
              <th>Did not dress</th>
              <th>Did not play</th>
              <th>Not with team</th>
              <th>Assists</th>
              <th>Blocked shots</th>
              <th>Defensive rebounds</th>
              <th>Field goals attempted</th>
              <th>Field goals made</th>
              <th>Free throws attempted</th>
              <th>Free throws made</th>
              <th>Is top scorer</th>
              <th>Offensive rebounds</th>
              <th>Personal fouls</th>
              <th>Plus minus</th>
              <th>Points</th>
              <th>Seconds played</th>
              <th>Start position</th>
              <th>Steals</th>
              <th>Three pointers attempted</th>
              <th>Three pointers made</th>
              <th>Turnovers</th>`;
$("#homeHeaders").html(headers);
$("#awayHeaders").html(headers);

// First lookup the game.
$.get(APIURL + "/game/" + gameID, function(game) {
    // Look up the teams just for their team name.
    lookupTeams(game);
    
    // Now make the player table.    
    makePlayerTables(game);
});

function lookupTeams(game) {
    let ids = [game.home_team_id, game.away_team_id];

    winnerToString = function(isHome, homeTeamWon) {
        if ((isHome && homeTeamWon) || (!isHome && !homeTeamWon)) {
            return " (Winner of match)";
        }
        return "";
    }

    
    for (let i = 0; i < ids.length; i++) {
        $.get(APIURL + "/team/" + ids[i], function(team) {
            if (i == 0) {                                
                $("#homeTeamName").html("Home team: " + team.nickname +
                                        winnerToString(true, game.home_team_won));
                homeTeamName = team.nickname;
                $("#homeLink").attr("href", "specificTeam.html?id=" + ids[i])
            } else {
                $("#awayTeamName").html("Away team: " + team.nickname +
                                       winnerToString(false, game.home_team_won));
                awayTeamName = team.nickname;
                $("#awayLink").attr("href", "specificTeam.html?id=" + ids[i])
            }
        });
    }
}

function makePlayerTables(game) {
    // Make call to get the game details.
    let players = [];
    $.get(APIURL + "/player_game_details/game/" + gameID, function(details) {
        for (let i = 0; i < details.length; i++) {
            lookupAndAddPlayer(game, players, details, i);
        }
    });
}

function lookupAndAddPlayer(game, players, details, i) {
    // We need to lookup each player to get their name.
    $.get(APIURL + "/player/" + details[i].player_id, function(player) {
        players.push({"player": player, "detail": details[i]});
        
        let playerURL = "specificPlayer.html?id=" + details[i].player_id;        
        let row = "<tr>" +
            "<td><a href='" + playerURL + "'>" + details[i].player_id + "</a></td>" +            
            "<td>" + player[0].player_name + "</td>" +
            "<td>" + replaceBool(details[i].did_not_dress) + "</td>" +
            "<td>" + replaceBool(details[i].did_not_play) + "</td>" +
            "<td>" + replaceBool(details[i].not_with_team) + "</td>"+
            
            "<td>" + cleanseUndefined(details[i].assists) + "</td>" +
            "<td>" + cleanseUndefined(details[i].blocked_shots) + "</td>" +
            "<td>" + cleanseUndefined(details[i].defensive_rebounds) + "</td>" +
            "<td>" + cleanseUndefined(details[i].field_goals_attempted) + "</td>" +
            "<td>" + cleanseUndefined(details[i].field_goals_made) + "</td>" +
            "<td>" + cleanseUndefined(details[i].free_throws_attempted) + "</td>" +
            "<td>" + cleanseUndefined(details[i].free_throws_made) + "</td>"+
            "<td>" + replaceBool(details[i].is_top_scorer) + "</td>" +
            "<td>" + cleanseUndefined(details[i].offensive_rebounds) + "</td>" +
            "<td>" + cleanseUndefined(details[i].personal_fouls) + "</td>" +
            "<td>" + cleanseUndefined(details[i].plus_minus) + "</td>" +
            "<td>" + cleanseUndefined(details[i].points) + "</td>" +
            "<td>" + cleanseUndefined(details[i].seconds_played) + "</td>" +
            "<td>" + cleanseUndefined(details[i].start_position) + "</td>" +
            "<td>" + cleanseUndefined(details[i].steals) + "</td>" +
            "<td>" + cleanseUndefined(details[i].three_pointers_attempted) + "</td>" +
            "<td>" + cleanseUndefined(details[i].three_pointers_made) + "</td>" +
            "<td>" + cleanseUndefined(details[i].turnovers) + "</td>" +
            "</tr>";

        if (details[i].team_id == game.home_team_id) {
            $('#homeTable').append(row);
        } else {
            $('#awayTable').append(row);
        }

        // All done can make our tables into data tables and make our chart.
        if (players.length == details.length) {
            $('#homeTable').DataTable(row);
            $('#awayTable').DataTable(row);
            makeChart(players, game);
        }
    });
}

function makeChart(players, game) {
    // Remove players for the chart who didn't score a point.
    players = players.filter(function(player) {
        return player.detail.points > 0;
    });

    // Sort by points scored.
    players.sort(function(first, second) {
        return first.detail.points < second.detail.points;
    });
    
    let labels = [];
    let home_vals = [];
    let away_vals = [];
    for (let i = 0; i < players.length; i++) {
        labels.push(players[i].player[0].player_name);
        if (players[i].detail.team_id == game.home_team_id) {
            home_vals.push(players[i].detail.points);
            away_vals.push(0);
        } else {
            away_vals.push(players[i].detail.points);
            home_vals.push(0);
        }
    }

    const data = {
        labels: labels,
        datasets: [
            {
                label: homeTeamName,
                data: home_vals,
                backgroundColor: "rgba(31, 120, 180, 0.5)",
                borderColor: "#2166ac",
                borderWidth: 1
            },
            {
                label: awayTeamName,
                data: away_vals,
                backgroundColor: "rgba(106, 61, 154, 0.5)",
                borderColor: "#2d004b",
                borderWidth: 1
            }
        ]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    stacked: true,
                    beginAtZero: true
                },
                xAxes: [{
                    stacked: true,
                    ticks: {
                        beginAtZero: true,
                        autoSkip: false,
                    }
                }],
            }
        },
    };

    document.getElementById("chartContainer").innerHTML = '<canvas class="my-4"' +
        'id="myChart" width="900" height="380"></canvas>';
    var ctx = document.getElementById("myChart");    

    const myChart = new Chart(ctx, config);
    
}
