import React from 'react';
import { Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend, 
    Filler} from 'chart.js';
import { Line } from 'react-chartjs-2';
import settings from './settings.js';


export default function RevenueStackedChart(props) {
    ChartJS.register(CategoryScale,
        LinearScale,
        PointElement,
        LineElement,
        Title,
        Tooltip,
        Legend,
        Filler);
    let colorStrings = ['rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)'];
    let chartData = {
        labels: [],
        datasets: []
    };

    const options = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Revenue Share'
            },
            legend: {
                  position: settings.legendPosition,
                  onClick: settings.preventDataRemoval
            },
        },
        scales: {
            x: {

            },
            y: {
                stacked: true,
                min: 0.0,
                max: 1.0
            },
        },
        elements: {
            point: {
                radius: 0
            }
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
    // Construct revenue total object
    let revenueTotal = {};
    selectedYears.forEach((year) => {
        revenueTotal[year] = 0;
        financialData.ciks.forEach(company => {
            revenueTotal[year] += financialData[company]["is"]["absolute"]["revenue"][year];
        });
    });
    for (let company of financialData.ciks) {
        let companyRevenueShare = [];
        for (let year of selectedYears) {
            companyRevenueShare.push((financialData[company]["is"]["absolute"]["revenue"][year] / revenueTotal[year]));
        }
        chartData.datasets.push({
            label: financialData["company_metadata"][company]["ticker"],
            fill: true,
            backgroundColor: colorStrings[companyIndex],
            pointBackgroundColor: colorStrings[companyIndex],
            borderColor: colorStrings[companyIndex],
            pointHighlightStroke: colorStrings[companyIndex],
            spanGaps: true,
            data: companyRevenueShare,
        });
        companyIndex += 1;
    }
   return (
        <div style={{width:"60%"}}>
            <Line data={chartData} options={options} width={1} height={1} />
        </div>);
}
// <Line data={chartData} options={options} width={1} height={1} />