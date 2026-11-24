/**
 * HousePrice AI - Main Frontend Interactive Logic
 * Handles Chart.js initializations, AJAX predictions, form validations, and UI interactions.
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Mobile Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggle');
    const appSidebar = document.getElementById('appSidebar');
    if (sidebarToggleBtn && appSidebar) {
        sidebarToggleBtn.addEventListener('click', function () {
            appSidebar.classList.toggle('show');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function (e) {
            if (window.innerWidth <= 992 &&
                !appSidebar.contains(e.target) &&
                !sidebarToggleBtn.contains(e.target) &&
                appSidebar.classList.contains('show')) {
                appSidebar.classList.remove('show');
            }
        });
    }

    // 2. INR Formatting Helper
    window.formatINR = function (num) {
        if (!num || isNaN(num)) return '₹ 0';
        const val = Math.round(Number(num));
        if (val >= 10000000) {
            return `₹ ${(val / 10000000).toFixed(2)} Cr`;
        } else if (val >= 100000) {
            return `₹ ${(val / 100000).toFixed(2)} L`;
        } else {
            return `₹ ${val.toLocaleString('en-IN')}`;
        }
    };

    window.formatINRFull = function (num) {
        if (!num || isNaN(num)) return '₹ 0';
        return '₹ ' + Math.round(Number(num)).toLocaleString('en-IN');
    };

    // 3. Initialize Charts if elements exist on current page
    initDashboardCharts();
    initAnalyticsCharts();
    initPerformanceCharts();

    // 4. Prediction Form AJAX Handler
    initPredictionForm();
});

/* ==========================================================
   PREDICTION FORM HANDLER (AJAX + Validation)
========================================================== */
function initPredictionForm() {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('predictSubmitBtn');
    const resultContainer = document.getElementById('predictionResultContainer');

    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Client side validation
        const location = document.getElementById('predLocation').value;
        const areaSqft = parseFloat(document.getElementById('predArea').value);
        const bedrooms = parseInt(document.getElementById('predBedrooms').value);
        const bathrooms = parseInt(document.getElementById('predBathrooms').value);
        const floors = parseInt(document.getElementById('predFloors').value);
        const propertyAge = parseInt(document.getElementById('predAge').value);
        const parking = parseInt(document.getElementById('predParking').value);

        if (!location) {
            alert('Please select a valid property location.');
            return;
        }
        if (isNaN(areaSqft) || areaSqft < 200 || areaSqft > 15000) {
            alert('Please enter a valid property area between 200 and 15,000 sq ft.');
            return;
        }

        // Disable button & show spinner
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Calculating Regression...';

        const payload = {
            location: location,
            area_sqft: areaSqft,
            bedrooms: bedrooms,
            bathrooms: bathrooms,
            floors: floors,
            property_age: propertyAge,
            parking: parking
        };

        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-magic me-2"></i>Predict Price Now';

            if (!data.success) {
                alert('Prediction Error: ' + (data.error || 'Unknown error'));
                return;
            }

            const pred = data.prediction;
            displayPredictionResult(pred, data.disclaimer);
        })
        .catch(err => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-magic me-2"></i>Predict Price Now';
            console.error('Prediction request failed:', err);
            alert('Server error while predicting. Please try again.');
        });
    });
}

function displayPredictionResult(pred, disclaimer) {
    const container = document.getElementById('predictionResultContainer');
    if (!container) return;

    container.innerHTML = `
        <div class="prediction-result-card animate__animated animate__fadeInUp">
            <div class="d-flex align-items-center justify-content-between mb-2">
                <span class="badge bg-success text-white px-3 py-2 rounded-pill">
                    <i class="bi bi-check-circle-fill me-1"></i> Multiple Linear Regression Output
                </span>
                <span class="text-white-50 small"><i class="bi bi-clock me-1"></i>Just Now</span>
            </div>
            
            <p class="text-white-50 mb-1 small text-uppercase fw-bold letter-spacing-1">Estimated Market Value</p>
            <div class="prediction-price-tag">
                <span>${pred.formatted_price}</span>
                <span class="prediction-price-secondary">(${pred.formatted_price_full})</span>
            </div>
            
            <p class="text-white-50 mb-3">Estimated Rate: <strong class="text-white">₹ ${pred.price_per_sqft.toLocaleString('en-IN')}/sq.ft</strong></p>
            
            <div class="border-top border-secondary pt-3 mt-3">
                <p class="text-white-50 small fw-bold mb-2 text-uppercase">Configured Property Specs:</p>
                <div class="property-details-pill-grid">
                    <span class="detail-pill"><i class="bi bi-geo-alt-fill"></i> ${pred.location}</span>
                    <span class="detail-pill"><i class="bi bi-aspect-ratio-fill"></i> ${pred.area_sqft} sq.ft</span>
                    <span class="detail-pill"><i class="bi bi-door-closed-fill"></i> ${pred.bedrooms} BHK</span>
                    <span class="detail-pill"><i class="bi bi-droplet-half"></i> ${pred.bathrooms} Baths</span>
                    <span class="detail-pill"><i class="bi bi-building"></i> ${pred.floors} Floor(s)</span>
                    <span class="detail-pill"><i class="bi bi-calendar2-check"></i> ${pred.property_age} yrs old</span>
                    <span class="detail-pill"><i class="bi bi-p-square-fill"></i> Parking: ${pred.parking}</span>
                </div>
            </div>

            <div class="disclaimer-alert">
                <i class="bi bi-exclamation-triangle-fill fs-5 mt-1 text-warning flex-shrink-0"></i>
                <div>
                    <strong>Academic & Demonstration Disclaimer:</strong>
                    <div>${disclaimer}</div>
                </div>
            </div>
        </div>
    `;

    // Smooth scroll to result
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ==========================================================
   DASHBOARD CHARTS
========================================================== */
function initDashboardCharts() {
    const locChartEl = document.getElementById('dashLocationChart');
    const areaChartEl = document.getElementById('dashAreaPriceChart');
    if (!locChartEl && !areaChartEl) return;

    fetch('/api/analytics/charts')
        .then(res => res.json())
        .then(data => {
            // 1. Location Bar Chart
            if (locChartEl) {
                const locations = data.price_by_location.map(d => d.location);
                const avgPrices = data.price_by_location.map(d => (d.avg_price / 100000).toFixed(2)); // in Lakhs

                new Chart(locChartEl, {
                    type: 'bar',
                    data: {
                        labels: locations,
                        datasets: [{
                            label: 'Avg Price (₹ Lakhs)',
                            data: avgPrices,
                            backgroundColor: 'rgba(16, 185, 129, 0.85)',
                            borderColor: '#10b981',
                            borderRadius: 6,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        return `Avg Price: ₹ ${ctx.raw} Lakhs`;
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: { display: true, text: 'Price (₹ in Lakhs)' },
                                grid: { color: 'rgba(226, 232, 240, 0.8)' }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { maxRotation: 45, minRotation: 30 }
                            }
                        }
                    }
                });
            }

            // 2. Area vs Price Scatter Chart
            if (areaChartEl) {
                const scatterPoints = data.area_vs_price.map(p => ({
                    x: p.area_sqft,
                    y: parseFloat((p.price_inr / 100000).toFixed(2)),
                    location: p.location
                }));

                new Chart(areaChartEl, {
                    type: 'scatter',
                    data: {
                        datasets: [{
                            label: 'Properties (Area vs Price)',
                            data: scatterPoints,
                            backgroundColor: 'rgba(37, 99, 235, 0.65)',
                            borderColor: '#2563eb',
                            pointRadius: 4,
                            pointHoverRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        const p = ctx.raw;
                                        return `${p.location}: ${p.x} sqft → ₹ ${p.y} Lakhs`;
                                    }
                                }
                            }
                        },
                        scales: {
                            x: {
                                title: { display: true, text: 'Area (Square Feet)' },
                                grid: { color: 'rgba(226, 232, 240, 0.8)' }
                            },
                            y: {
                                title: { display: true, text: 'Price (₹ in Lakhs)' },
                                grid: { color: 'rgba(226, 232, 240, 0.8)' }
                            }
                        }
                    }
                });
            }
        })
        .catch(err => console.error('Error fetching dashboard charts:', err));
}

/* ==========================================================
   MARKET ANALYTICS CHARTS (All 4 Required Charts)
========================================================== */
function initAnalyticsCharts() {
    const locBarEl = document.getElementById('analyticsLocationBarChart');
    const areaScatterEl = document.getElementById('analyticsAreaScatterChart');
    const dateTrendEl = document.getElementById('analyticsDateTrendChart');
    const bedroomBarEl = document.getElementById('analyticsBedroomsBarChart');

    if (!locBarEl && !areaScatterEl && !dateTrendEl && !bedroomBarEl) return;

    fetch('/api/analytics/charts')
        .then(res => res.json())
        .then(data => {
            // Chart 1: Bar chart comparing average prices by location
            if (locBarEl) {
                const locations = data.price_by_location.map(d => d.location);
                const avgPrices = data.price_by_location.map(d => (d.avg_price / 100000).toFixed(2));

                new Chart(locBarEl, {
                    type: 'bar',
                    data: {
                        labels: locations,
                        datasets: [{
                            label: 'Average Price (₹ Lakhs)',
                            data: avgPrices,
                            backgroundColor: '#10b981',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: { display: true, text: 'Avg Price (₹ Lakhs)' }
                            },
                            x: { ticks: { maxRotation: 45, minRotation: 30 } }
                        }
                    }
                });
            }

            // Chart 2: Scatter plot showing area versus house price
            if (areaScatterEl) {
                const scatterPoints = data.area_vs_price.map(p => ({
                    x: p.area_sqft,
                    y: parseFloat((p.price_inr / 100000).toFixed(2)),
                    location: p.location,
                    bedrooms: p.bedrooms
                }));

                new Chart(areaScatterEl, {
                    type: 'scatter',
                    data: {
                        datasets: [{
                            label: 'Property Listings',
                            data: scatterPoints,
                            backgroundColor: 'rgba(99, 102, 241, 0.7)',
                            borderColor: '#6366f1',
                            pointRadius: 4.5
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        const p = ctx.raw;
                                        return `${p.location} (${p.bedrooms} BHK): ${p.x} sqft, ₹ ${p.y}L`;
                                    }
                                }
                            }
                        },
                        scales: {
                            x: { title: { display: true, text: 'Super Built-up Area (Sq. Ft)' } },
                            y: { title: { display: true, text: 'House Price (₹ in Lakhs)' } }
                        }
                    }
                });
            }

            // Chart 3: Line chart showing property price trends by dataset date
            if (dateTrendEl && data.price_trends_by_date) {
                const months = data.price_trends_by_date.map(d => d.month);
                const avgMonthlyPrice = data.price_trends_by_date.map(d => (d.avg_price / 100000).toFixed(2));

                new Chart(dateTrendEl, {
                    type: 'line',
                    data: {
                        labels: months,
                        datasets: [{
                            label: 'Average Listed Price (₹ Lakhs)',
                            data: avgMonthlyPrice,
                            borderColor: '#059669',
                            backgroundColor: 'rgba(16, 185, 129, 0.12)',
                            tension: 0.35,
                            fill: true,
                            pointRadius: 5,
                            pointBackgroundColor: '#059669'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                title: { display: true, text: 'Average Price (₹ in Lakhs)' }
                            },
                            x: { title: { display: true, text: 'Listing Period (Month)' } }
                        }
                    }
                });
            }

            // Chart 4: Bar chart comparing prices by number of bedrooms
            if (bedroomBarEl && data.prices_by_bedrooms) {
                const bedLabels = data.prices_by_bedrooms.map(d => `${d.bedrooms} BHK`);
                const avgBedPrice = data.prices_by_bedrooms.map(d => (d.avg_price / 100000).toFixed(2));

                new Chart(bedroomBarEl, {
                    type: 'bar',
                    data: {
                        labels: bedLabels,
                        datasets: [{
                            label: 'Average Price by Bedroom Config (₹ Lakhs)',
                            data: avgBedPrice,
                            backgroundColor: [
                                'rgba(59, 130, 246, 0.8)',
                                'rgba(16, 185, 129, 0.8)',
                                'rgba(245, 158, 11, 0.8)',
                                'rgba(139, 92, 246, 0.8)',
                                'rgba(236, 72, 153, 0.8)'
                            ],
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: { display: true, text: 'Price (₹ in Lakhs)' }
                            }
                        }
                    }
                });
            }
        })
        .catch(err => console.error('Error loading analytics charts:', err));
}

/* ==========================================================
   MODEL PERFORMANCE CHARTS (Actual vs Predicted & Residuals)
========================================================== */
function initPerformanceCharts() {
    const actVsPredEl = document.getElementById('actualVsPredChart');
    const residualEl = document.getElementById('residualDistChart');

    if (!actVsPredEl && !residualEl) return;

    fetch('/api/performance/charts')
        .then(res => res.json())
        .then(data => {
            // Chart 5: Actual vs Predicted Price Chart
            if (actVsPredEl && data.actual_vs_predicted) {
                const points = data.actual_vs_predicted.map(d => ({
                    x: parseFloat((d.actual / 100000).toFixed(2)),
                    y: parseFloat((d.predicted / 100000).toFixed(2)),
                    loc: d.location,
                    area: d.area_sqft
                }));

                // Calculate reference 45-degree line bounds
                const allVals = points.flatMap(p => [p.x, p.y]);
                const minVal = Math.min(...allVals);
                const maxVal = Math.max(...allVals);

                new Chart(actVsPredEl, {
                    type: 'scatter',
                    data: {
                        datasets: [
                            {
                                label: 'Test Samples (Actual vs Predicted)',
                                data: points,
                                backgroundColor: 'rgba(16, 185, 129, 0.75)',
                                borderColor: '#059669',
                                pointRadius: 5
                            },
                            {
                                type: 'line',
                                label: 'Ideal Fit (y = x)',
                                data: [{ x: minVal, y: minVal }, { x: maxVal, y: maxVal }],
                                borderColor: '#ef4444',
                                borderDash: [6, 6],
                                borderWidth: 2,
                                fill: false,
                                pointRadius: 0
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        if (ctx.datasetIndex === 1) return 'Ideal Line (y = x)';
                                        const p = ctx.raw;
                                        return `${p.loc} (${p.area} sqft): Actual ₹${p.x}L vs Pred ₹${p.y}L`;
                                    }
                                }
                            }
                        },
                        scales: {
                            x: { title: { display: true, text: 'Actual Price on Test Data (₹ in Lakhs)' } },
                            y: { title: { display: true, text: 'Predicted Price by Linear Regression (₹ in Lakhs)' } }
                        }
                    }
                });
            }

            // Chart 6: Residual Distribution Visualization
            if (residualEl && data.residual_distribution) {
                const labels = data.residual_distribution.map(d => d.bin_label);
                const counts = data.residual_distribution.map(d => d.count);

                new Chart(residualEl, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Frequency of Residuals',
                            data: counts,
                            backgroundColor: 'rgba(59, 130, 246, 0.8)',
                            borderColor: '#2563eb',
                            borderRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: { display: true, text: 'Frequency (Test Set Samples)' }
                            },
                            x: {
                                title: { display: true, text: 'Residual Range (Actual - Predicted in ₹ Lakhs)' },
                                ticks: { maxRotation: 45, minRotation: 30 }
                            }
                        }
                    }
                });
            }
        })
        .catch(err => console.error('Error loading performance charts:', err));
}
