<template>
<b-card no-body class="mb-1">
    <b-card-header header-tag="header" class="p-1" role="tab">
      <b-button block v-b-toggle=accordion variant="info">
       <b>{{index}}</b> 
       <h6 class="row-title">{{title}}</h6>
      </b-button>
    </b-card-header>
    <b-collapse :id="'accordion-' + index" accordion="my-accordion" role="tabpanel">
    <b-card-body>
      <b-card-text class="text-left">
        <h5 class="text-center">General Info</h5>
        <div>
          <b>Title: </b> {{title}}
        </div>
        <div>
          <b>Identifier: </b> {{identifier}}
        </div>
        <div>
          <b>Type: </b> {{type}}
        </div>
        <div>
          <b>Type (Scheme): </b> {{type_scheme}}
        </div>
        <div>
          <b>Creator: </b> {{creator}}
        </div>
        <div>
          <b>Creator (Scheme): </b> {{creator_scheme}}
        </div>
        <div>
          <b>Language: </b> {{language}}
        </div>
        <div>
          <b>Modified: </b> {{modified}}
        </div>
        <h5 class="text-center">External Links</h5>
        <div>
        <b>Zoek Overheid:</b> <a :href="zoek_url" target="_blank"> {{zoek_url}}</a>
        </div>
        <div v-for="(url, index) in urls" :key="'url-' + index">
            <b>{{ url['$']['manifestation'] }}: </b> <a :href="url['_']" target="_blank"> {{url['_']}}</a>
        </div>
      </b-card-text>
    </b-card-body>
  </b-collapse>
</b-card>
</template>
  
<script>
  
export default {
    props: ["record", "index"],
    data() {
      return {
        owskern: {},
        accordion: 'accordion-' + this.index,
        urls: [],
        zoek_url: ""
      }
    },
    computed: {
        title() {
            if (this.owskern['dcterms:title']) {
                return this.owskern['dcterms:title'][0];
            }
        },
        creator() {
            if (this.owskern['dcterms:creator']) {
                let res = ""
                for (let i = 0; i < this.owskern['dcterms:creator'].length; i++) {
                    res +=  this.owskern['dcterms:creator'][i]['_'] + ',';
                }
                return res.substring(0, res.length - 1);
            }
        },
        creator_scheme() {
            if (this.owskern['dcterms:creator']) {
                let res = ""
                for (let i = 0; i < this.owskern['dcterms:creator'].length; i++) {
                    if(this.owskern['dcterms:creator'][i]['$'])
                        res +=  this.owskern['dcterms:creator'][i]['$']['scheme'] + ',';
                }
                return res.substring(0, res.length - 1);
            }
        },
        identifier() {
            if (this.owskern['dcterms:identifier']) {
                return this.owskern['dcterms:identifier'][0];
            }
        },
        language() {
            if (this.owskern['dcterms:language']) {
                return this.owskern['dcterms:language'].join(",");
            }
        },
        type_scheme() {
            if (this.owskern['dcterms:type']) {
                let res = ""
                for (let i = 0; i < this.owskern['dcterms:type'].length; i++) {
                    if(this.owskern['dcterms:type'][i]['$'])
                        res +=  this.owskern['dcterms:type'][i]['$']['scheme'] + ',';
                }
                return res.substring(0, res.length - 1);
            }
        },
        type() {
            if (this.owskern['dcterms:type']) {
                let res = ""
                for (let i = 0; i < this.owskern['dcterms:type'].length; i++) {
                    res +=  this.owskern['dcterms:type'][i]['_'] + ',';
                }
                return res.substring(0, res.length - 1);
            }
        },
        modified() {
            if (this.owskern['dcterms:modified']) {
                return this.owskern['dcterms:modified'][0];
            }
        }
    },
    methods: {
      
    },
    mounted() {
        // console.log(this.record)
        this.owskern = this.record['sru:recordData'][0]['gzd:gzd'][0]['gzd:originalData'][0]['overheidwetgeving:meta'][0]['overheidwetgeving:owmskern'][0];
        this.urls = this.record['sru:recordData'][0]['gzd:gzd'][0]['gzd:enrichedData'][0]['gzd:itemUrl'];
        const exist_zoek_url = this.record['sru:recordData'][0]['gzd:gzd'][0]['gzd:enrichedData'][0]['gzd:preferredUrl'];
        if (exist_zoek_url)
            this.zoek_url = this.record['sru:recordData'][0]['gzd:gzd'][0]['gzd:enrichedData'][0]['gzd:preferredUrl'][0];

    }
  }
</script>
<style>
.row-title {
    /* text-align: initial; */
}
</style>
  