fetch("http://127.0.0.1:5000/predictions")
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById("prediction-table-body");
        const labels = [];
        const scores = [];
        const colors = [];

        let danger = 0;
        let warning = 0;
        let safe = 0;

        data.forEach(item => {
            labels.push(item.place);
            scores.push(item.risk_score);

            let badgeClass = "";
            let barColor = "";

            if (item.risk_level === "Danger") {
                danger++;
                badgeClass = "danger";
                barColor = "rgba(220, 53, 69, 0.8)";
            } else if (item.risk_level === "Warning") {
                warning++;
                badgeClass = "warning";
                barColor = "rgba(255, 193, 7, 0.8)";
            } else {
                safe++;
                badgeClass = "safe";
                barColor = "rgba(40, 167, 69, 0.8)";
            }

            colors.push(barColor);

            const row = `
                <tr>
                    <td>${item.place}</td>
                    <td>${item.severity}</td>
                    <td>${item.type}</td>
                    <td>${item.risk_score}</td>
                    <td><span class="badge ${badgeClass}">${item.risk_level}</span></td>
                    <td>${item.reason}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });

        document.getElementById("total-locations").innerText = `Total Locations: ${data.length}`;
        document.getElementById("danger-count").innerText = `Danger: ${danger}`;
        document.getElementById("warning-count").innerText = `Warning: ${warning}`;
        document.getElementById("safe-count").innerText = `Safe: ${safe}`;

        const ctx = document.getElementById("riskChart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Flood Risk Score",
                    data: scores,
                    backgroundColor: colors,
                    borderColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => console.error("Error fetching predictions:", error));