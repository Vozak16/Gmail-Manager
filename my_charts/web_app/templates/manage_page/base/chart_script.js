var endpoint = '/api/manage/chart/data/'

var defaultData = []
var labels = []
var chartColors = []

$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        labels = data.labels
        defaultData = data.default
        chartColors = data.colors
        setChart()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setChart(){
    let myChart1 = document.getElementById("myChart").getContext('2d');
    let chart1 = new Chart(myChart1, {
	type: 'doughnut',
	data: {
		labels: labels,
		datasets: [ {
			data: defaultData,
			backgroundColor: chartColors
		}]
	},
	options: {
		title: {
			text: "Inbox Statistics",
			display: false
		},
		legend: {
            display: false,
        },
        responsive: true,
        maintainAspectRatio: false
	}
});
}