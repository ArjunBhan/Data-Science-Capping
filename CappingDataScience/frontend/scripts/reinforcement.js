const APIURL = "http://nicholasblaskey.com:8080/api";
const BET_AMOUNT = 100;

function makeChart(starting_money, ending_moneys) {
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
                label: 'Money our betting bot has',
                data: ending_moneys,
                borderWidth: 3,
                fill: false,
                borderColor: 'red'
            },
                       {
                           label: "Money if we didn't bet anything",
                           data: starting_moneys,
                           borderWidth: 3,
                           fill: false,
                           borderColor: 'green'
                       }
                      ]
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
    let starting_money = parseInt($("#startingMoneyInput").val());
    $.post(
        {
            url: APIURL + "/model/reinforcement",
            data: JSON.stringify({
                "starting_money": starting_money,
                "starting_date": $("#startingDateInput").val(),
                "num_games": parseInt($("#numGamesInput").val())
            }),
            contentType : 'application/json',
        },
        
        function(data) {
            summary = buildBettingTable(data, starting_money);

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

            makeChart(starting_money, summary.ending_moneys)

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

function buildBettingTable(data, starting_money) {
    let summary = {
        ending_money: starting_money,
        underdog_bets: 0,
        underdog_profit: 0,
        favorite_bets: 0,
        favorite_profit: 0,
        ending_moneys: [starting_money]
    }

    
    console.log(data.bet_on_games)
    
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
        if (data.bet_on_games[i*2]) {
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
        if (data.bet_on_games[i*2 + 1]) {
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
        summary.ending_money += game_profit_loss;
        let profit = summary.ending_money - starting_money;

        summary.ending_moneys.push(summary.ending_money);
        
        let bet_on_home = "";
        if (data.bet_on_games[i * 2]) {
            bet_on_home = "&#9989;";
        }
        let bet_on_away = "";
        if (data.bet_on_games[i * 2 + 1]) {
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
