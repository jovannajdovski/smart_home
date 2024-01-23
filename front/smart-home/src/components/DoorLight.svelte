<script lang="ts">
    export let light: { id:number; type: string; name: string; area: string; active: boolean;};
</script>

<div class="card">
    <h1>{light.type} {light.name}</h1>
    <p>Area {light.area}</p>
    <p>{`${light.active ? "ON" : "OFF"}`}</p>
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