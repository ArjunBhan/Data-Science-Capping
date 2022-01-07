const APIURL = "http://nicholasblaskey.com:8080/api";

let searchParams = new URLSearchParams(window.location.search);
let playerID = searchParams.get('id');

let seasonSummaries = new Map();

$("#seasonSelect1").change(makeChart);
$("#seasonSelect2").change(makeChart);

// Get information about the player
$.get(APIURL + "/player/" + playerID, function(data) {
    $("#playerName").html(data[0].player_name);
    
    // Get unique and sorted list of seasons played in.
    let seasons = new Set();
    for (let i = 0; i < data.length; i++) {
        seasons.add(data[i].season);        
    }

    makeTeamHistoryTable(data);
    
    let seasons_list = [];
    seasons.forEach(function(v) {
        seasons_list.push(v);
    });
    seasons_list.sort();
    
    // Put these seasons into our select 1.
    for (let i = 0; i < seasons_list.length; i++) {
        $("#seasonSelect1").append(
            "<option value='" + seasons_list[i] + "'>" + seasons_list[i] + "</option>");
    }
    // Copy our select one into select 2.
    $("#seasonSelect2").html($("#seasonSelect1").html());

    // Select the first option for select1 and last for select2.
    $('#seasonSelect1').val(seasons_list[0]).prop('selected', true);
    $('#seasonSelect2').val(seasons_list[seasons_list.length - 1]).prop('selected', true);

    makeChart();
    
    //makeSeasonChart(param, seasons_list[seasons_list.length - 1]);
});

function makeTeamHistoryTable(data) {
    $.get(APIURL + "/team", function(teams) {
        data.sort(function(first, second) {
            return first.season > second.season;
        });
        for (let i = 0; i < data.length; i++) {
            let team = teams.find(function(team) {
                return team.team_id == data[i].team_id;
            })

            let teamURL = "specificTeam.html?id=" + team.team_id;
            let row = "<tr>" +
                "<td>" + data[i].age + "</td>" +
                "<td>" + data[i].season + "</td>" +
                "<td><a href='" + teamURL + "'>" + data[i].team_id + "</a></td>" +
                "<td>" + team.nickname + "</td>" +
                "</tr>"
            $("#teamTable").append(row);

        }
    });
}

let season1 = -1;
let season2 = -1;
let season1Ready = false;
let season2Ready = false;
function makeChart() {    
    // Get our seasons
    season1 = $("#seasonSelect1").val();
    season2 = $("#seasonSelect2").val();

    // Set we are not ready
    season1Ready = false;
    season2Ready = false;
    
    
    // Do we need to get our season summary from the API?
    if (seasonSummaries.has(season1)) {
        season1Ready = true;
    }    
    if (seasonSummaries.has(season2)) {
        season2Ready = true;
    }    

    // Both ready? We are good to go and make our chart.
    if (season1Ready && season2Ready) {
        makeSeasonChart(season1, season2);
        return; 
    }

    // Otherwise get the data for the season(s) we need.
    if (!season1Ready) {
        getSeasonData(season1, 1);
    }
    if (!season2Ready) {
        getSeasonData(season2, 2);
    }
}

function getSeasonData(season, seasonIndex) {
    $.get(APIURL + "/seasonStats/" + playerID + "/" + season, function(data) {
        // Store the data.
        seasonSummaries.set(season, data);

        // Ready our season depending on which season we are getting.
        if (seasonIndex == 1) {
            season1Ready = true;
        } else {
            season2Ready = true;
        }

        // Call our season chart creation if we are ready.
        if (season1Ready && season2Ready) {
            makeSeasonChart(season1, season2);
        }
    })
}

function makeSeasonChart(season1, season2) {
    // Make chart js canvas in the space for divID.
    document.getElementById("chartContainer").innerHTML = '<canvas class="my-4"' +
        'id="myChart" width="900" height="380"></canvas>';
    var ctx = document.getElementById("myChart");

    
    let seasonsDat = [seasonSummaries.get(season1), seasonSummaries.get(season2)];
    let datasets = [];
    let colors = ["rgba(166, 206, 227, 0.2)", "rgba(251, 154, 153, 0.2)"];
    let borderColors = ["rgb(31, 120, 180)", "rgba(227, 26, 28)"];
    let labels = [season1 + "-" + (parseInt(season1) + 1),
                  season2 + "-" + (parseInt(season2) + 1)];
    for (i = 0; i < seasonsDat.length; i++) {
        datasets.push({
            label: labels[i],
            data: [seasonsDat[i].avg_assists, seasonsDat[i].avg_blocked_shots,
                   seasonsDat[i].avg_offensive_rebounds, seasonsDat[i].avg_defensive_rebounds,
                   seasonsDat[i].avg_field_goals_made,
                   seasonsDat[i].avg_free_throws_made,
                   seasonsDat[i].avg_three_pointers_made,
                   seasonsDat[i].avg_personal_fouls, seasonsDat[i].avg_points,
                   seasonsDat[i].avg_plus_minus, seasonsDat[i].avg_turnovers
                  ],
            fill: true,
            backgroundColor: colors[i],
            borderColor: borderColors[i],
            pointBackgroundColor: borderColors[i],
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: borderColors[i]
        });
    }

    let dat = {
        labels: ["Average assists",
                 "Average blocked shots",
                 "Average offensive rebounds",
                 "Average defensive rebounds",
                 "Average field goals made",
                 "Average free throws made",
                 "Average three pointers made",
                 "Average personal fouls",
                 "Average points",
                 "Average plus minus",
                 "Average turnovers"
                ],
        datasets: datasets
    };

    const config = {
        type: 'radar',
        data: dat,
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            }
        },
    };
    
    const myChart = new Chart(ctx, config);    
}
