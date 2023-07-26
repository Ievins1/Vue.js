<script>
import axios from 'axios';

export default {
  data() {
    return {
      sensorsData: [],
      metricsData: [],
      sensorTypesData: [],
      searchQuery: '',
      selectedSensorType: '',
      sortBy: '',
      sortDesc: false,
      visibleUnits: [],
      tableFields: [
        'name',
        // Add other fields based on the metrics.json data structure
        // For example: 'metric_1'
      ]
    };
  },
  created() {
    this.loadData();
  },
  computed: {
    filteredSensorData() {
      let filteredData = this.sensorsData;
      if (this.searchQuery) {
        filteredData = filteredData.filter(sensor => sensor.name.toLowerCase().includes(this.searchQuery.toLowerCase()));
      }
      if (this.selectedSensorType) {
        filteredData = filteredData.filter(sensor => sensor.type.toString() === this.selectedSensorType);
      }
      return filteredData;
    },
    sensorTypesOptions() {
      return Object.keys(this.sensorTypesData).map(key => ({ value: key, text: this.sensorTypesData[key].name }));
    }
  },
  methods: {
    async loadData() {
      const [sensorsResponse, metricsResponse, sensorTypesResponse] = await Promise.all([
        axios.get('/api/sensors'), // Adjust the API endpoint based on your Python API implementation
        axios.get('/api/metrics'),
        axios.get('/api/sensorTypes')
      ]);
      this.sensorsData = sensorsResponse.data;
      this.metricsData = metricsResponse.data;
      this.sensorTypesData = sensorTypesResponse.data;
      this.generateVisibleUnits();
    },
    generateVisibleUnits() {
      // Extracting units data from metricsData and creating the visibleUnits array
      // based on the selected option in metrics.json
      const selectedMetric = this.metricsData.data.items.find(metric => metric.id === '1');
      if (selectedMetric) {
        this.visibleUnits = selectedMetric.units;
      }
    },
    sortByColumn(field) {
      if (this.sortBy === field) {
        this.sortDesc = !this.sortDesc;
      } else {
        this.sortBy = field;
        this.sortDesc = false;
      }
    },
    getMetricValue(sensor, unitId) {
      return sensor.metrics[unitId].v;
    }
  }
};
</script>

<template>
  <div>
    <b-container>
      <b-row>
        <b-col>
          <b-form-input v-model="searchQuery" placeholder="Search by sensor name"></b-form-input>
        </b-col>
        <b-col>
          <b-form-select v-model="selectedSensorType" :options="sensorTypesOptions" placeholder="Filter by sensor type"></b-form-select>
        </b-col>
      </b-row>

      <b-table striped hover :items="filteredSensorData" :fields="tableFields" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc">
        <template v-for="unit in visibleUnits" v-slot:[`cell(metric_${unit.id})`]="{ item }">
          {{ getMetricValue(item, unit.id) }} {{ unit.name }}
        </template>
      </b-table>
    </b-container>
  </div>
</template>