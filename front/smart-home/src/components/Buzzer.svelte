<script lang="ts">
    export let buzzer: { id:number; type: string; name: string; area: string; active: boolean;};
</script>

<div class="card">
    <h1>{buzzer.type} {buzzer.name}</h1>
    <p>Area {buzzer.area}</p>
    <p>{`${buzzer.active ? "ACTIVE" : "INACTIVE"}`}</p>
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