document.addEventListener('DOMContentLoaded', function() {
    
    // breakpoints 
    const sm = window.matchMedia("(min-width: 576px)");
    const md = window.matchMedia("(min-width: 768px)");
    const lg = window.matchMedia("(min-width: 992px)");
    const xl = window.matchMedia("(min-width: 1200px)");
    const xxl = window.matchMedia("(min-width: 1400px)");

    // Select all account card elements
    const accountCards = document.querySelectorAll('.account-card');
    
    // Function to adjust the layout of account cards based on screen size
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


    // -- Spending Doughnut Chart -- //
    const dataElement = document.getElementById('spending-data');
    if (!dataElement) {
            
        console.error("Error: Spending data element (#spending-data) not found in the template.");
        // We will continue so other parts of the script can run
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
    }


    // =========================================================
    // START: BALANCE TREND LINE CHART
    // =========================================================
    const balanceLabelsElement = document.getElementById('balance-labels');
    const balanceDataElement = document.getElementById('balance-data');
    const trendCtx = document.getElementById('balanceTrendChart');
    
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
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
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
                        },
                        title: {
                            display: true,
                            text: 'Cumulative Financial Balance'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Balance (€)'
                            }
                        },
                        x: {
                            type: 'category', 
                            title: {
                                display: true,
                                text: 'Date'
                            }
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