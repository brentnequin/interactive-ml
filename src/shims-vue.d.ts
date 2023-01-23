/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'plotly.js-dist' {
  import Plotly from 'plotly.js-dist'
  export default Plotly
}