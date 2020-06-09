<template>
  <div class="page">
    <v-card class="ma-4 mx-sm-auto" raised max-width="600">
      <v-list-item>
        <v-list-item-content>
          <v-icon class="icon" large v-text="item.icon"></v-icon>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title class="headline text-center" v-text="item.title" />
          <v-list-item-subtitle class="text-center">
            更新時間：{{ data[0].date }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-card-text>
        <v-row align="center">
          <v-col class="display-3" cols="6">
            23&deg;C
          </v-col>
          <v-col cols="6">
            <v-img
              src="https://cdn.vuetifyjs.com/images/cards/sun.png"
              alt="Sunny image"
              width="92"
            ></v-img>
          </v-col>
        </v-row>
      </v-card-text>
      <v-list-item>
        <v-list-item-icon>
          <v-icon>mdi-send</v-icon>
        </v-list-item-icon>
        <v-list-item-subtitle>23 km/h</v-list-item-subtitle>
      </v-list-item>
    </v-card>
    <v-card class="ma-4 mx-sm-auto" raised max-width="600">
      <v-list-item>
        <v-menu
          ref="menu1"
          v-model="menu1"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="dateFormatted"
              label="Date"
              persistent-hint
              prepend-icon="event"
              v-bind="attrs"
              @blur="date = parseDate(dateFormatted)"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="date"
            no-title
            @input="menu1 = false"
          ></v-date-picker>
        </v-menu>
      </v-list-item>
      <v-list-item>
        <v-menu
          v-model="menu2"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="computedDateFormatted"
              label="Date (read only text field)"
              hint="MM/DD/YYYY format"
              persistent-hint
              prepend-icon="event"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="date"
            no-title
            @input="menu2 = false"
          ></v-date-picker>
        </v-menu>
      </v-list-item>
    </v-card>
  </div>
</template>

<style lang="scss" scoped>
.icon {
  color: black;
  font-style: normal;
}
</style>

<script>
import data, { dataItems } from '@/plugins/data';

export default {
  computed: {
    item() {
      for (const dataItem of dataItems) {
        if (dataItem.key === this.$route.params.key) return dataItem;
      }
      return null;
    },
    data() {
      return data.get(this.item.title);
    },
  },
  // TODO
};
</script>
