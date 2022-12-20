<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <h1 class="my-3 text-center">Graph</h1>
          <Graph :graph="graph"></Graph>
        </div>
      </div>
    </div>
  </main>
</template>
<script>
export default {
    computed: {
        graph() {
            return this.$store.state.graph.graph;
        }
    },
    mounted() {
        console.log(this.graph);
    },
}
</script>