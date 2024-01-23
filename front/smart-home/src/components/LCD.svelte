<script lang="ts">
    export let display: { id:string; type: string; measurement: string; area: string; value: string|undefined; time: string|undefined; pi:number};;
</script>

<div class="card">
    <h1>LCD {display.id}</h1>
    <p>Area {display.area}</p>
    <p>{display.value}</p>
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