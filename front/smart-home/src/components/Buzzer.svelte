<script lang="ts">
    export let buzzer: { id:string; type: string; measurement: string; area: string; value: string|undefined; time: string|undefined; pi:number};
</script>

<div class="card">
    <h1>{buzzer.type} {buzzer.id}</h1>
    <p>Area <b>{buzzer.area}</b></p>
    <p><b>{buzzer.value}</b> at <b>{buzzer.time}</b></p>
    <!-- <p>{`${buzzer.active ? "ACTIVE" : "INACTIVE"}`}</p> -->
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