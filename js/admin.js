const ctx = document.getElementById('pieChart').getContext('2d');
const myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['Accommodation', 'Activities', 'Food & Drinks', 'Destination', 'Articles'],
    datasets: [{
      label: 'Inquiries',
      data: [10, 15, 20, 25, 30],
      backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56', '#4bc0c0', '#9966ff']
    }]
  },
  options: {
    responsive: false, // Disable automatic resizing
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          label: function (context) {
            const data = context.dataset.data;
            const total = data.reduce((a, b) => a + b, 0);
            const percentage = ((context.raw / total) * 100).toFixed(2);
            return `${context.label}: ${percentage}% (${context.raw})`;
          }
        }
      },
      datalabels: {
        formatter: (value, ctx) => {
          const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
          const percentage = ((value / total) * 100).toFixed(1);
          return `${percentage}%`;
        },
        color: '#fff',
        font: {
          weight: 'bold'
        }
      }
    }
  },
  plugins: [ChartDataLabels] // Ensure the ChartDataLabels plugin is included
});
