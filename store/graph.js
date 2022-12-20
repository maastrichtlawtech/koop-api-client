export const state = () => ({
    graph: {
        nodes: [],
        edges: []
    }
  })
  
  export const mutations = {
    add_node (state, node) {
      state.graph.nodes.push(node);
    },
    add_edge (state, edge) {
      state.graph.edges.push(edge);
    },
    clear (state) {
        state.graph = {
            nodes: [],
            edges: []
        };
    }
    // remove (state, { todo }) {
    //   state.list.splice(state.list.indexOf(todo), 1)
    // },
    // toggle (state, todo) {
    //   todo.done = !todo.done
    // }
  }