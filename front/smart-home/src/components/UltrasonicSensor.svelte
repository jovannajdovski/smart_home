<script lang="ts">
    export let sensor: { id:string; type: string; measurement: string; area: string; value: number|undefined; time: string|undefined; pi:number};
</script>

<div class="card">
    <h1>{sensor.type} {sensor.id}</h1>
    <p>Area <b>{sensor.area}</b></p>
    <p>Last detected distance <b>{sensor.value} m</b></p>
</div>
    
<style>
    .card{
        background-color: #D9D9D9;
        border-radius: 5px;
        padding: 10px;

        width: 300px;
        height: 150px;
        margin: 5px;
    }
    h1, p{
        padding: 5px;
    }
    b{
        font-size: 18px;
    }
</style>
