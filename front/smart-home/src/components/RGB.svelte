<script lang="ts">
    export let rgb: { id:string; type: string; measurement: string; area: string; value: string|undefined; time: string|undefined; pi:number};

</script>

<div class="card">
    <h1>{rgb.type} {rgb.id}</h1>
    <p>Area {rgb.area}</p>

    <div class="color-picker">
        <div
            class={`${
                rgb.value === "off"
                    ? "bg-gray-600"
                    : null
            } 
            ${
                rgb.value === "red"
                    ? "bg-red-600"
                    : null
            }
            ${
                rgb.value === "green"
                    ? "bg-green-600"
                    : null
            }
            ${
                rgb.value === "blue"
                    ? "bg-blue-600"
                    : null
            }
            w-10 h-10 rounded m-3`}
        />
    </div>
</div>

<style>
    .card {
        background-color: #d9d9d9;
        border-radius: 5px;
        padding: 10px;

        width: 200px;
        height: 130px;
        margin: 5px;
    }

    .color-picker {
        display: flex;
        flex-direction: row;
    }
</style>
