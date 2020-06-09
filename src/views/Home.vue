<template>
  <div class="home">
    <v-list subheader>
      <v-list-item v-for="item in items" :key="item.key" :to="item.key" link>
        <v-list-item-avatar>
          <v-icon class="icon" v-text="item.icon" />
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
.icon {
  color: black;
  font-style: normal;
}
.value {
  backdrop-filter: blur(1px);
  background: rgba(158, 158, 158, 0.4);
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
import data, { getData, dataItems, dataUnit } from '@/plugins/data';
import { getValueString } from '@/utils';

export default {
  name: 'Home',
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
        const last = data.get(dataItem.title)[0];
        const diff = last.value - data.get(dataItem.title)[1].value;
        item.key = dataItem.key;
        item.icon = dataItem.icon;
        item.title = dataItem.title;
        item.subtitle = `${dataUnit}，更新：${last.date}`;
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
    },
  },
  created: async function() {
    if (Object.keys(data).length === 0) await this.getData();
    this.setItems();
  },
};
</script>
