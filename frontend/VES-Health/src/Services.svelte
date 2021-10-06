<script>
import { onDestroy, onMount } from "svelte";
import Spinner from "./Spinner.svelte";
import UptimeBar from "./UptimeBar.svelte";

let services = [];
let loaded = false;

async function fetchData() {
	// fetch services
	let _services = await (await fetch("/status")).json()
	_services.forEach(service => {
    let color="green";
    let count = 0;
    service.endpoints.forEach(url => {
      color = url.state === "ok" ? "green" : "red";
      count += url.state === "ok" ? 1 : 0;
    });
    service.color = color;
    service.count = count;     
	});
	console.log(_services);
	services = _services;
	loaded = true;
}


onMount(() => {
	const interval = setInterval(fetchData, 3000);
	fetchData();
});

onDestroy(() => {
	clearInterval(interval);
});
</script>

<style>
	.no_decoration {
	  list-style: none;
	}
	.centered {
		margin: 2em 10% 2em 10%;
	}
	.service {
		width: 90%;
		height: 11em;
		margin: 0 0 1em 0;
		border: 1px solid gray;
		box-shadow: 0.5em 0.5em 0.5em gray;
	}
  .state {
    float: right;
    height: 100%;
    width: 4em;
  }
</style>

<div class="centered">
{#if !loaded}
	<Spinner></Spinner>
{:else}
<ul>
	{#each services as s}
		<li class="no_decoration">
			<div class="service">
        <div class="state" style="background-color: {s.color}"></div>
        <h2>{s.id}</h2>
        <span>{s.count} of {s.endpoints.length} endpoints are <b>OK</b></span>
        <span>Service uptime is {s.uptime}</span>
        <div style="margin-left:25%"><UptimeBar></UptimeBar></div>
			</div>
		</li>
	{/each}
</ul>
{/if}
</div>