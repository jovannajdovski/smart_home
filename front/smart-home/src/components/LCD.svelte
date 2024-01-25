<script lang="ts">
    export let display: { id:string; type: string; measurement: string; area: string; value: string|undefined; time: string|undefined; pi:number};;
</script>

<div class="card">
    <h1>LCD {display.id}</h1>
    <p>Area <b>{display.area}</b></p>
    <p>Time <b>{display.value}</b></p>
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