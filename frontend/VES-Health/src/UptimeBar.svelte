<script>
  let uptimePercent = "100.0";
  let dataPoints = [1,1,1,1,1,1,1,1,1,1,];
</script>
<style>
  .wrapper {
    height: calc(34px+4em);
    width: 28em;
    background-color: ivory;
    padding: 2px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    border: 1px solid gray;
    box-shadow: 0.2em 0.2em 0.2em gray;
    margin: 0.5em;
  }
</style>
<div data-component-id="jgnwrfzynh93" 
  data-component-status="operational" 
  data-js-hook="component-group-opener"
  class="wrapper">


<div class="shared-partial uptime-90-days-wrapper">
 <svg preserveAspectRatio="none" height="34" viewBox="0 0 448 34">
   {#each dataPoints as datapoint, i}
   <rect height="34" width="3" x="{450- 5 *i}" y="0" fill="#36b37e" class="uptime-day day-{i}" data-html="true"></rect>
   {/each}
</svg>
 <div class="legend legend-group">
  <span style="float: left"> {dataPoints.length} days ago</span>
  <span style="padding: 0 4em 0 4em; text-overflow: ellipsis; text-align: center">Uptime: {uptimePercent} %</span>
  <span style="float:right">Today</span>
</div>

</div>

</div>