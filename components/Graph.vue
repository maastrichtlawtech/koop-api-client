<template>
  <div>
    <GraphInfo :info="info"></GraphInfo>
    <div id="cy">
    </div>
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
        info: {
          title: "Graph Info",
          general: {
            title: "General",
            tuples: [
              { name: "Total Nodes", value: this.graph.nodes.length },
              { name: "Total Edges", value: this.graph.edges.length }
            ]
          },
          selected_node: {
            title: "Selected Node",
            tuples: [
                
            ]
          },
        }
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
        console.log(cy);

        cy.on('tap', 'node', (evt) => {
          var node = evt.target;
          this.info.selected_node.tuples = [
            { name: "id", value: node.data('id') },
            { name: "link", value: node.data('link') }
          ]
        });
    },
}
</script>
<style>
#cy {
    width: 100%;
    height: calc(100vh - 126px);
    outline: black dotted 1px;
}
</style>