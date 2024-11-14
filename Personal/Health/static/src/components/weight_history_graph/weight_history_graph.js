/** @odoo-module **/

import { registry } from "@web/core/registry"
import { CharField } from "@web/views/fields/char/char_field"
import { onMounted, onWillUpdateProps } from "@odoo/owl"
import { loadJS } from "@web/core/assets"

// Load Chart.js dynamically
loadJS("/web/static/lib/Chart/Chart.js")

class WeightHistoryGraph extends CharField {
    setup() {
        super.setup();

        this.chart = null;
        this.weightHistoryData = this.parseData(this.props.value);

        onMounted(() => {
            this.renderChart();
        });

        onWillUpdateProps((nextProps) => {
            if (nextProps.value !== this.props.value) {
                this.weightHistoryData = this.parseData(nextProps.value);
                this.updateChart();
            }
        });
    }

    renderChart() {
        const ctx = document.getElementById(`weightHistoryChart${this.props.record.id}${this.props.name}`);
        const data = this.weightHistoryData;

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Peso',
                        data: data.weightValues,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: false
                    },
                    {
                        label: 'Peso Deseado',
                        data: data.desiredWeightValues,
                        borderColor: 'rgba(255, 99, 132, 1)',  // Un color diferente para diferenciar las líneas
                        borderWidth: 2,
                        borderDash: [5, 5],  // Línea discontinua para diferenciar visualmente
                        fill: false
                    }
                ]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'MMM D',  // Formato en el tooltip
                            displayFormats: {
                                day: 'MMM D',  // Formato de visualización
                            },
                            parser: 'YYYY-MM-DD',  // Define cómo se debe parsear la fecha
                        },
                        title: {
                            display: true,
                            text: 'Fecha'
                        },
                        ticks: {
                            source: 'auto',
                            autoSkip: true,
                            maxRotation: 0,
                            major: {
                                enabled: true,
                            },
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Peso'
                        }
                    }
                }
            }
        });
    }

    updateChart() {
        if (this.chart) {
            this.chart.data.labels = this.weightHistoryData.labels;
            this.chart.data.datasets[0].data = this.weightHistoryData.values;
            this.chart.update();
        }
    }

    parseData(dataString) {
        const data = JSON.parse(dataString);
        const labels = data.map(item => item[0]);  // Mantén la fecha como string en el formato 'YYYY-MM-DD'
        const weightValues = data.map(item => item[1]);
        const desiredWeightValues = data.map(item => item[2]);  // Peso Deseado
        return { labels, weightValues, desiredWeightValues};
    }
}

WeightHistoryGraph.template = "Health.WeightHistoryGraph";
WeightHistoryGraph.supportedTypes = ["char"];

registry.category("fields").add("weight_history_graph", WeightHistoryGraph);
