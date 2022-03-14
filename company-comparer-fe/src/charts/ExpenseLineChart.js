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


export default function ExpenseLineChart(props) {
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

    // TODO move to external config file
    const fieldFormatting = {
        "revenue": {"text": "Revenue"},
        "cogs": {"text": "COGS"},
        "grossprofit": {"text": "Gross Profit"},
        "rd": {"text": "R&D"},
        "sga": {"text": "SG&A", "style": ""},
        "sm": {"text": "SM"},
        "ga": {"text": "GA"},
        "oth": {"text": "Other"},
        "op": {"text": "EBIT"}
    }

    const options = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: fieldFormatting[props.expenseCat]["text"]
            },
            legend: {
                // Switch to top maybe
                  position: 'bottom',
            },
        }
    }

    

    const financialData = props.data.data;
    const selectedYears = props.data.data.years;
    const expLine = props.expenseCat;
    // Sort selected years
    selectedYears.sort();
    // Remove first element
    chartData.labels = selectedYears;
    let companyIndex = 0;
    for (let company of financialData.ciks) {
        let companyExpense = [];
        for (let year of selectedYears) {
            companyExpense.push(financialData[company]["norm"][expLine][year]);
        }
        chartData.datasets.push({
            label: financialData["company_metadata"][company]["ticker"],
            data: companyExpense,
            borderColor: colorStrings[companyIndex],
            backgroundColor: colorStrings[companyIndex],
            spanGaps: true
        });
        companyIndex += 1;
    }
   return (
        <div style={{width:"60%"}}>
            <Line data={chartData} options={options} width={1} height={1} />
        </div>);
}
// <Line data={chartData} options={options} width={1} height={1} />