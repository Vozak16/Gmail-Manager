var endpoint = '/api/chart/data/'
var data = []
var data_unread = []

var defaultData = []
var labels = []
var chartColors = []

var defaultData_unread = []
var labels_unread = []
var chartColors_unread = [];

$.ajax({
    method: "GET",
    url: endpoint,
    success: function(all_data){
        data = all_data.data
        data_unread = all_data.data_unread

        labels = data.labels
        defaultData = data.default
        chartColors = data.colors

        labels_unread = data_unread.labels
        defaultData_unread = data_unread.default
        chartColors_unread = data_unread.colors
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

    let myChart2 = document.getElementById("myChartUnread").getContext('2d');
    let chart2 = new Chart(myChart2, {
	type: 'doughnut',
	data: {
		labels: labels_unread,
		datasets: [ {
			data: defaultData_unread,
			backgroundColor: chartColors_unread
		}]
	},
	options: {
		title: {
			text: "Read/Unread Statistics",
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