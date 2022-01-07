const APIURL = "http://nicholasblaskey.com:8080/api";

// Get list of tables and put into our select.
$.get(APIURL + "/meta/tables", function(data) {
    for (let i = 0; i < data.length; i++) {        
        $('#tableSelect').append(
            "<option value='" + data[i] + "'>" + data[i] + "</option>");
    }

    // Just make our chart originally that first value.
    makeChartFromTable(data[0]);
});


$('#tableSelect').change(function () {
    let tableName = $('#tableSelect').val();
    makeChartFromTable(tableName);    
});

function makeChartFromTable(tableName) {
    $.get(APIURL + "/meta/nulls/" + tableName, function(data) {
        makeNullChart(tableName, data, "chartContainer0");
    });
}

function makeNullChart(tableName, nullInfo, divID) {
    // Make chart js canvas in the space for divID.
    document.getElementById(divID).innerHTML = '<canvas class="my-4"' +
        'id="myChart" width="900" height="380"></canvas>';
    var ctx = document.getElementById("myChart");    


    // Setup data
    const labels = nullInfo.columns;
    labels.unshift("row count", "rows_with_any_nulls");
    const null_columns = nullInfo.nulls_in_columns;
    null_columns.unshift(nullInfo.row_count, nullInfo.rows_with_any_nulls);
    const data = {
        labels: labels,
        datasets: [{
            label: tableName + " table",
            data: null_columns,
            backgroundColor: ["blue", "purple", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red","red","red","red", "red","red","red","red","red","red"],
            borderColor: ["blue", "purple", "red", "red", "red", "red","red","red","red","red","red","red","red","red","red","red", "red", "red", "red", "red","red","red","red","red","red","red"],
            borderWidth: 5
        }]
    };
    console.log(labels);
    // Setup chart configuration
    const myChart = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: {
        scaleShowValues: true,
        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero: true,
                    autoSkip: false,
                    maxRotation: 90,
                    minRotation: 90
                }
            }]
        }
    }
});}
