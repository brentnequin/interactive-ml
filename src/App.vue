<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Plotly from 'plotly.js-dist'

const plot = ref<HTMLDivElement>()

let points = [
  { x: 1, y: 1 },
  { x: 3, y: 3 },
  { x: 5, y: 5 },
  { x: 7, y: 7 },
]

onMounted(()=>{    
  refreshPlot()
})

function refreshPlot() {
  Plotly.newPlot(plot.value, [{
    x: points.map((({x}) => x)),
    y: points.map((({y}) => y)),
    mode: 'markers',
    type: 'scatter'
  }], {
    margin: { t: 0 },
    xaxis: { fixedrange: true },
    yaxis: { fixedrange: true }
  }, {
    displayModeBar: false
  });
}

function addPoint(event) {
  var { left, top } = plot.value.getBoundingClientRect();
  
	var xInDataCoord = plot.value._fullLayout.xaxis.p2c(event.x - plot.value._fullLayout.margin.l - left + document.documentElement.scrollLeft);
	var yInDataCoord = plot.value._fullLayout.yaxis.p2c(event.y - plot.value._fullLayout.margin.t - top + document.documentElement.scrollTop);

  // plot.value.data[0].x.push(xInDataCoord)
  // plot.value.data[0].y.push(yInDataCoord)

  points.push({ x: xInDataCoord, y: yInDataCoord })
  refreshPlot()
}

async function run() {
}
</script>

<template>
  <h1 class="text-4xl">Test</h1>
  <div class="flex flex-wrap">
    <div>
      <div ref="plot" v-on:click="addPoint" />
    </div>
    <div>
      <button v-on:click="run">KMeans</button>
    </div>
  </div>
</template>