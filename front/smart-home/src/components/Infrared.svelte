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

    export let color: string;
    console.log(color)

    const sendRgbCommand = async (command:string, id:string, tmp: any) => {
        try {
        const response = await fetch('http://localhost:5000/send_rgb_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'command':command,'id':id, 'tmp':tmp}),
        });
        if (response.ok) {
            console.log('send pin ok')
        } else {
            console.error('Failed to fetch data:', response.statusText);
        }
        } catch (error) {
        console.error('Error:', error);
        }
    };

    const turn = () => {
        if (color === "off"){
            color = "red"
        } 
        else {
            color = "off";
        }

        sendRgbCommand("OK",infrared.id, new Date());
    };

    const changeColor = (newColor: string) => {
        color = newColor;
        if (color === "red") sendRgbCommand("1",infrared.id, new Date());
        if (color === "green") sendRgbCommand("2",infrared.id, new Date());
        if (color === "blue") sendRgbCommand("3",infrared.id, new Date());
    };
</script>

<div class="card">
    <h1>{infrared.type} {infrared.id}</h1>
    <p>Area <b>{infrared.area}</b></p>
    <button
        class={`${
            color !== "off" ? "bg-gray-400" : "bg-gray-600"
        } w-64 h-10 border-4 border-solid border-gray-500  rounded m-2`}
        on:click={turn}>TURN {`${color !== "off" ? "OFF" : "ON"}`}</button
    >

    <div class="color-picker">
        <button
            class={`${
                color === "red"
                    ? "border-4 border-solid border-gray-500"
                    : null
            } w-20 h-10 bg-red-600 rounded m-2 cursor-pointer`}
            on:click={() => changeColor("red")}
        />
        <button
            class={`${
                color === "green"
                    ? "border-4 border-solid border-gray-500"
                    : null
            } w-20 h-10 bg-green-600 rounded m-2 cursor-pointer`}
            on:click={() => changeColor("green")}
        />
        <button
            class={`${
                color === "blue"
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
