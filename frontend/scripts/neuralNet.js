const APIURL = "http://nicholasblaskey.com:8080/api";

// Have the report be hidden by default.
$("#neuralReport").hide();
$("#hideButton").click(function() {
    $("#neuralReport").hide();
});

$("#submitBettingConfig").click(function() {
    $.post(
        {
            url: APIURL + "/model/neuralNetwork",
            data: JSON.stringify({
                "tweet": $("#tweetInput").val(),
                "date": $("#startingDateInput").val()
            }),
            contentType : 'application/json',
        },
        
        function(data) {
            $("#neuralReport").show();
            
            // Get the team names.
            let team_ids = [data.game.home_team_id, data.game.away_team_id];
            for (let i = 0; i < team_ids.length; i++) {
                $.get(APIURL + "/team/" + team_ids[i], function(team) {
                    if (i == 0) {
                        $("#homeTeamName").html("Home team: " + team.nickname);
                    } else {
                        $("#awayTeamName").html("Away team: " + team.nickname);
                    }
                });
            }
            
            $("#HomeWin").html(": " + (data.chance_to_win.toFixed(2) * 100) + "%");
            $("#HomeFirstRoundScore").html(": " + data.game.home_first + " ");
            $("#HomeSecondRoundScore").html(": " + data.game.home_second + " ");
            $("#HomeThirdRoundScore").html(": " + data.game.home_third + " ");
            $("#HomeFourthRoundScore").html(": " + data.game.home_fourth + " ");
            
            $("#AwayFirstRoundScore").html(": " + data.game.away_first + " ");
            $("#AwaySecondRoundScore").html(": " + data.game.away_second + " ");
            $("#AwayThirdRoundScore").html(": " + data.game.away_third + " ");
            $("#AwayFourthRoundScore").html(": " + data.game.away_fourth + " ");
            $("#AwayScore").html(": " + (data.game.away_first+data.game.away_second+data.game.away_third+data.game.away_fourth)) + " ";
            $("#HomeScore").html(": " +(data.game.home_first+data.game.home_second+data.game.home_third+data.game.home_fourth)) + " ";
            $("#AwayWin").html(": " + ((1-data.chance_to_win).toFixed(2) * 100) + "%");
        }        
    );
});

