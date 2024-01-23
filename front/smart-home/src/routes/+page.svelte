<script lang="ts">
    import axios from "axios";
    import { onMount } from "svelte";
    import Buzzer from "../components/Buzzer.svelte";
    import DoorSensor from "../components/DoorSensor.svelte";
    import FSD from "../components/FSD.svelte";
    import DoorLight from "../components/DoorLight.svelte";
    import UltrasonicSensor from "../components/UltrasonicSensor.svelte";
    import Dht from "../components/DHT.svelte";
    import Gyro from "../components/Gyro.svelte";
    import Infrared from "../components/Infrared.svelte";
    import LCD from "../components/LCD.svelte";
    import MembraneSwitch from "../components/MembraneSwitch.svelte";
    import MotionSensor from "../components/MotionSensor.svelte";
    import Rgb from "../components/RGB.svelte";

    // :TODO load pis object
    import pis from "../data.json";

    // let pis: {
    //     id: number;
    //     alt_description: string;
    // }[] = [];

    let selectedPiIdx = 1;
    let selectedPi: any;

    // const fetchData = async () => {
    //     const response = await axios.get(
    //         `http://api.unsplash.com/search/photos?page=1&query=${
    //             term || "office"
    //         }&client_id=PQyLgjK4KgjRI9GVsFTK0HGB-uFZQC_eEsghofjcr1E`,
    //     );
    //     photos = response.data.results;
    // };

    onMount(() => {
        //fetchData();
        // pis = [{id:1, alt_description:"PI1"},
        // {id:2, alt_description:"PI2"},
        // {id:3, alt_description:"PI3"}]
    });

    $: selectedPi = pis.find((pi) => pi.id === selectedPiIdx);

    const toPi = (idx: number) => {
        selectedPiIdx = idx;
    };

    let alarm = "INACTIVE";

    const turnAlarm = () => {
        if (alarm === "INACTIVE") {
            alarm = "ACTIVE";
        } else if (alarm === "ACTIVE") {
            alarm = "PANIC";
        } else if (alarm === "PANIC") {
            alarm = "INACTIVE";
        }
    };
</script>

<div class="container">
    <div class="header">
        <div class="nav">
            <h1>SMART HOME</h1>
            <div class="button-container">
                {#each pis as pi, i (pi.id)}
                    <button
                        class={`button ${
                            pi.id === selectedPiIdx ? "btn-act" : "btn-inact"
                        }`}
                        on:click={() => toPi(pi.id)}>PI {pi.id}</button
                    >
                {/each}
            </div>
        </div>
        <button
            class={`alarm ${alarm === "PANIC" ? "blink" : null} ${
                alarm === "ACTIVE" ? "alarm-ac" : null
            } ${alarm === "INACTIVE" ? "alarm-in" : null}`}
            on:click={() => turnAlarm()}>ALARM {alarm}</button
        >
    </div>

    <div class="pi-container">
        <div class="pi-components">
            {#each selectedPi.components as component}
                {#if component.type === "Buzzer"}
                    <Buzzer buzzer={component} />
                {:else if component.type === "DHT"}
                    <Dht sensor={component} />
                {:else if component.type === "Door light"}
                    <DoorLight light={component} />
                {:else if component.type === "Door sensor"}
                    <DoorSensor sensor={component} />
                {:else if component.type === "4SD"}
                    <FSD display={component} />
                {:else if component.type === "Gyro"}
                    <Gyro sensor={component} />
                {:else if component.type === "Infrared"}
                    <Infrared infrared={component} />
                {:else if component.type === "LCD"}
                    <LCD display={component} />
                {:else if component.type === "Membrane switch"}
                    <MembraneSwitch keypad={component} />
                {:else if component.type === "Motion sensor"}
                    <MotionSensor sensor={component} />
                {:else if component.type === "RGB"}
                    <Rgb rgb={component} />
                {:else if component.type === "Ultrasonic sensor"}
                    <UltrasonicSensor sensor={component} />
                {:else}
                    <div class="bg-gray-200 w-10 h-10 rounded-full m-3" />
                {/if}
            {/each}
        </div>
        <div class="grafana-container">GRAFANA</div>
    </div>
</div>

<style>
    .image {
        width: 400px;
        height: 250px;
        margin: 5px;
    }
    .photos {
        display: flex;
        flex-wrap: wrap;
    }
    .container {
        width: 100%;
        height: 100%;
        margin: 0 auto;
        /* background-color: #484545; */
    }

    .pi-container {
        background-color: #797881;
        border-radius: 10px;
        width: auto;
        height: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .pi-components {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
        gap: 20px;
        width: 90%;
        margin-top: 30px;
    }

    .header {
        text-align: center;
        font-size: 20px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        margin: 20px;
    }

    .header h1 {
        color: white;
        margin-right: 20px;
        font-size: 30px;
    }

    .nav {
        display: flex;
        flex-direction: row;
    }

    .button {
        font-size: 20px;
        height: 40px;
        min-width: 200px;

        border: 2px solid black;
        color: white;
    }

    .btn-act {
        background-color: #dbdbdd;
    }

    .btn-inact {
        background-color: #797881;
    }

    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .alarm {
        font-size: 20px;
        height: 70px;
        min-width: 300px;
        background-color: #d9d9d9;
        border-radius: 10px;
        align-self: flex-end;
    }

    @keyframes blink {
        0% {
            opacity: 1;
        }
        50% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }

    .blink {
        animation: blink 1s infinite;
        background-color: red;
    }

    .alarm-ac {
        border: 5px solid rgb(82, 255, 47);
    }

    .alarm-in {
        border: 5px solid rgb(29, 29, 29);
    }

    .grafana-container {
        background-color: #d9d9d9;
        border-radius: 5px;

        min-height: 200px;
        width: 90%;
        margin: 50px;

        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
