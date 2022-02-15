import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import axios from 'axios';

export default function CompanySearchBar(props) {
    // Should put these defaults in a config file
    const [options, setOptions] = useState([{
        "cik": "0000320193", 
        "name": "Apple inc.", 
        "ticker": "AAPL"
    }]);

    const [input, setInput] = useState('');
    const [value, setValue] = useState([])

    function handleSearch() {
    axios.get(`http://127.0.0.1:5000/company_code/search/${input}`)
        .then(resp => resp.data)
        .then(data => setOptions(data.search_results))
        .catch(err => console.log(err));
    }
    return (
        <div>
            <Autocomplete
                multiple
                id="tags-standard"
                options={options.filter(option => {
                    for (let val of value) {
                        if (val.ticker === option.ticker) {
                            return false;
                        }
                    }
                    return true;
                })}
                getOptionLabel={(option) => `${option.name} (${option.ticker})`}
                onInputChange={(e, newInput) => {
                    setInput(newInput);
                    handleSearch();
                }}
                onChange={(e, newValue) => {
                    if (newValue.length <=5 ) {
                        props.handleChange(newValue)
                        setValue([...newValue]);
                    }
                    else {
                        alert("Max number of companies is 5!");
                    }
                }}
                value ={value}
                renderInput={(params) => (
                <TextField
                    {...params}
                    label="Enter Company"
                    placeholder=""
                />
            )}
        />
      </div>
    );
}