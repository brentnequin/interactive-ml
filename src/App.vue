<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Plotly from 'plotly.js-dist'
import axios from "axios";

const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  headers: { 'x-api-key': process.env.VUE_APP_API_KEY }
})

const plot = ref<HTMLDivElement>()

const xmax = 10, xmin = 0
const ymax = 10, ymin = 0

let points = [
  { x: 1, y: 1 },
  { x: 3, y: 3 },
  { x: 7, y: 7 },
  { x: 9, y: 9 },
]

const plot_layout = {
  margin: { t: 20, l: 20, r: 20, b: 20 },
  xaxis: {
    fixedrange: true,
    range: [xmin, xmax],
    showticklabels: false,
    zeroline: false
  },
  yaxis: { 
    fixedrange: true,
    range: [ymin, ymax],
    showticklabels: false,
    zeroline: false
  }
}

const plot_config = {
  displayModeBar: false
}

onMounted(()=>{    
  refreshPlot()
})

function refreshPlot() {
  Plotly.newPlot(plot.value, [{
    x: points.map((({x}) => x)),
    y: points.map((({y}) => y)),
    mode: 'markers',
    type: 'scatter'
  }], plot_layout, plot_config);
}

function addPoint(event: MouseEvent) {

  if (!plot) return
  
  var { left, top } = plot.value.getBoundingClientRect();
  
	var xInDataCoord = plot.value._fullLayout.xaxis.p2c(event.x - plot.value._fullLayout.margin.l - left + document.documentElement.scrollLeft);
	var yInDataCoord = plot.value._fullLayout.yaxis.p2c(event.y - plot.value._fullLayout.margin.t - top + document.documentElement.scrollTop);

  if (xInDataCoord > xmax || xInDataCoord < xmin) return
  if (yInDataCoord > ymax || yInDataCoord < ymin) return

  points.push({ x: xInDataCoord, y: yInDataCoord })
  refreshPlot()
}

async function run() {
  try {
    const response = await api.post('execute/kmeans', {'points': points, 'k': 2})
    console.log(response.data)
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <div class="bg-slate-800 text-gray-50 h-screen flex flex-col justify-between">
    <div class="p-8 text-center">
      <h1 class="text-4xl">Interactive ML</h1>
    </div>
    <div class="flex flex-col items-center md:flex-row space-y-4 justify-center md:space-x-4 md:space-y-0">
      <div class="rounded-lg h-96 w-96">
        <div ref="plot" v-on:click="addPoint" class=" h-full w-full" />
      </div>
      <div class="h-96 w-96 bg-slate-700">
        <div class="p-8 ">
          <h2 class="text-2xl mb-4">Run Algorithm</h2>
          <h3 class="text-xl">Clustering</h3>
          <button v-on:click="run" class=""><i>k</i>-means</button>
        </div>
      </div>
    </div>
    <div class="p-8 text-center">
      <small>© 2022 Brent Nequin. All Rights Reserved.</small>
    </div>
  </div>
</template>