<script>
import { onDestroy, onMount } from "svelte";

let services = [
    {"id": "HRM", "color":"", "urls":[{"url": "/ping", "state":"ok"}]},
    {"id": "ECONOMY", "color":"", "urls":[{"url": "/ping", "state":"ok"}]},
    {"id": "PROCUREMENT", "color":"", "urls":[{"url": "/ping", "state":"ok"}]},
    {"id": "COMMON", "color":"", "urls":[{"url": "/ping", "state":"nok"}]},     
];

async function fetchData() {
    // fetch services
    let _services = await (await fetch("/status")).json()
    _services.forEach(service => {
        let color="green";
        service.urls.forEach(url => {
            color = url.state === "ok" ? "green" : "red";
        });
        service.color = color;     
    });
    console.log(_services);
    services = _services;
}


onMount(() => {
    const interval = setInterval(fetchData, 3000);
    fetchData();
});

onDestroy(
    () => {
        clearInterval(interval);
    }
);
</script>

<style>
    .centered {
        margin: 2em 10% 2em 10%;
    }
    .service {
        width: 90%;
        height: 5em;
        margin: 0 0 1em 0;
        border: 1px solid gray;
        box-shadow: 0.5em 0.5em 0.5em gray;
        list-style: none;
    }
</style>

<div class="centered">
    <ul>
        {#each services as s}
            <li class="service" style="background-color: {s.color}">
                <h2>{s.id}</h2>
            </li>
        {/each}
    </ul>
</div>