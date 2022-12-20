<template>
    <div id="cy">
       
    </div>
</template>
<script>
import cytoscape from 'cytoscape';
import cola from 'cytoscape-cola';

cytoscape.use( cola );
let cy = null;
export default {
    props: ["graph"],
    data() {
        return {
            
        }
    },
    mounted() {
        
        cy = cytoscape({
            container: document.getElementById('cy'),
            elements: this.graph,
            layout: {
                name: 'cola',
            },
            style: [ // the stylesheet for the graph
                {
                selector: 'node',
                style: {
                    'background-color': 'data(color)',
                    'label': 'data(id)'
                }
                },

                {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
                }
            ]
        });
        console.log(cy)
    },
}
</script>
<style>
#cy {
    width: 100%;
    height: 700px;
    outline: black dotted 1px;
}
</style>