<script lang="ts">
    export let sensor: { id:string; type: string; measurement: string; area: string; value: string|undefined; time: string|undefined; pi:number};
</script>

<div class="card">
    <h1>{sensor.type} {sensor.id}</h1>
    <p>Area {sensor.area}</p>
    <p>Last detected {sensor.time}</p>
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
