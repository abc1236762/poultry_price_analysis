<template>
  <div class="home">
    <v-list subheader>
      <v-list-item v-for="item in items" :key="item.key" :to="item.link" link>
        <v-list-item-avatar>
          <v-icon
            color="black"
            style="font-style: normal;"
            v-text="item.icon"
          ></v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title v-text="item.title" />
          <v-list-item-subtitle v-text="item.subtitle" />
        </v-list-item-content>
        <v-list-item-icon>
          <v-icon large :color="item.color" v-text="item.status" />
          <v-list-item-title class="value">
            <pre v-text="item.value" />
          </v-list-item-title>
        </v-list-item-icon>
      </v-list-item>
    </v-list>
    <v-overlay :value="isLoading">
      <v-progress-circular indeterminate size="64" />
    </v-overlay>
  </div>
</template>

<style lang="scss" scoped>
.value {
  backdrop-filter: blur(1px);
  background: rgba(64, 64, 64, 0.5);
  border-radius: 16px;
  height: 32px;
  line-height: 32px;
  margin-left: -12px;
  position: absolute;
  text-align: center;
  width: 60px;
}
</style>

<script>
import data, { getData, dataItems } from '@/plugins/data';
import { getValueString } from '@/utils';

// import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'Home',
  components: {
    // HelloWorld,
  },
  data: () => ({
    isLoading: false,
    items: [],
  }),
  methods: {
    async getData() {
      this.isLoading = true;
      await getData();
      this.isLoading = false;
    },
    setItems() {
      for (const dataItem of dataItems) {
        const item = {};
        const last = data[dataItem.title][0];
        const diff = last.value - data[dataItem.title][100].value;
        item.key = dataItem.key;
        item.icon = dataItem.icon;
        item.title = `${dataItem.title}`;
        item.subtitle = `最後更新日期：${last.date}`;
        item.value = getValueString(last.value);
        item.link = dataItem.link;
        item.color = 'grey';
        item.status = 'mdi-trending-neutral';
        if (diff > 0) {
          item.color = 'red';
          item.status = 'mdi-trending-up';
        } else if (diff < 0) {
          item.color = 'green';
          item.status = 'mdi-trending-down';
        }
        this.items.push(item);
      }
      // TODO
    },
  },
  created: function() {
    if (Object.keys(data).length === 0) this.getData();
    this.setItems();
  },
};
// mdi-trending-up mdi-trending-down mdi-trending-neutral
</script>
