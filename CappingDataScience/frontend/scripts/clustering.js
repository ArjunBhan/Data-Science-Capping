import('./chartjs-plugin-datalabels');

//const APIURL = "http://nicholasblaskey.com:8080/api";
const APIURL = "http://nicholasblaskey.com:8080/api";
const BET_AMOUNT = 100;
const NUM_CLUSTERS = 5;

let player_ids = [203497, 1628378, 203954, 203507, 1626164, 1629027, 202710,
                  1628389, 1629029, 2544, 101108, 202695, 202331, 1627759,
                  1628369, 201935, 203999, 203081, 202681, 200768, 201939, 1629627];

Chart.plugins.register(ChartDataLabels);
Chart.helpers.merge(Chart.defaults.global.plugins.datalabels, {
  align: 'top'
});
$("#playerNotFound").hide();

function getColorScale(i) {
    return ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"][i];
}

function getClusters(player_ids, season) {
    $.post(
        {
            url: APIURL + "/model/clustering",
            data: JSON.stringify({
                "player_ids": player_ids,
                "season": season
            }),
            contentType : 'application/json',
        },
        
        function(data) {
            makeClusterGraphs(data.players, data.players_clustered, true);            
            makeClusterGraphs(data.players, data.players_clustered, false);
            // GIVE WARNING for missing players
        });
}

function makeClusterGraphs(players, players_clustered, isOffensive) {
    // Prepare our dataset.
    id_to_name = {};
    for (let i = 0; i < players.length; i++) {
        if (players[i] !== null) {        
            id_to_name[players[i].player_id] = players[i].player_name;
        }
    }
    
    let clusterPoints = [];
    for (let i = 0; i < NUM_CLUSTERS; i++) {
        clusterPoints.push([]);
    }
    
    for (let i = 0; i < players_clustered.length; i++) {        
        if (isOffensive) {        
            clusterPoints[players_clustered[i].offense_label].push({
                x: players_clustered[i].average_points,
                y: players_clustered[i].average_assists,
                label: id_to_name[players_clustered[i].player_id]
            });
        } else {
            clusterPoints[players_clustered[i].defense_label].push({
                x: players_clustered[i].average_steals,
                y: players_clustered[i].average_blocks,
                label: id_to_name[players_clustered[i].player_id]
            });            
        }
    }

    const data = {datasets: []};
    for (let i = 0; i < clusterPoints.length; i++) {
        data.datasets.push({
            label: "Cluster number " + i,
            data: clusterPoints[i],
            backgroundColor: getColorScale(i),
            pointRadius: 5,
            pointHoverRadius: 5            
        });
    }


    let chartName = "Chart";
    let xLab = "Average points per game";
    let yLab = "Average assists per game";
    let xMax = 40;
    let yMax = 8.5;
    if (isOffensive) {
        chartName = "offensive" + chartName;
    } else {
        xLab = "Average steals per game";
        yLab = "Average blocks per game";
        xMax = 2.3;
        yMax = 2.3;
        chartName = "defensive" + chartName;
    }

    // Reset / make canvas object
    // height was 380.
    document.getElementById(chartName + "Container").innerHTML =
        "<canvas class='my-4' id='" + chartName +
        "' width='900' height='200'></canvas>";    
    
    var ctx = document.getElementById(chartName);

    
    const config = {
        type: 'scatter',
        data: data,
        options: {
            scales: {
                xAxes: [{
                    offset: true,
                    padding: 100,
                    position: 'bottom',
                    scaleLabel: {
                        display: true,
                        fontSize: 14,
                        labelString: xLab,
                    },
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: xMax
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        fontSize: 14,
                        labelString: yLab,
                    },
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: yMax
                    }
                }],
            }
        }
    };

    const chart = new Chart(ctx, config);
}

getClusters(player_ids, 2018); 

$("#submitBettingConfig").click(function() {
    $("#playerNotFound").hide();
    
    let season = parseInt($("#seasonInput").val());
    
    // Handle adding players by ID.
    let playerID = parseInt($("#idInput").val());
    if (playerID == playerID) { // Javascript fun. Check if not NAN.
        // Add our ID only if we don't have it in our ids already.
        if (player_ids.indexOf(playerID) == -1) {
            player_ids.push(playerID);
        }
    }

    // Handle adding players by name.
    let name = $("#nameInput").val();
    if (name != "") { 
        $.get(APIURL + "/player/name/" + name)
            .done(function(data) {
                if (player_ids.indexOf(data[0].player_id) == -1) {
                    player_ids.push(data[0].player_id);
                }
                getClusters(player_ids, season); 
            })
            .fail(function() {
                $("#playerNotFound").html("Player not found " + name);
                $("#playerNotFound").show();
                getClusters(player_ids, season); 
            });
    } else {
        // No need to make another request looking up the player
        // by name since we don't have a player by name to add.
        getClusters(player_ids, season); 
    }    
});

