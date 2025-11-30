document.addEventListener('DOMContentLoaded', function() {
    
    // breakpoints 
    const sm = window.matchMedia("(min-width: 576px)");
    const md = window.matchMedia("(min-width: 768px)");
    const lg = window.matchMedia("(min-width: 992px)");
    const xl = window.matchMedia("(min-width: 1200px)");
    const xxl = window.matchMedia("(min-width: 1400px)");

    // Select all account card elements
    const accountCards = document.querySelectorAll('.account-card');
    
    // Adjust the layout of account cards based on screen size
    function adjustAccountCardLayout() {
        accountCards.forEach(card => {
            if (lg.matches) {
                card.children[0].style.display = 'block';
            } else {
                card.children[0].style.display = 'none';
            }
        });
    }
    adjustAccountCardLayout(); 
    // Adjust layout on window resize
    window.addEventListener('resize', adjustAccountCardLayout);

    
    // =========================================================
    // START: MONTH/YEAR DROPDOWN AUTO-SUBMIT LOGIC
    // =========================================================
    const monthSelect = document.getElementById('month-select');
    const yearSelect = document.getElementById('year-select');
    const filterForm = document.getElementById('filter-form');
    
    if (monthSelect && yearSelect && filterForm) {
        monthSelect.addEventListener('change', function() {
            filterForm.submit();
        });
        yearSelect.addEventListener('change', function() {
            filterForm.submit();
        });
    }
    // =========================================================
    // END: MONTH/YEAR DROPDOWN AUTO-SUBMIT LOGIC
    // =========================================================


    // =========================================================
    // START: EXPENSE STRUCTURE DOUGHNUT CHART
    // =========================================================
    const dataElement = document.getElementById('spending-data');
    if (!dataElement) {
            
        console.error("Error: Spending data element (#spending-data) not found in the template.");

    } else {
        let spendingData = [];
        try {
            spendingData = JSON.parse(dataElement.textContent);
        } catch (e) {
            console.error("Failed to parse spending data JSON:", e);
        }

        const ctx = document.getElementById('spendingChart');

        if (ctx && spendingData.length > 0) {
            
            const labels = spendingData.map(item => item.category__name);
            const amounts = spendingData.map(item => item.total_spent);
            
            const backgroundColors = [
                '#eb9c64', '#ff8789', '#554e4f', '#8fbf9f', '#346145', 
                '#353535', '#000000', '#f5ecd7', '#ebe2cd', '#c2baa6'
            ];

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        label: ' Total Spent',
                        data: amounts,
                        backgroundColor: backgroundColors.slice(0, labels.length),
                        borderColor: '#ebe2cd',
                        borderWidth: 2,
                        hoverOffset: 3
                    }]
                },
                options: {
                    cutout: '60%',
                    animation: {
                        animateRotate: true
                    },
                    plugins: {
                        legend: {
                            display: false,
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
    }
    // =========================================================
    // END: EXPENSE STRUCTURE DOUGHNUT CHART
    // =========================================================


    // =========================================================
    // START: BALANCE TREND LINE CHART
    // =========================================================
    const balanceLabelsElement = document.getElementById('balance-labels');
    const balanceDataElement = document.getElementById('balance-data');
    const trendCtx = document.getElementById('balanceTrendChart');

    // Helper function to abbreviate large numbers
    function abbreviateNumber(value) {
        let newValue = value;
        const sign = value < 0 ? -1 : 1;
        value = Math.abs(value);

        const suffixes = ["", "K", "M", "B","T"];
        const suffixNum = Math.floor( ("" + value).length / 3 );

        if (suffixNum > 0) {
            let base = Math.pow(1000, suffixNum);
            newValue = newValue / base;

            if (Math.abs(newValue) % 1 !== 0) {
                newValue = newValue.toFixed(1);
            } else {
                newValue = Math.round(newValue);
            }
        } else {
            return newValue.toFixed(2);
        }

        return (newValue * sign) + suffixes[suffixNum];
    }
    
    if (balanceLabelsElement && balanceDataElement && trendCtx) {
        // Parse data from the json_script tags
        const labels = JSON.parse(balanceLabelsElement.textContent);
        const data = JSON.parse(balanceDataElement.textContent);

        if (data.length > 0) {
            const chartData = {
                labels: labels,
                datasets: [{
                    label: 'Total Balance',
                    data: data,
                    fill: true,
                    borderColor: '#eb9c64',
                    backgroundColor: 'rgba(235, 156, 100, 0.2)',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: '#f5ecd7',
                    pointBackgroundColor: '#8fbf9f',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#346145',
                    pointHoverBorderColor: '#f5ecd7',
                    pointHoverBorderWidth: 2,
                    pointHitRadius: 30,
                    pointStyle: 'circle',
                    tension: 0.1
                }]
            };

            const config = {
                type: 'line',
                data: chartData,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: false,
                            },
                            ticks: {
                                callback: function(value) {
                                    return '€' + abbreviateNumber(value);
                                }
                            }
                        },
                        x: {
                            type: 'category'
                        }
                    }
                }
            };

            new Chart(
                trendCtx,
                config
            );
        } else {
            // Display message if no data exists for the period
            trendCtx.parentElement.innerHTML = '<div class="text-center p-5 text-muted">No transaction data available for this period to show the balance trend.</div>';
        }
    }
    // =========================================================
    // END: BALANCE TREND LINE CHART
    // =========================================================

});