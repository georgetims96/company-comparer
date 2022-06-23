import React from 'react';

export default function IncomeStatement(props) {
    // TODO These should probably be in a config file
    const possibleFields = ["revenue", "cogs", "grossprofit", "rd", "sga", "sm", "ga","oth", "op"];
    // Maps JSON fields to appropriate user-friendly name
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

    function openFiling(e) {
        // Make sure it's a double click
        if (e.detail === 2) {
            // Get the 10-K identifier
            const rawText = e.currentTarget.id;
            // The below converts the identifier to a link
            const linkDetails = rawText.split('&');
            let cik = linkDetails[0];
            cik = cik.replace(/^0+/, '');
            //https://www.sec.gov/Archives/edgar/data/320193/000032019321000105/
            let accnOrig = linkDetails[1]
            let accnTrunc = accnOrig.replace(/-/g, '');
            // Redirect user to link
            window.open(`https://www.sec.gov/Archives/edgar/data/${cik}/${accnTrunc}/${accnOrig}-index.html`);
        }
    }
    
    function renderIncomeFields(financialData) {
        // Construct the "other" line. In short, it's a plug given other values
        // TODO move this into a separate function
        for (let company of financialData["ciks"]){
            financialData[company]["is"]["norm"]["oth"] = {}
            for (let year in financialData[company]["is"]["norm"]["revenue"]) {
                let rev = financialData[company]["is"]["norm"]["revenue"][year];
                let cogs = financialData[company]["is"]["norm"]["cogs"][year] === "N/A" ? 0 : financialData[company]["is"]["norm"]["cogs"][year];
                let rd = financialData[company]["is"]["norm"]["rd"][year] === "N/A" ? 0 : financialData[company]["is"]["norm"]["rd"][year];
                let sga = financialData[company]["is"]["norm"]["sga"][year] === "N/A" ? 0 : financialData[company]["is"]["norm"]["sga"][year];
                let op = financialData[company]["is"]["norm"]["op"][year] === "N/A" ? 0 : financialData[company]["is"]["norm"]["op"][year];
                financialData[company]["is"]["norm"]["oth"][year] = 
                    financialData[company]["is"]["norm"]["grossprofit"][year] === "N/A" 
                        ? rev - cogs - rd - sga - op 
                        : financialData[company]["is"]["norm"]["grossprofit"][year] - rd - sga - op;
            }
        }
        // Add calculated 'other' to 'fields' property
        // financialData.fields.push("oth");
        // If user hasn't selected a year, default to most recent
        const year = props.yearSelected || Math.max(...financialData["years"]);
        // Get all the financial fields provided, converting to set for efficiency
        const fieldsToRender = new Set(financialData.fields);
        // Get all the companies provided
        const companiesToRender = financialData.ciks;
        // alert(financialData[companiesToRender[0]]["is"]["norm"]['cogs']['2015']);
        const numCompanies = companiesToRender.length;
        // Generate table rows based on company JSON data and financial fields
        let tableRowsToRender = [];
        
        tableRowsToRender.push(<tr>
            <td><i>{year}</i></td>
                { companiesToRender.map(cik => 
                <td onClick={openFiling} id={`${cik}&${financialData[cik]['accn'][year]}`}><b>{numCompanies < 2 ? financialData["company_metadata"][cik]["name"] : financialData["company_metadata"][cik]["ticker"]} </b></td>)}
            </tr>)
        possibleFields.forEach(field => {
            if (fieldsToRender.has(field)) {
                tableRowsToRender.push(
                    <tr id={field} onMouseDown={props.handleChartChange}>
                        <td className={`statement_header ${field}_header`}>{ fieldFormatting[field]["text"] }</td>
                        { companiesToRender.map(company => <td className={field}> { !(year in financialData[company]["is"]["norm"][field]) || financialData[company]["is"]["norm"][field][year] === "N/A" ? "N/A" : financialData[company]["is"]["norm"][field][year].toFixed(2) }</td>) }
                    </tr>
                );
            }
        });
        
        
        return tableRowsToRender;
    }

    return (
        <div className="financialStatements"> 
            <table cellspacing={0} className="incomeStatement">
                {renderIncomeFields(props.data.data)}
            </table>
        </div>
    );
}