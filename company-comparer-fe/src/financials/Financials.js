import { useState, React } from 'react';
import Grid from '@material-ui/core/Grid';
import IncomeStatement from './IncomeStatement';
import ExpenseLineChart from '../charts/ExpenseLineChart'
import RevenueLineChart from '../charts/RevenueLineChart';
import RevenueStackedChart from '../charts/RevenueStackedChart';
import Paper from '@mui/material/Paper';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import CashFlowStatement from './CashFlowStatement';


function TabPanel(props) {
  const { children, value, index, ...other} = props;
  return (
    <div
      role="tablepanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
     { value === index && (
      <Box sx={{ p: 3}}>
        <Typography>{children}</Typography>
      </Box>
     )} 
    </div>
  );
}

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

function FinancialStatementTabs(props) {
  const [value, setValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setValue(newValue);
  }

  return (
    <Box sx ={{ width: '100%'}}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider'}}>
        <Tabs value={value} onChange={handleTabChange}>
          <Tab label="I/S" {...a11yProps(0)} />
          <Tab label="C/F" {...a11yProps(1)} />
        </Tabs>
        <TabPanel value={value} index={0}>
          <IncomeStatement data={props.data} yearSelected={props.yearSelected} handleChartChange={props.updateChart}/>
        </TabPanel>
        <TabPanel value={value} index={1}>
          <CashFlowStatement data={props.data} yearSelected={props.yearSelected} handleChartChange={props.updateChart}/>
        </TabPanel>
      </Box>
    </Box>
  );

}

export default function Financials (props) {
    const [year, setYear] = useState(props.data.data.years[0]);
    const [chartType, setChartType] = useState("revenue_growth");

    function updateYear(e) {
        setYear(e.target.value);
        setChartType(prevState => prevState);
    }

    function updateChart(e) {
        // Get selected chart type
        let newChartType = e.currentTarget.id;
        // Check to see if it's the same (i.e. we're unclicking)
        if (newChartType === chartType) {
            // If so, set chart back to original revenue growth chart
            setChartType("revenue_growth");
        } else {
            // Otherwise, update chart to new chart type
            setChartType(newChartType);
        }
    }

    function determineChart(chartTypeInput) {
        switch (chartTypeInput) {
            case "revenue":
                // Revenue share chart
                return <RevenueStackedChart data = {props.data} yearSelected={year} />;
            case "revenue_growth":
                // Revenue growth chart
                return <RevenueLineChart data = {props.data} />;
            default:
                // Any other chart will have the same format
                // Differentiate the exact type using expenseCat prop
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
                          <FinancialStatementTabs data={props.data} yearSelected={year} updateChart={updateChart} />
                        </Grid>
                    </Grid>
                </Paper>
        </div>);
}

//<RevenueDonutChart data={props.data} yearSelected={year} />


