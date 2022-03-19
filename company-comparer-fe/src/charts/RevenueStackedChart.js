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

    // We do not want to allow the removal of datasets on revenue share
    const newLegendClickHandler = function (e, legendItem, legend) {
        const index = legendItem.datasetIndex;
        const type = legend.chart.config.type;
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
                  onClick: newLegendClickHandler
                  // display: false
            },
        },
        scales: {
            x: {

            },
            y: {
                stacked: true
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
            revenueTotal[year] += financialData[company]["absolute"]["revenue"][year];
        });
    });
    for (let company of financialData.ciks) {
        let companyRevenueShare = [];
        for (let year of selectedYears) {
            companyRevenueShare.push((financialData[company]["absolute"]["revenue"][year] / revenueTotal[year]));
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