<script lang="ts">
    export let sensor: { id:string; type: string; measurement: string; area: string; value: (number|undefined)[][]; time: string|undefined; pi:number};;
</script>

<div class="card">
    <h1>{sensor.type} {sensor.id}</h1>
    <p>Area {sensor.area}</p>
    <p>Rotation {sensor.value[1]}</p>
    <p>Acceleration {sensor.value[0]}</p>
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
