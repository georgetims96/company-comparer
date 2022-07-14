import React from 'react';

export default function CashFlowStatement(props) {
    // TODO These should probably be in a config file
    // Order of possible fields dictates order of appearance
    const possibleFields = ["op", "ni", "da", "sbc", "ar_delta", "inv_delta", "ap_delta", "dr_delta", "wc_delta", "cfo", "ppe", "acq", "cfi"];
    // Maps JSON fields to appropriate user-friendly name
    const fieldFormatting = {
        "ni": {"text": "N/I"},
        "op": {"text": "EBIT"},
        "cfo": {"text": "CFO"},
        "da": {"text": "D&A"},
        "sbc": {"text": "SBC"},
        "ar_delta": {"text": "Δ A/R"},
        "inv_delta": {"text": "Δ Inv."},
        "ap_delta": {"text": "Δ A/P"},
        "dr_delta": {"text": "Δ D/R", "style": ""},
        "wc_delta": {"text": "Δ W/C"},
        "cfi": {"text" : "CFI"},
        "ppe": {"text": "PPE"},
        "acq": {"text": "Acq.'s"}
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
    
    function renderCashFields(financialData) {
        
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
            </tr>);

        possibleFields.forEach(field => {
            if (fieldsToRender.has(field)) {
                tableRowsToRender.push(
                    <tr id={field} onMouseDown={props.handleChartChange}>
                        <td className={`statement_header_cf ${field}_header_cf`}>{ fieldFormatting[field]["text"] }</td>
                        { companiesToRender.map(company => <td className={`${field}_cf`}> { !(year in financialData[company]["cf"]["norm"][field]) || financialData[company]["cf"]["norm"][field][year] === "N/A" ? "N/A" : financialData[company]["cf"]["norm"][field][year].toFixed(2) }</td>) }
                    </tr>
                );
            }
        });
        
       // { companiesToRender.map(company => <td className={field}> { !(year in financialData[company]["cf"]["norm"][field]) || financialData[company]["cf"]["norm"][field][year] === "N/A" ? "N/A" : financialData[company]["cf"]["norm"][field][year].toFixed(2) }</td>) }
        return tableRowsToRender;
    }

    return (
        <div className="financialStatements"> 
            <table cellspacing={0} className="cashFlowStatement">
                {renderCashFields(props.data.data)}
            </table>
        </div>
    );
}