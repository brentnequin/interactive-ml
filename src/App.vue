<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Plotly from 'plotly.js-dist'

const plot = ref<HTMLDivElement>()

onMounted(()=>{    
  Plotly.newPlot(plot.value, [{
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16],
    mode: 'markers',
    type: 'scatter'
  }], {
    margin: { t: 0 }
  });
})

function addPoint(event) {
  var { left, top } = plot.value.getBoundingClientRect();
  
	var xInDataCoord = plot.value._fullLayout.xaxis.p2c(event.x - plot.value._fullLayout.margin.l - left + document.documentElement.scrollLeft);
	var yInDataCoord = plot.value._fullLayout.yaxis.p2c(event.y - plot.value._fullLayout.margin.t - top + document.documentElement.scrollTop);

  plot.value.data[0].x.push(xInDataCoord)
  plot.value.data[0].y.push(yInDataCoord)

  Plotly.redraw(plot.value);
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