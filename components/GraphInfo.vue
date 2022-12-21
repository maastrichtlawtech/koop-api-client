<template>
  <b-sidebar id="graph-info" :title="info.title" bg-variant="dark" text-variant="light" shadow>
    <div class="px-3 py-2">
      <div class="info-section py-2">
        <h4>{{ info.general.title }}</h4>
        <div v-for="t in info.general.tuples" :key="t.name">
          <span>{{ t.name }}:</span> <span>{{ t.value }}</span>
        </div>
      </div>
      <div class="info-section py-2">
        <h4>{{ info.selected_node.title }}</h4>
        <div v-for="t in info.selected_node.tuples" :key="t.name">
          <span>{{ t.name }}:</span> 
          <a v-if="t.name=='link'" :href="t.value" target="_blank">{{ t.value }}</a>
          <span v-else>{{ t.value }}</span>
        </div>
      </div> 
    </div>
  </b-sidebar>
</template>
<script>
  
export default {
      props: ["info"],
      data() {
          return {
              
          }
      },
      mounted() {
          console.log(this.info)
      },
  }
</script>
<style>
.info-section {
  border-bottom: 1px solid white;
}
</style>
