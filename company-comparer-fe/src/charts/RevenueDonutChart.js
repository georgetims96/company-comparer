import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';


export default function RevenueDonutChart(props) {
    ChartJS.register(ArcElement, Tooltip, Legend, Title);
    let colorStrings = ['rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'];
    let chartData = {
        labels: [],
        datasets: [{
            label: "Revenue",
            data: [],
            backgroundColor: [],
            borderColor: [],
            borderWidth:1,
        }]
    };

    const options = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Revenue Share'
            },
            legend: {
                // Switch to top maybe
                  position: 'bottom',
            },
        }
    }

    const financialData = props.data.data;
    const selectedYear = props.yearSelected || Math.max(props.data.data.years);
    let colorIndex = 0;
    for (let company of financialData.ciks) {
        chartData.labels.push(financialData["company_metadata"][company]["ticker"]);
        chartData.datasets[0].data.push(financialData[company]["absolute"]["revenue"][selectedYear])
        chartData.datasets[0].backgroundColor.push(colorStrings[colorIndex]);
        chartData.datasets[0].borderColor.push(colorStrings[colorIndex]);
        colorIndex += 1;
    }
   
   return (
        <div style={{width:"85%"}}>
            <Doughnut data={chartData} options={options} width={1} height={1} />
        </div>);
}