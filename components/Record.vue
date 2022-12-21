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
        <h5 class="text-center">Metadata</h5>
        <div>
        <b>Zoek Overheid:</b> <a :href="zoek_url" target="_blank"> {{zoek_url}}</a>
        </div>
        <div v-for="(url, index) in urls" :key="'url-' + index">
            <b>{{ url['$']['manifestation'] }}: </b> <a :href="url['_']" target="_blank"> {{url['_']}}</a>
        </div>
        <div v-show="has_xml" class="text-center my-3">
          <button v-show="!loading_citations && !already_loaded_citations" class="btn btn-outline-primary" @click=find_citations(1)>Find citations</button>
          <h5 v-show="loading_citations || already_loaded_citations">Citations</h5>
          <b-spinner v-show="loading_citations" label="Loading.." variant="info"></b-spinner>
            <ol class="text-left">
              <li class="" v-for="(citation, index) in citations" :key="accordion + '_' + index">
                <span class="mx-3">[{{ citation['extref']['_'] }}]</span><a target="_blank" :href="citation_link(citation)">{{citation_link(citation)}}</a>
              </li>
            </ol>
        </div>
      </b-card-text>
    </b-card-body>
  </b-collapse>
</b-card>
</template>
  
<script>
import { mapMutations } from 'vuex'
var parseString = require('xml2js').parseString;

export default {
    props: ["record", "index"],
    data() {
      return {
        owskern: {},
        accordion: 'accordion-' + this.index,
        urls: [],
        has_xml: false,
        zoek_url: "",
        citations: [],
        xml_url: null,
        loading_citations: false,
        already_loaded_citations: false
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
      citation_link(citation) {
        if(citation['extref']['$']['soort'] == 'document') {
          return 'https://zoek.officielebekendmakingen.nl/' + citation['extref']['$']['doc'];
        }
        else if(citation['extref']['$']['soort'] == 'URL') {
          return citation['extref']['$']['doc'];
        }
        return '/';
      },
      async find_citations(depth) {
        this.loading_citations = true;

        let url = new URL("https://koop-api-client-flying-forward.vercel.app/api/find_citations")
        url.searchParams.append('xml_url', this.xml_url);
        url.searchParams.append('depth', 1);
        const response = await fetch(url);
        const text = await response.text();
        const matches = JSON.parse(text);

        const source = this.identifier;
        this.add_node({ data: { id: source, link: this.zoek_url, color: 'red' }});

        if (matches?.length > 0) {
          for (let i = 0; i < matches.length; i++) {
            parseString(matches[i], (err, result) => {
              this.citations.push(result);
              const target = result['extref']['_'];
              this.add_node({ data: { id: target, link: this.citation_link(result), color: 'lightgray' }});
              this.add_edges({ data: { id: source + target, source: source, target: target }});
              if (i == matches.length-1) {
                this.loading_citations = false;
                this.already_loaded_citations = true;
              }
            });
          }
        }
        else {
          this.loading_citations = false;
          this.already_loaded_citations = true;
        }
      },
      add_node(node) {
        this.$store.commit('graph/add_node', node)
      },
      add_edges(edge) {
        this.$store.commit('graph/add_edge', edge)
      }
    },
    mounted() {
        this.owskern = this.record['sru:recordData'][0]['gzd:gzd'][0]['gzd:originalData'][0]['overheidwetgeving:meta'][0]['overheidwetgeving:owmskern'][0];
        this.urls = this.record['sru:recordData'][0]['gzd:gzd'][0]['gzd:enrichedData'][0]['gzd:itemUrl'];
        for (let i = 0; i < this.urls.length; i++) {
          if(this.urls[i]['$']['manifestation'] == "xml") {
            this.has_xml = true;
            this.xml_url = this.urls[i]['_'];
            break;
          }
        }
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
  