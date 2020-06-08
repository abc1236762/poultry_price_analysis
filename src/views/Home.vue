<template>
  <div class="home">
    <v-list two-line subheader>
      <v-list-item v-for="item in items" :key="item.title" @click="() => {}">
        <v-list-item-avatar>
          <v-icon color="black" v-text="item.icon"></v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title v-text="item.title" />
          <v-list-item-subtitle v-text="item.subtitle" />
        </v-list-item-content>
        <v-list-item-icon>
          <v-icon :color="item.color">{{ item.status }}</v-icon>
        </v-list-item-icon>
      </v-list-item>
    </v-list>
    <v-overlay :value="isLoading">
      <v-progress-circular indeterminate size="64" />
    </v-overlay>
  </div>
</template>

<script>
import data, { getData } from '@/plugins/data';

// import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'Home',
  components: {
    // HelloWorld,
  },
  data: () => ({
    isLoading: true,
    items: [
      {
        icon: 'test',
        title: 'test',
        subtitle: 'test',
        color: 'black',
        status: 'test',
      },
    ],
  }),
  methods: {
    getData: async function() {
      await getData();
      this.items.push({
        icon: 'test',
        title: 'test1',
        subtitle: 'test',
        color: 'black',
        status: 'test',
      });
      console.log(data);
      this.isLoading = false;
    },
  },
  created: function() {
    this.getData();
  },
};
</script>
