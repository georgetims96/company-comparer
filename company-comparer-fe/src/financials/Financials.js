import { useState, React } from 'react';
import Grid from '@material-ui/core/Grid';
import IncomeStatement from './IncomeStatement';
import RevenueDonutChart from '../charts/RevenueDonutChart';
import RevenueBarChart from '../charts/RevenueBarChart';
import ExpenseLineChart from '../charts/ExpenseLineChart'
import RevenueLineChart from '../charts/RevenueLineChart';
import RevenueStackedChart from '../charts/RevenueStackedChart';
import Paper from '@mui/material/Paper'

export default function Financials (props) {
    const [year, setYear] = useState(props.data.data.years[0]);
    const [chartType, setChartType] = useState("revenue_growth");

    function updateYear(e) {
        setYear(e.target.value);
        setChartType(prevState => prevState);
    }

    function updateChart(e) {
        setChartType(e.currentTarget.id);
    }

    function determineChart(chartTypeInput) {
        switch (chartTypeInput) {
            case "revenue":
                // RevenueDonutChart
                return <RevenueStackedChart data = {props.data} yearSelected={year} />;
            case "revenue_growth":
                return <RevenueLineChart data = {props.data} />;
            default:
                return <ExpenseLineChart data = {props.data} expenseCat ={chartTypeInput} />;
        }
    }

    

    // Get years from data, sort in descending order, and construct select component, with max year (i.e most recent) 
    // the default
    let yearOptions = (props.data.data.years)
    .sort(function(a, b){return b - a})
    .map(yearOption => <option value={yearOption}>{yearOption}</option>);
    let yearSelection = <select defaultValue={yearOptions[0]} onChange={updateYear}>
        {yearOptions}
        </select>;
    return (<div>
                {yearSelection}
                <Paper>
                    <Grid container spacing={1}>
                        <Grid item
                            direction="column"
                            style={{
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center"
                            }} 
                            xs={12} md={6}>
                            {determineChart(chartType)}
                        </Grid>
                        <Grid 
                            item
                            direction="column"
                            style={{
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center"
                            }}
                        xs={12} md={6}>
                            <IncomeStatement data={props.data} yearSelected={year} handleChartChange={updateChart}/>
                        </Grid>
                    </Grid>
                </Paper>
        </div>);
}

//<RevenueDonutChart data={props.data} yearSelected={year} />


