import logo from './logo.svg';
import './App.css';
import { React, useState } from 'react';
import Financials from './financials/Financials';
import CompanySearchBar from './search/CompanySearch';
import axios from 'axios';
import Grid from '@material-ui/core/Grid';

function App() {
  const [financials, setFinancials] = useState({data : {}});

  function getFinancials(companies) {
    // Empty company data object, that we will pass to 
    let company_meta = {}
    let cikQuery = ""
    for (let company in companies) {
      cikQuery += companies[company]["cik"];
      cikQuery += "&";
      company_meta[companies[company]["cik"]] = companies[company];
    }
    cikQuery = cikQuery.slice(0, -1);
    axios.get(`http://127.0.0.1:5000/company_data/${cikQuery}`)
    .then(resp => resp.data)
    .then(data => {
      data.data["company_metadata"] = company_meta;
      setFinancials(data);
    })//setFinancials(data))
    .catch(err => console.log);
  }

  return (
    <div className="App">
      <Grid container spacing={2}>
        <Grid item justifyContent="center" xs={12}>
          <CompanySearchBar handleChange={getFinancials} />
        </Grid>
        <Grid item justifyContent="center" xs={12}>
          { Object.keys(financials.data).length !== 0 ? <Financials data={financials} /> : "Enter some companies to begin"} 
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
