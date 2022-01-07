const APIURL = "http://nicholasblaskey.com:8080/api";
const BET_AMOUNT = 100;

addTweets($("#numGamesInput").val());

$("#numGamesInput").change(function() {
    let numGames = parseInt($("#numGamesInput").val());
    addTweets(numGames);   
});

function addTweets(numGames) {
    // Add places for tweets if we need to.
    let numRowsAlready = $("#tweetRow").children().length;
    for (let i = numRowsAlready / 2; i < numGames; i++) {
        $("#tweetRow").append(`
            <div class="form-group col-md-2" id="tweetContainerHome` + i + `">
            <textarea class="form-control" id="tweetInputHome` + i + `" rows="3"></textarea>
            <small id="thresholdHelp" class="form-text text-muted">home tweet ` + i + `</small>
            </div>`);
        $("#tweetRow").append(`
            <div class="form-group col-md-2" id="tweetContainerAway` + i + `">
            <textarea class="form-control" id="tweetInputAway` + i + `" rows="3"></textarea>
            <small id="thresholdHelp" class="form-text text-muted">away tweet ` + i + `</small>
            </div>`);
    }

    // Remove places for tweets if we need to.
    console.log(numRowsAlready + "|" + numGames);
    for (let i = numRowsAlready / 2; i > numGames; i--) {
        console.log(i)
        $("#tweetContainerHome" + (i - 1)).remove();
        $("#tweetContainerAway" + (i - 1)).remove();
    }
    
}


function makeChart(starting_money, ending_moneys, ending_moneys_one_agrees,
                   neural_moneys, reinforce_moneys) {
    // Reset canvas object
    document.getElementById("chartContainer").innerHTML = '<canvas class="my-4"' +
        'id="myChart" width="900" height="380"></canvas>';    
    
    var ctx = document.getElementById("myChart");    
    var thresholdValue = 2;

    let labels = [];
    let starting_moneys = [];
    for (let i = 0; i < ending_moneys.length; i++) {
        labels.push(i);
        starting_moneys.push(starting_money);
    }
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {            
            labels: labels,
            datasets: [{
                label: 'Money our ensemble has (both agree)',
                data: ending_moneys,
                borderWidth: 3,
                fill: false,
                borderColor: 'rgba(102, 166, 30, 0.5)',
                borderWidth: 10,
                pointStyle: 4
            },
                       {
                           label: "Money if we didn't bet anything",
                           data: starting_moneys,
                           borderWidth: 3,
                           fill: false,
                           borderColor: 'rgba(27, 158, 119, 0.5)',
                           borderWidth: 10,
                           pointStyle: 0
                       },
                       {
                           label: "Money our ensemble has (either agrees)",
                           data: ending_moneys_one_agrees,
                           borderWidth: 3,
                           fill: false,
                           borderColor: 'rgba(217, 95, 02, 0.5)',
                           borderWidth: 10,
                           pointStyle: 1
                       },
                       {
                           label: "Money our neural has alone",
                           data: neural_moneys,
                           borderWidth: 3,
                           fill: false,
                           borderColor: 'rgba(117, 112, 179, 0.5)',
                           borderWidth: 10,
                           pointStyle: 2
                       },
                       {
                           label: "Money our reinforcement has alone",
                           data: reinforce_moneys,
                           borderWidth: 3,
                           fill: false,
                           borderColor: 'rgba(231, 41, 138, 0.5)',
                           borderWidth: 10,
                           pointStyle: 3
                       }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Total money'
                    }
                }]
            }
        }
    });
}

// Have the report be hidden by default.
$("#bettingBotReport").hide();
$("#hideButton").click(function() {
    $("#bettingBotReport").hide();
    $("#bettingResultTable > tbody:last").children().remove();
});

$("#submitBettingConfig").click(function() {
    // Run betting simulation.
    let numGames = parseInt($("#numGamesInput").val());
    
    let tweets = [];
    for (let i = 0; i < numGames; i++) {
        tweets.push($("#tweetInputHome" + i).val(), $("#tweetInputAway" + i).val());
    }
    console.log(tweets);
    
    let starting_money = parseInt($("#startingMoneyInput").val());
    $.post(
        {
            url: APIURL + "/model/ensemble",
            data: JSON.stringify({
                "starting_money": starting_money,
                "starting_date": $("#startingDateInput").val(),
                "num_games": numGames,
                "tweets": tweets
            }),
            contentType : 'application/json',
        },
        
        function(data) {
            summary = buildBettingTable(data, starting_money,
                                        parseFloat($("#thresholdInput").val()));

            let profit = summary.underdog_profit + summary.favorite_profit;
            
            $('#endingMoney').text(Math.round(summary.ending_money));
            $('#gamesBetOn').text(summary.underdog_bets + summary.favorite_bets);
            $('#profit').text(Math.round(profit));
            $('#profit').css('color', getTextColor(profit));
                        
            $('#underdogBets').text(summary.underdog_bets);
            $('#underdogProfit').text(Math.round(summary.underdog_profit));
            $('#underdogProfit').css('color', getTextColor(summary.underdog_profit));
            
            $('#favoriteBets').text(summary.favorite_bets);
            $('#favoriteProfit').text(Math.round(summary.favorite_profit));
            $('#favoriteProfit').css('color', getTextColor(summary.favorite_profit));

            makeChart(starting_money, summary.ending_moneys,
                      summary.ending_moneys_one_agrees,
                      summary.ending_money_neurals,
                      summary.ending_money_reinforces);

            console.log(summary.ending_moneys_one_agrees);
            
            $("#bettingBotReport").show();
        }        
    );
});

function getTextColor(x) {
    if (x == 0) {
        return "black";
    }    
    if (x > 0) {
        return "green";
    }
    return "red";
}

function buildBettingTable(data, starting_money, threshold) {
    console.log(data);
    console.log(threshold);
    
    let summary = {
        ending_money: starting_money,
        underdog_bets: 0,
        underdog_profit: 0,
        favorite_bets: 0,
        favorite_profit: 0,
        ending_moneys: [starting_money],
        ending_moneys_one_agree: starting_money,
        ending_moneys_one_agrees: [starting_money],
        ending_money_neural: starting_money,
        ending_money_neurals: [starting_money],
        ending_money_reinforce: starting_money,
        ending_money_reinforces: [starting_money]
    }

    
    // Remove any previous rows that may be there from a previous run.
    $("#bettingResultTable > tbody:last").children().remove();    
    for (let i = 0; i < data.games.length; i++) {
        let rows = "<tr>";

        let home_ml = data.games[i].home_ml;
        if (home_ml > 0) {
            home_ml = "+" + home_ml
        }
        let away_ml = data.games[i].away_ml;
        if (away_ml > 0) {
            away_ml = "+" + away_ml
        }

        let game_profit_loss = 0;
        if (data.betting_bot_bet_on_games[i*2]) {
            let bet_return = getReturn(data.games[i].home_ml,
                                    data.games[i].home_team_won) - BET_AMOUNT;
            game_profit_loss += bet_return;

            if (data.games[i].home_ml < 0) { // Is favorite.
                summary.favorite_bets += 1;
                summary.favorite_profit += bet_return;
            } else { // Is underdog?
                summary.underdog_bets += 1;
                summary.underdog_profit += bet_return;
            }
        }
        if (data.betting_bot_bet_on_games[i*2 + 1]) {
            let bet_return = getReturn(data.games[i].away_ml,
                                    !data.games[i].home_team_won) - BET_AMOUNT;
            game_profit_loss += bet_return;

            if (data.games[i].away_ml < 0) { // Is favorite?
                summary.favorite_bets += 1;
                summary.favorite_profit += bet_return;
            } else { // Is underdog?
                summary.underdog_bets += 1;
                summary.underdog_profit += bet_return;
            }
        }

        // One agree
        if (data.betting_bot_bet_on_games[i * 2] || data.neural_network_prob[i * 2] > threshold) {
            summary.ending_moneys_one_agree -= getReturn(data.games[i].home_ml,
                                                         !data.games[i].home_team_won) - BET_AMOUNT;
        }
        if (data.betting_bot_bet_on_games[i * 2 + 1] || data.neural_network_prob[i * 2 + 1] > threshold) {
            summary.ending_moneys_one_agree -= getReturn(data.games[i].away_ml,
                                                         !data.games[i].home_team_won) - BET_AMOUNT;
        }
        // Neural network agrees
        if (data.neural_network_prob[i * 2] > threshold) {
            summary.ending_money_neural -= getReturn(data.games[i].home_ml,
                                                         !data.games[i].home_team_won) - BET_AMOUNT;
        }
        if (data.neural_network_prob[i * 2 + 1] > threshold) {
            summary.ending_money_neural -= getReturn(data.games[i].away_ml,
                                                         !data.games[i].home_team_won) - BET_AMOUNT;
        }        
        // Reinforcement network agrees
        if (data.betting_bot_bet_on_games[i * 2]) {
            summary.ending_money_reinforce -= getReturn(data.games[i].home_ml,
                                                         !data.games[i].home_team_won) - BET_AMOUNT;
        }
        if (data.betting_bot_bet_on_games[i * 2 + 1]) {
            summary.ending_money_reinforce -= getReturn(data.games[i].away_ml,
                                                         !data.games[i].home_team_won) - BET_AMOUNT;
        }        
        
        
        summary.ending_money += game_profit_loss;
        let profit = summary.ending_money - starting_money;

        summary.ending_moneys_one_agrees.push(summary.ending_moneys_one_agree);
        summary.ending_moneys.push(summary.ending_money);
        summary.ending_money_neurals.push(summary.ending_money_neural);
        summary.ending_money_reinforces.push(summary.ending_money_reinforce);
        
        let bet_on_home = "";
        if (data.betting_bot_bet_on_games[i * 2] && data.neural_network_prob[i*2] > threshold) {
            bet_on_home = "&#9989;";
        }
        let bet_on_away = "";
        if (data.betting_bot_bet_on_games[i * 2 + 1] && data.neural_network_prob[i*2 + 1] > threshold) {
            bet_on_away = "&#9989;"
        }
        let which_team_won = "home";
        if (!data.games[i].home_team_won) {
            which_team_won = "away";
        }
        
        rows += "<td>" + i + "</td>" +
            "<td>" + data.teams[i * 2].nickname + "</td>" +
            "<td>" + data.teams[i * 2 + 1].nickname + "</td>" +
            "<td>" + home_ml + "</td>" +
            "<td>" + away_ml + "</td>" +
            "<td>" + bet_on_home + "</td>" +
            "<td>" + bet_on_away + "</td>" +
            "<td>" + data.neural_network_prob[i * 2].toFixed(2) + "</td>" +
            "<td>" + data.neural_network_prob[i * 2 + 1].toFixed(2) + "</td>" + 
            "<td>" + which_team_won + "</td>" +
            "<td style='color: " + getTextColor(game_profit_loss) + "'>"
            + Math.round(game_profit_loss) + "</td>" +
            "<td style='color: " + getTextColor(profit) + "'>"
            + Math.round(profit) + "</td>" +            
            "<td>" + Math.round(summary.ending_money) + "</td>";

        rows += "</tr>"
        $('#bettingResultTable').append(rows);
    }
           
    return summary;
}

function getReturn(ml, teamWon) {
    if (!teamWon) {
        return 0;
    }
    
    if (ml < 0) {
        return (100 / -ml) * 100 + BET_AMOUNT;
    }
    return (ml / 100) * 100 + BET_AMOUNT;
}
