<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        Information Retrieval Systems - Project
      </div>

      <v-spacer></v-spacer>

      <div>
        <v-btn color="accent" large @click.stop="showModal=true">
          ABOUT
        </v-btn>    
        <Modal v-model="showModal" />
      </div>
    </v-app-bar>

    <v-content>
      <Search :query.sync="query" :search="search" :switchPRF="togglePRF"/>
      <Results :results="results" :query="querySubmited" :loading="sentRequest" />
    </v-content>
  </v-app>
</template>

<script>
import Search from './components/Search';
import Results from './components/Results'
import Modal from './components/Modal'
export default {
  name: 'App',

  components: {
    Search,
    Results, 
    Modal
  },

  data() {
    return {
      query: "",
      querySubmited: "",
      results: [], 
      sentRequest: false,
      showModal: false,
      PRF: false
    }
  }, 

  methods: {
     search() {
        console.log("Search: " + this.query)
        this.querySubmited = this.query
        this.sentRequest = true
        fetch('http://localhost:5000/api/search?q=' + this.query + '&prf=' + this.PRF, {
          method: 'get'
        })
        .then((response) => {
          return response.json()
        })
        .then((jsonData) => {
          this.results = jsonData
          console.log(this.results)
          this.sentRequest = false
        })
      },
      togglePRF() {
        this.PRF = !this.PRF
      }
  },

  // mounted: function() {
  //   fetch('http://localhost:5000/api/search?q=tebra%20olivar%20universidad', {
  //     method: 'get'
  //   })
  //   .then((response) => {
  //     return response.json()
  //   })
  //   .then((jsonData) => {
  //     this.results = jsonData
  //     console.log(this.results)
  //   })
  // }
};
</script>
