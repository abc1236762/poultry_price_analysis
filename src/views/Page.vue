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
      <v-card-title>歷史資料</v-card-title>
      <v-list-item>
        <v-dialog
          ref="datePickerDialog"
          v-model="isDatePickerEnabled"
          :return-value.sync="dateRange"
          persistent
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="dateRangeText"
              label="選擇日期範圍"
              prepend-icon="mdi-calendar-range"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="dateRange"
            scrollable
            range
            show-current="false"
            :min="dateRangeMin"
            :max="dateRangeMax"
            :allowed-dates="allowedDates"
            :title-date-format="titleDateFormat"
            :selected-items-text="dateRangeText"
            :day-format="dayFormat"
          >
            <v-spacer />
            <v-btn text color="primary" @click="isDatePickerEnabled = false">
              取消
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="$refs.datePickerDialog.save(dateRange)"
            >
              確定
            </v-btn>
          </v-date-picker>
        </v-dialog>
      </v-list-item>
      <v-data-table
        :headers="dataTableHeaders"
        :items="dataTableItems"
        :loading="isDataTableLoading"
        dense
        mobile-breakpoint=""
      />
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
import { getValueString } from '@/utils';
import data, { dataItems, dataUnit } from '@/plugins/data';

export default {
  data: () => ({
    isDatePickerEnabled: false,
    isDataTableLoading: true,
    dateRange: [],
    dataTableHeaders: [
      {
        text: '日期',
        value: 'date',
        align: 'center',
        sortable: false,
      },
      { text: `價格（${dataUnit}）`, value: 'value', align: 'end' },
    ],
    dataTableItems: [],
  }),
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
    dates() {
      return this.data.map((d) => d.date).sort();
    },
    dateRangeMin() {
      return this.dates[0].split('/').join('-');
    },
    dateRangeMax() {
      return this.dates[this.dates.length - 1].split('/').join('-');
    },
    dateRangeText() {
      return this.titleDateFormat(this.dateRange);
    },
  },
  methods: {
    allowedDates(date) {
      return this.dates.includes(date.split('-').join('/'));
    },
    dayFormat(date) {
      return date.split('-')[2].toString();
    },
    titleDateFormat(date) {
      return date
        .map((dt) => dt.replace(/(\d{4})-(\d{2})-(\d{2})/, '$1年$2月$3日'))
        .sort()
        .join('～');
    },
    setDataTableItems() {
      let begin = this.dates.indexOf(this.dateRange[0].split('-').join('/'));
      let end = this.dates.indexOf(
        this.dateRange[this.dateRange.length - 1].split('-').join('/')
      );
      if (begin > end) [begin, end] = [end, begin];
      const dates = this.dates.slice(begin, end + 1);
      this.dataTableItems = this.data
        .filter((d) => dates.includes(d.date.split('-').join('/')))
        .map((d) => ({
          date: d.date.replace(/(\d{4})\/(\d{2})\/(\d{2})/, '$1年$2月$3日'),
          value: getValueString(d.value),
        }));
    },
  },
  created() {
    this.dateRange = [this.dateRangeMin, this.dateRangeMax];
  },
  watch: {
    dateRange() {
      this.isDataTableLoading = true;
      this.setDataTableItems();
      this.isDataTableLoading = false;
    },
  },
};
</script>
