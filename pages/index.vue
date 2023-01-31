<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col text-center">
          <div class="search-box mt-5">
            <b-input-group class="mb-2">
              <!-- <b-input-group-prepend> -->
                <b-form-input id="query_input" placeholder="Search"></b-form-input>
              <!-- </b-input-group-prepend> -->
              <b-input-group-append>
                 <b-form-input type="number" value="200" id="limit_input" min="1" step="1"></b-form-input>
                 <b-button @click="search" variant="outline-info">Search</b-button>
              </b-input-group-append>
            </b-input-group>
          </div>
          <div>
            <b-embed
              type="iframe"
              aspect="16by9"
              src="https://fairmodels.org/index.ttl"
              allowfullscreen
            ></b-embed>
          </div>
          <div>
            <b-embed
              type="iframe"
              aspect="16by9"
              src="https://raw.githubusercontent.com/MaastrichtU-CDS/FAIRmodels/main/models/radiotherapy/stiphout_2011.ttl"
              allowfullscreen
            ></b-embed>
          </div>
          <div class="my-5">
            <h2 v-show="records.length && !loading">{{ records.length }}  Results </h2>
            <b-spinner v-show="loading" label="Loading..." variant="info"></b-spinner>
          </div>
          <div class="accordion" role="tablist">
            <div v-for="(record, index) in records" :key="'row-' + index">
              <Record :record="record" :index="index + 1"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
var parseString = require('xml2js').parseString;

export default {
  data() {
    return {
      records: [],
      loading: false,
      graph: {
        nodes: [],
        edges: []
      }
    }
  },
  methods: {
    async search() {
      this.loading = true;
      this.records = [];

      let query = document.getElementById('query_input').value;
      let limit = document.getElementById('limit_input').value;
      let url = new URL("https://koop-api-client-flying-forward.vercel.app/api/search")
      url.searchParams.append('query', query);
      url.searchParams.append('limit', limit);
      const response = await fetch(url);
      let xml = await response.text();
      console.log(response)
      console.log(xml)
      parseString(xml, (err, result) => {
        this.records = result['sru:searchRetrieveResponse']['sru:records'][0]['sru:record'];
        this.loading = false;
      });
      
    }
  },
  mounted() {
    this.$store.commit('graph/clear');
  }
}
</script>
<style>
#limit_input {
  width: 100px;
}
</style>
