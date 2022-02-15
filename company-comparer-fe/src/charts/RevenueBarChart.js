import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';




export default function RevenueBarChart(props) {
    ChartJS.register(
      CategoryScale,
      LinearScale,
      BarElement,
      Title,
      Tooltip,
      Legend
    );

    function genRandomRGBString() {
      const r = Math.floor(Math.random() * 255);
      const g = Math.floor(Math.random() * 255);
      const b = Math.floor(Math.random() * 255);
      return `rgba(${r}, ${g}, ${b}, 0.5)`;
    }

    const options = {
      responsive: true,
      plugins: {
        legend: {
          // Switch to top maybe
          position: 'bottom',
        },
        title: {
          display: true,
          text: 'Revenue',
        },
      },
    };
  
    const labels = ['Revenue'];
  
    let data = {
      labels,
      datasets: []
    };
    const financialData = props.data.data;
    const selectedYear = props.yearSelected || Math.max(props.data.data.years);
    financialData.ciks.forEach(company => {
      data["datasets"].push( {
          label: financialData["company_metadata"][company]["ticker"],
          data: [financialData[company]["absolute"]["revenue"][selectedYear]],
          backgroundColor: genRandomRGBString(),
      });
    })
    return <Bar options={options} data={data} />
}
