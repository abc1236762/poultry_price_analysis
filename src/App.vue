<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" clipped mobile-break-point="640" app>
      <v-list dense shaped>
        <template v-for="item in items">
          <v-list-item :key="item.text" :to="item.link" link>
            <v-list-item-icon v-text="item.icon" />
            <v-list-item-content>
              <v-list-item-title v-text="item.title" />
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar clipped-left app color="blue darken-3" dense dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>
        🐣家禽價格分析
      </v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-container
        fluid
        class="pa-0 overflow-y-auto"
        style="max-height: calc(100vh - 48px);"
      >
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { dataItems } from './plugins/data';

export default {
  name: 'App',
  data: () => ({
    drawer: null,
    items: [{ icon: '🏠', title: '首頁', link: '/' }, ...dataItems],
  }),
};
</script>
