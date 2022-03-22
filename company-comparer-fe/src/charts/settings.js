const settings = {
    // We want legend to be on bottom
    legendPosition: 'bottom',
    // We do not want to allow the removal of datasets for revenue share
    preventDataRemoval: function(e, legendItem, legend) {
        const index = legendItem.datasetIndex;
        const type = legend.chart.config.type;
    }
}

export default settings;