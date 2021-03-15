
var config = {
    type: 'line',
    data: {
		labels:grafico.labels,
        datasets: [{
			data:grafico.data ,
			backgroundColor: [
				'rgba(242,38,19,0.2)' ,
			],
			borderColor: [
				 'rgba(242,38,19,0.5)',
			],
        }],
    },
    options: {
        responsive: true,
        legend:{
            display:false
        },
        title:{
            display:false
        },
        label:{
            display:false
        },
		tooltips: {
			displayColors:false,
			titleFontSize:18,
			titleAlign: 'center',
			titleFontColor: 'rgba(242,38,19,.8)',
			backgroundColor:'rgba(255,255,255,0.8)' ,
			borderColor: 'rgba(242,38,19,.8)',
			caretSize: 14,
			cornerRadius:8,
			caretPadding:7,
			borderWidth:2,
			intersect:false,
			callbacks: {
				label: function(tooltipItem, data) {
					return
				},
				title: function(tooltipItem, data) {
					return '\n'+tooltipItem[0].value+' pruebas'+ '\n\n'+grafico.labels[tooltipItem[0].index]
				}
			}
		},
		scales: {
            xAxes: [{
                ticks: {
                    display: false ,
					maxTicksLimit: 10,
                },
				gridLines:{display:false}
            }],
            yAxes: [{
                ticks: {
                    display: false ,
					beginAtZero: true,
					maxTicksLimit: 10,
                },
				gridLines:{display:false}
            }]
        }
    }
};
var chart
$(document).ready(function(){
      var ctx = $('#grafico')[0].getContext('2d');
      chart = new Chart(ctx, config);
})
