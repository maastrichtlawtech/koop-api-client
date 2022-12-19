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
      loading: false
    }
  },
  methods: {
    async search() {
      this.loading = true;
      this.records = [];

      let query = document.getElementById('query_input').value;
      let limit = document.getElementById('limit_input').value;
      var url = new URL("https://koop-api-client-flying-forward.vercel.app/api/search")
      url.searchParams.append('query', '\"' + query + '\"');
      url.searchParams.append('limit', limit);
      const response = await fetch(url);
      console.log(response)
      // const response = await fetch(`https://repository.overheid.nl/sru?query=cql.textAndIndexes=\"${query}\"&maximumRecords=${limit}`)
      let xml = await response.text();
      console.log(xml)

      parseString(xml, (err, result) => {
        this.records = result['sru:searchRetrieveResponse']['sru:records'][0]['sru:record'];
        this.loading = false;
      });
      
    }
  },
  mounted() {

  }
}
</script>
<style>
#limit_input {
  width: 120px;
}
</style>
