const APIURL = "http://nicholasblaskey.com:8080/api";

let searchParams = new URLSearchParams(window.location.search);
let teamID = searchParams.get('id');

// Get all teams
$.get(APIURL + "/team", function(data) {
    // Find the team of the ID
    let ourTeam = data.find(function(t) {
        return t.team_id == teamID
    });

    // Set our team name to the page.
    $("#teamName").html(ourTeam.nickname);

    let arenaCaps = [];
    let playersBeenOnTeam = [];
    for (let i = 0; i < data.length; i++) {
        arenaCaps.push(data[i].arena_capacity);
        playersBeenOnTeam.push(data[i].players_been_on_team);
    }
    
    makeChart(data, arenaCaps, "Team's arena capacity", "chartContainer0");
    makeChart(data, playersBeenOnTeam, "# Players been on team", "chartContainer1");
});

function makeChart(teams, vals, title, divID) {
    // Prepare data
    let labels = [];
    let colors = [];
    for (let i = 0; i < teams.length; i++) {
        labels.push(teams[i].nickname);
        if (teams[i].team_id != teamID) {
            colors.push("rgba(254, 224, 139, 0.5)"); // Muted
        } else {
            colors.push("rgba(158, 1, 66, 0.5)"); // Highlighted
        }
    }

    
    const data = {
        labels: labels,
        datasets: [{
            label: title,
            data: vals,
            backgroundColor: colors,
            borderColor: colors,
            borderWidth: 1
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                },
                xAxes: [{
                    ticks: {
                        beginAtZero: true,
                        autoSkip: false,
                    }
                }],
            }
        },
    };

    document.getElementById(divID).innerHTML = '<canvas class="my-4"' +
        'id="myChart' + divID + '" width="900" height="380"></canvas>';
    var ctx = document.getElementById("myChart" + divID);    

    const myChart = new Chart(ctx, config);
}

// Get all the players and put them in a table
$.get(APIURL + "/player/team/" + teamID, function(data) {
    for (let i = 0; i < data.length; i++) {
        let playerURL = "specificPlayer.html?id=" + data[i].player_id;                
        let row = "<tr>" +
            "<td><a href='" + playerURL + "'>" + data[i].player_id + "</a></td>" +
            "<td>" + data[i].player_name + "</td>" +
            "<td>" + data[i].season + "</td>" +
            "<td>" + data[i].age + "</td>" +
            "<td>" + data[i].height + "</td>" +
            "<td>" + data[i].weight + "</td>" +
            "</tr>";
        $("#playerTable").append(row);
    }

    $("#playerTable").DataTable();
});


