<template>
  <v-container>
    <v-row v-if="loading == true" justify="center" class="pa-0 ma-0 text-center">
      <v-col cols="6" sm="7">
        <div>
          <v-progress-circular indeterminate color="primary">
          </v-progress-circular>
        </div>
      </v-col>
    </v-row>
    <v-row v-if="query != '' && results.length > 0 && loading == false" justify="center" class="pa-0 ma-0">
      <v-col cols="6" sm="7">
        <span class="font-weight-black">{{ results.length }}</span>
         {{ results.length == 1 ? 'result' : 'results' }} for
        <span class="font-weight-black">{{ query }}</span>
      </v-col>
    </v-row>
    <v-row v-if="query != '' && results.length == 0 && loading == false" justify="center" class="pa-0 ma-0">
      <v-col cols="6" sm="7">
         No results for 
        <span class="font-weight-black">{{ query }}</span>
      </v-col>
    </v-row>
    <v-row v-if="results.length > 0 && loading == false" no-gutters justify="center">
      <v-col v-for="fileRes in this.results" :key="fileRes.fileID" cols="6" sm="7">
        <v-card class="mb-2" target="_blank">
          <v-container class="pa-0 ma-0">
            <v-row class="pa-0 ma-0" justify="space-between">
              <v-col class="pa-0 ma-0" col="11">
                <v-list-item col="12" three-line dense>
                  <v-list-item-content class="pa-0">
                    <v-list-item-title class="mb-1">{{ fileRes.fileName }}</v-list-item-title>
                    <v-list-item-subtitle class="mb-1">{{ fileRes.similarity }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
              <v-col class="pa-0" cols="auto">
                <div class="mt-5 mr-2">
                  <v-btn :href=getFile(fileRes.filePath) icon target="_blank">
                    <font-awesome-icon icon="external-link-alt" />
                  </v-btn>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Results",
  methods: {
    getFile(fileName) {
      return 'http://localhost:5000/api/file/' + fileName
    }
  },

  props: {
    loading: {
      type: Boolean,
      defualt() {
        return false
      }
    },
    query: {
      type: String,
      defualt() {
        return ""
      }
    },
    results: {
      type: Array,
      default() {
        return [];
      }
    }
  }
};
</script>
