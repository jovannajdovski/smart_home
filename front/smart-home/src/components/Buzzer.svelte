<script lang="ts">
    export let buzzer: { id:string; type: string; measurement: string; area: string; value: string|undefined; time: string|undefined; pi:number};
</script>

<div class="card">
    <h1>{buzzer.type} {buzzer.id}</h1>
    <p>Area {buzzer.area}</p>
    <p>{buzzer.value} at {buzzer.time}</p>
    <!-- <p>{`${buzzer.active ? "ACTIVE" : "INACTIVE"}`}</p> -->
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