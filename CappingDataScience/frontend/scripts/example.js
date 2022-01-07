//console.log("Hello from javascript");

const APIURL = "http://nicholasblaskey.com:8080/api";

// Get list of tables and put into our select.
$.get(APIURL + "/meta/tables", function(data) {
    let tableNamesString = "";
    for (let i = 0; i < data.length; i++) {        
        tableNamesString += data[i] + ", ";        
        //getNullInfo(data[2], i);

        $('#tableSelect').append(
            "<option value='" + data[i] + "'>" + data[i] + "</option>");
    }

    $('#tableList').html(tableNamesString);
});


$('#tableSelect').change(function () {
    let tableName = $('#tableSelect').val();
    $.get(APIURL + "/meta/nulls/" + tableName, function(data) {
        makeNullChart(tableName, data, "chartContainer0");
    });
});

function makeNullChart(tableName, nullInfo, divID) {
    // Make chart js canvas in the space for divID.
    document.getElementById(divID).innerHTML = '<canvas class="my-4"' +
        'id="myChart" width="900" height="380"></canvas>';
    var ctx = document.getElementById("myChart");    

    
    // Setup data
    const labels = nullInfo.columns;
    labels.unshift("row count", "row with nulls");
    const null_columns = nullInfo.nulls_in_columns;
    null_columns.unshift(nullInfo.row_count, nullInfo.rows_with_any_nulls);
    const data = {
        labels: labels,
        datasets: [{
            label: 'TODO CHANGE TITLE ' + tableName,
            data: null_columns,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 5
        }]
    };
    
    // Setup chart configuration
    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                
                y: {
                    beginAtZero: true
                }
            }
        },
    };

    const chart = new Chart(ctx, config)

    
}

/*
$.get(APIURL + "/team", function(data) {
    // What happens after the API request responds.
    //console.log(data);
    for (let i = 0; i < data.length; i++) {
        console.log(i);
        console.log(data[i]);

        let rows = "<tr>";

        rows += "<td>" + data[i].abbreviation + "</td>" +
        "<td>" + data[i].nickname + "</td>" +
        "<td>" + data[i].city + "</td>"+
        "<td>" + data[i].head_coach + "</td>"+
        "<td>" + data[i].manager + "</td>"+
        "<td>" + data[i].max_year_in_nba_champ + "</td>"+
        "<td>" + data[i].min_year_in_nba_champ + "</td>"+
        "<td>" + data[i].nickname + "</td>"+
        "<td>" + data[i].owner + "</td>"+
        "<td>" + data[i].players_been_on_team + "</td>"+
        "<td>" + data[i].team_id + "</td>"+
        "<td>" + data[i].year_founded + "</td>";
            
        rows += "</tr>";
        console.log(rows);
        $('#teamTable').append(rows);
    }
});
*/
