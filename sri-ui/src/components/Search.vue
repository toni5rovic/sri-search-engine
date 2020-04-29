<template>
  <v-container class="pa-0">
    <v-row class="text-center" justify="center">
      <v-col cols="12">
      </v-col>

      <v-col class="mb-4" cols="12">
        <!-- <h1 class="display-2 font-weight-bold mb-3">
          Search Engine
        </h1> -->
        <img src="../assets/poni-search-logo-fin2.png"/>
      </v-col>

      <v-col  cols="7">
        <v-text-field class="pa-0 ma-0" hide-details label="Search" filled 
        prepend-icon="search" append-icon="close" 
        v-model="query"
        @keyup="$emit('update:query', query);"
        v-on:keydown.enter="onEnter"
        @click:append="clearSearch">

        </v-text-field>
      </v-col>
      <v-col cols="7" class="pa-0 ma-0">
        <v-row justify="center" class="pa-0 ma-0">
          <v-col cols="5" class="pa-0 ma-0">
            <v-spacer></v-spacer>
            <v-switch hide-details class="pa-0" v-model="prf" 
            label="Pseudo relevance feedback">
            </v-switch>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'Search',
    props: ['search', 'switchPRF'],
    methods: { 
      clearSearch() {
        this.query = ""
      },
      onEnter() {
        this.search()
      },

    },

    watch: {
      prf(){
        this.switchPRF()
      }
    },

    data: () => {
      return {
        query: "",
        prf: false
        //results: []
      }
    }
  }
</script>
