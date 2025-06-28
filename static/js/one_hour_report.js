document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('pieChart');
    if (!canvas) return;
    const labels = JSON.parse(canvas.dataset.labels);
    const values = JSON.parse(canvas.dataset.values);
    const data = {
        labels: labels,
        datasets: [{
            data: values,
            backgroundColor: [
                '#4F46E5', '#9333EA', '#059669',
                '#F59E0B', '#EF4444', '#3B82F6'
            ]
        }]
    };
    new Chart(canvas, {
        type: 'pie',
        data: data,
        options: { responsive: true }
    });
});
