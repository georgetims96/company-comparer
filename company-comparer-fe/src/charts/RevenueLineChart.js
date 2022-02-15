import React from 'react';
import { Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,} from 'chart.js';
import { Line } from 'react-chartjs-2';


export default function RevenueLineChart(props) {
    ChartJS.register(CategoryScale,
        LinearScale,
        PointElement,
        LineElement,
        Title,
        Tooltip,
        Legend);
    let colorStrings = ['rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'];
    let chartData = {
        labels: [],
        datasets: []
    };

    const options = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Revenue Growth'
            },
            legend: {
                // Switch to top maybe
                  position: 'bottom',
            },
        }
    }

    const financialData = props.data.data;
    const selectedYears = props.data.data.years;
    // Sort selected years
    selectedYears.sort();
    // Remove first element
    chartData.labels = selectedYears;
    const minYear = selectedYears[0];
    let companyIndex = 0;
    for (let company of financialData.ciks) {
        let companyRevenueGrowth = [];
        for (let year of selectedYears) {
            companyRevenueGrowth.push((financialData[company]["absolute"]["revenue"][year+1]/financialData[company]["absolute"]["revenue"][year])-1);
        }
        chartData.datasets.push({
            label: financialData["company_metadata"][company]["ticker"],
            data: companyRevenueGrowth,
            borderColor: colorStrings[companyIndex],
            backgroundColor: colorStrings[companyIndex],
            spanGaps: true
        });
        companyIndex += 1;
    }
   return (
        <div style={{width:"85%"}}>
            <Line data={chartData} options={options} width={1} height={1} />
        </div>);
}
// <Line data={chartData} options={options} width={1} height={1} />