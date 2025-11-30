document.addEventListener('DOMContentLoaded', function() {
    
    const dataElement = document.getElementById('spending-data');
    if (!dataElement) {
            
        console.error("Error: Spending data element (#spending-data) not found in the template.");
        return;
    }
    
    let spendingData = [];
    try {
        spendingData = JSON.parse(dataElement.textContent);
    } catch (e) {
        console.error("Failed to parse spending data JSON:", e);
        return;
    }

    const ctx = document.getElementById('spendingChart');

    if (ctx && spendingData.length > 0) {
        
        const labels = spendingData.map(item => item.category__name);
        const amounts = spendingData.map(item => item.total_spent);
        
        
        const backgroundColors = [
            '#eb9c64', 
            '#ff8789', 
            '#554e4f', 
            '#8fbf9f', 
            '#346145', 
            '#353535', 
            '#000000', 
            '#f5ecd7', 
            '#ebe2cd', 
            '#c2baa6'
            
        ];


        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Amount Spent',
                    data: amounts,
                    backgroundColor: backgroundColors.slice(0, labels.length),
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false,
                    }
                }
            }
        });
    } else if (ctx) {
        
        ctx.parentElement.innerHTML = '<div class="text-center p-5 text-muted">No expense transactions recorded this month to display a chart.</div>';
    }
});