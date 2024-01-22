<script lang="ts">
    export let sensor: { id:number; type: string; name: string; area: string; temperature: number; humidity: number;};
</script>

<div class="card">
    <h1>{sensor.type} {sensor.name}</h1>
    <p>Area {sensor.area}</p>
    <p>Temperature {sensor.temperature}</p>
    <p>Humidity {sensor.humidity}</p>
</div>
    
<style>
    .card{
        background-color: #D9D9D9;
        border-radius: 5px;
        padding: 10px;

        width: 200px;
        height: 100px;
        margin: 5px;
    }
</style>
