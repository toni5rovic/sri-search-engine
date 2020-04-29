<template>
	<v-dialog v-model="show" max-width="500px">
	<!-- <v-card>
		<v-card-title>
			About
		</v-card-title>
		<v-card-text>
			Antonije Petrovic
		</v-card-text>

        <v-divider></v-divider>
		<v-card-actions>
			<v-btn color="primary" flat @click.stop="show=false">Close</v-btn>
		</v-card-actions>
	</v-card> -->
		<v-card raised>
			<v-card-title class="headline grey lighten-2" primary-title>
				About
			</v-card-title>

			<v-divider></v-divider>

			<v-card-subtitle>
				Information Retrieval System Project
				<br />
				Sistemas de Recuperación de Información - Practicas 
			</v-card-subtitle>

			<v-card-text class="body-1">
				Student: Antonije Petrovic
				<br/>
				Professor: Pilar López Úbeda
			</v-card-text>

			<v-divider></v-divider>

			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary" flat @click.stop="show=false">Close</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
export default {
  props: {
     value: Boolean
  },
  computed: {
    show: {
      get () {
        return this.value
      },
      set (value) {
         this.$emit('input', value)
      }
    }
  }
}
</script>