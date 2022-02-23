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
    // Get financial data passed from props
    const financialData = props.data.data;
    // Construct the "other" line. In short, it's a plug given other values
    for (let company of financialData["ciks"]){
        financialData[company]["norm"]["oth"] = {}
        for (let year in financialData[company]["norm"]["revenue"]) {
            let rev = financialData[company]["norm"]["revenue"][year];
            let cogs = financialData[company]["norm"]["cogs"][year] === "N/A" ? 0 : financialData[company]["norm"]["cogs"][year];
            let rd = financialData[company]["norm"]["rd"][year] === "N/A" ? 0 : financialData[company]["norm"]["rd"][year];
            let sga = financialData[company]["norm"]["sga"][year] === "N/A" ? 0 : financialData[company]["norm"]["sga"][year];
            let op = financialData[company]["norm"]["op"][year] === "N/A" ? 0 : financialData[company]["norm"]["op"][year];
            financialData[company]["norm"]["oth"][year] = financialData[company]["norm"]["grossprofit"][year] === "N/A" ? rev - cogs - rd - sga - op : financialData[company]["norm"]["grossprofit"][year] - rd - sga - op;
        }
    }
    // Add calculated 'other' to 'fields' property
    financialData.fields.push("oth");
    // If user hasn't selected a year, default to most recent
    const year = props.yearSelected || Math.max(...financialData["years"]);
    // Get all the financial fields provided, converting to set for efficiency
    const fieldsToRender = new Set(financialData.fields);
    // Get all the companies provided
    const companiesToRender = financialData.ciks;
    const numCompanies = companiesToRender.length;
    // Generate table rows based on company JSON data and financial fields
    let tableRowsToRender = [];
    tableRowsToRender.push(<tr>
        <td></td>
        { companiesToRender.map(cik => <td><b>{numCompanies < 2 ? financialData["company_metadata"][cik]["name"] : financialData["company_metadata"][cik]["ticker"]} </b></td>)}
    </tr>)
    possibleFields.forEach(field => {
        if (fieldsToRender.has(field)) {
            tableRowsToRender.push(
                <tr>
                    <td className={`statement_header ${field}_header`}>{ fieldFormatting[field]["text"] }</td>
                    { companiesToRender.map(company => <td className={field}> { !(year in financialData[company]["norm"][field]) || financialData[company]["norm"][field][year] === "N/A" ? "N/A" : financialData[company]["norm"][field][year].toFixed(2) }</td>) }
                </tr>
            );
        }
    });
    return (
        <div className="financialStatements"> 
            
            <table cellspacing={0} className="incomeStatement">
                {tableRowsToRender}
            </table>
            </div>
    );
}