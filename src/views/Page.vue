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
      <v-list-item>
        <v-row align="center">
          <v-col />
          <v-col class="display-3" cols="auto" v-text="price" />
          <v-col>
            <v-row>
              <v-icon large :color="trend.color" v-text="trend.icon" />
            </v-row>
            <v-row v-text="dataUnit" />
          </v-col>
        </v-row>
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
      <line-chart
        class="pa-4"
        v-if="isLineChartLoaded"
        :chart-data="lineChartData"
        :options="{ legend: { display: false } }"
      />
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

import Vue from 'vue';
import { Line, mixins } from 'vue-chartjs';

const LineChart = Vue.component('line-chart', {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: {
    options: {
      type: Object,
      default: null,
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
});

export default {
  components: { LineChart },
  data: () => ({
    isDatePickerEnabled: false,
    isDataTableLoading: true,
    dataUnit: dataUnit,
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
    isLineChartLoaded: false,
    lineChartData: {},
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
    price() {
      return getValueString(this.data[0].value);
    },
    trend() {
      const trend = {};
      const diff = this.data[0].value - this.data[1].value;
      trend.icon = 'mdi-trending-neutral';
      if (diff > 0) {
        trend.color = 'red';
        trend.icon = 'mdi-trending-up';
      } else if (diff < 0) {
        trend.color = 'green';
        trend.icon = 'mdi-trending-down';
      }
      return trend;
    },
    dates() {
      return this.data.map((d) => d.date).sort();
    },
    dateRangeMin() {
      return this.dateOfIndex(this.dates.length - 1);
    },
    dateRangeMax() {
      return this.dateOfIndex(0);
    },
    dateRangeText() {
      return this.titleDateFormat(this.dateRange);
    },
  },
  methods: {
    dateOfIndex(index) {
      return this.dates[this.dates.length - 1 - index].split('/').join('-');
    },
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
      this.lineChartData = {
        labels: this.dataTableItems
          .map((d) =>
            d.date.replace(/20(\d{2})年(\d{2})月(\d{2})日/, '’$1/$2/$3')
          )
          .reverse(),
        datasets: [
          {
            label: '價格',
            borderColor: '#FFD600',
            borderWidth: 1,
            backgroundColor: '#FFEB3B',
            pointHoverRadius: 3,
            pointRadius: 2,
            fill: false,
            data: this.dataTableItems.map((d) => Number(d.value)).reverse(),
          },
        ],
      };
    },
  },
  created() {
    this.dateRange = [this.dateOfIndex(29), this.dateOfIndex(0)];
  },
  watch: {
    dateRange() {
      this.isDataTableLoading = true;
      this.isLineChartLoaded = false;
      this.setDataTableItems();
      this.isDataTableLoading = false;
      this.isLineChartLoaded = true;
    },
  },
};
</script>
