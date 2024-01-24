<script lang="ts">
    export let infrared: {
        id: string;
        type: string;
        name: string;
        area: string;
        active: boolean;
        color: string;
        pi: number;
    };

    const turn = () => {
        infrared.active = !infrared.active;
    };

    const changeColor = (color: string) => {
        infrared.color = color;
    };
</script>

<div class="card">
    <h1>{infrared.type} {infrared.id}</h1>
    <p>Area <b>{infrared.area}</b></p>
    <button
        class={`${
            infrared.active ? "bg-gray-400" : "bg-gray-600"
        } w-64 h-10 border-4 border-solid border-gray-500  rounded m-2`}
        on:click={turn}>TURN {`${infrared.active ? "OFF" : "ON"}`}</button
    >

    <div class="color-picker">
        <button
            class={`${
                infrared.active && infrared.color === "red"
                    ? "border-4 border-solid border-gray-500"
                    : null
            } w-20 h-10 bg-red-600 rounded m-2 cursor-pointer`}
            on:click={() => changeColor("red")}
        />
        <button
            class={`${
                infrared.active && infrared.color === "green"
                    ? "border-4 border-solid border-gray-500"
                    : null
            } w-20 h-10 bg-green-600 rounded m-2 cursor-pointer`}
            on:click={() => changeColor("green")}
        />
        <button
            class={`${
                infrared.active && infrared.color === "blue"
                    ? "border-4 border-solid border-gray-500"
                    : null
            } w-20 h-10 bg-blue-600 rounded m-2 cursor-pointer`}
            on:click={() => changeColor("blue")}
        />
    </div>
</div>

<style>
    .card {
        background-color: #d9d9d9;
        border-radius: 5px;
        padding: 10px;

        width: 300px;
        height: 200px;
        margin: 5px;
    }

    .color-picker {
        display: flex;
        flex-direction: row;
    }
    h1, p{
        padding: 5px;
    }
    b{
        font-size: 18px;
    }
</style>
