// Get the canvas element
const ctx = document.getElementById('pieChart').getContext('2d');

// Get the counts from your template
const destinationCount = parseInt(document.querySelector('.card:nth-child(1) .fw-bold').textContent);
const activityCount = parseInt(document.querySelector('.card:nth-child(2) .fw-bold').textContent);
const accommodationCount = parseInt(document.querySelector('.card:nth-child(3) .fw-bold').textContent);
const restaurantCount = parseInt(document.querySelector('.card:nth-child(4) .fw-bold').textContent);

const total = destinationCount + activityCount + accommodationCount + restaurantCount;

Chart.register(ChartDataLabels);


new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Destinations', 'Activities', 'Accommodations', 'Restaurants'],
        datasets: [{
            data: [destinationCount, activityCount, accommodationCount, restaurantCount],
            backgroundColor: [
                '#4bc0c0', 
                '#36a2eb', 
                '#ff6384', 
                '#ffcd56' 
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true, 
                position: 'bottom'
            },
            datalabels: {
                color: '#fff',
                font: {
                    weight: 'bold',
                    size: 14
                },
                formatter: (value) => {
                    const percentage = ((value / total) * 100).toFixed(1);
                    return `${value}\n(${percentage}%)`;
                },
                textAlign: 'center'
            }
        }
    }
});

!function(d,s,id){
    var js,fjs=d.getElementsByTagName(s)[0];
    if(!d.getElementById(id)){
      js=d.createElement(s);
      js.id=id;
      js.src='https://weatherwidget.io/js/widget.min.js';
      fjs.parentNode.insertBefore(js,fjs);
    }
  }(document,'script','weatherwidget-io-js');