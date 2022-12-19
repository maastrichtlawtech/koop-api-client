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
                <div v-if="citation['extref']['$']['soort'] == 'URL'">
                  <span class="mx-3">[{{ citation['extref']['_'] }}]</span><a target="_blank" :href="citation['extref']['$']['doc']">{{citation['extref']['$']['doc']}}</a>
                </div>
                <div v-else-if="citation['extref']['$']['soort'] == 'document'">
                  <span class="mx-3">[{{ citation['extref']['_'] }}]</span><a target="_blank" :href="'https://zoek.officielebekendmakingen.nl/' + citation['extref']['$']['doc']">{{'https://zoek.officielebekendmakingen.nl/' + citation['extref']['$']['doc']}}</a>
                </div>
              </li>
            </ol>
        </div>
      </b-card-text>
    </b-card-body>
  </b-collapse>
</b-card>
</template>
  
<script>
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
      async find_citations(depth) {
        this.loading_citations = true;

        let url = new URL("https://koop-api-client-flying-forward.vercel.app/api/find_citations")
        url.searchParams.append('xml_url', this.xml_url);
        url.searchParams.append('depth', 1);
        const response = await fetch(url);
        console.log(response);
        const text = await response.text();
        console.log(text);
        console.log('dd');
        const matches = await response.json();
        console.log(matches);
        // let xml = await response.text();

        // const myRe = new RegExp('<extref(.*?)</extref>', 'g');
        // let matches = xml.match(myRe);
        // if (matches) {
        //   for (let i = 0; i < matches.length; i++) {
        //     parseString(matches[i], (err, result) => {
        //       this.citations.push(result);
        //       if (i == matches.length-1) {
        //         this.loading_citations = false;
        //         this.already_loaded_citations = true;
        //       }
        //     });
        //   }
        // }
        // else {
        //   this.loading_citations = false;
        //   this.already_loaded_citations = true;
        // }
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
  