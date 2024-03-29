<script lang="ts">
    import axios from "axios";
    import { beforeUpdate, onMount } from "svelte";
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

    let pis = [1, 2, 3];
    let selectedPiIdx = 1;

    let data = [{}];

    const fetchData = async () => {
        try {
            const response = await fetch("http://localhost:5000/get_all");
            if (response.ok) {
                data = await response.json();
            } else {
                console.error("Failed to fetch data:", response.statusText);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    };

    let intervalId: number | undefined;

    onMount(() => {
        fetchData();
        intervalId = setInterval(fetchData, 20000);
        return () => clearInterval(intervalId);
    });

    // $: selectedPi = pis.find((pi) => pi.id === selectedPiIdx);

    const toPi = (idx: number) => {
        selectedPiIdx = idx;
    };

    let rgbComp;
    let alarm = "INACTIVE";
    $: {
        alarm = data[0].value?.toUpperCase() ?? "INACTIVE";
        rgbComp = data.find((element) => element.type === "RGB-LIGHT");
    }

    const turnAlarm = () => {
        // if (alarm === "INACTIVE") {
        //     alarm = "ACTIVE";
        // } else if (alarm === "ACTIVE") {
        //     alarm = "PANIC";
        // } else if (alarm === "PANIC") {
        //     alarm = "INACTIVE";
        // }
    };

    let selectedTime = "";
    const turnOff = () => {
        sendClockCommand("off","")
    };

    const sendClockTime = () => {
        if (selectedTime){
            sendClockCommand("set", selectedTime)
        }
    };

    const sendClockCommand = async (command:string, time:string) => {
        try {
        const response = await fetch('http://localhost:5000/send_clock_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'command':command,'time':time}),
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

    let dashboardUrl1 =
        "http://localhost:3001/d/bca1b468-31d6-441e-a3fb-6b025d29087d/pi-1?orgId=1&refresh=5s&from=1706113885578&to=1706117485578&kiosk=tv";
    let dashboardUrl2 =
        "http://localhost:3001/d/bc7cd3da-bcfc-47ec-9df5-2d78496e28d0/pi-2?orgId=1&from=1706108988730&to=1706119788730&refresh=auto&kiosk=tv";
    let dashboardUrl3 =
        "http://localhost:3001/d/aa2d4838-c1b1-4e4f-9178-6fc8375972fc/pi-3?orgId=1&from=1706117285180&to=1706120885180&kiosk=tv";
</script>

<div class="container">
    <div class="header">
        <div class="nav">
            <h1>SMART HOME</h1>
            <div class="button-container">
                {#each pis as piId}
                    <button
                        class={`button ${
                            piId === selectedPiIdx ? "btn-act" : "btn-inact"
                        }`}
                        on:click={() => toPi(piId)}>PI {piId}</button
                    >
                {/each}
            </div>
        </div>

        <div class="clock-alarm">
            <p>CLOCK ALARM</p>
            <div class="pick">
                <input
                type="time"
                id="timePicker"
                bind:value={selectedTime}
            />
            <button class="bg-green-500 hover:bg-green-700 text-white font-bold w-12 m-1 rounded" on:click={() => sendClockTime()}>SET</button>
            </div>
            
            <button class="bg-gray-500 hover:bg-gray-700 text-white font-bold w-52 m-1 rounded" on:click={() => turnOff()}>TURN OFF</button>
        </div>

        <button
            class={`alarm ${alarm === "PANIC" ? "blink" : null} ${
                alarm === "ACTIVE" ? "alarm-ac" : null
            } ${alarm === "INACTIVE" ? "alarm-in" : null}`}
            on:click={() => turnAlarm()}>ALARM {alarm}</button
        >
    </div>

    <div class="pi-container">
        {#if data.find((element) => element.type === "MS" && element.pi === selectedPiIdx)}
            <div style="width: 90%;">
                <div style="float:left; width: 75%; margin: 50px 0px 0px 0px">
                    <div class="pi-components-split">
                        {#each data as component}
                            {#if component.pi === selectedPiIdx}
                                {#if component.type === "BUZZER"}
                                    <Buzzer buzzer={component} />
                                {:else if component.type === "DHT"}
                                    <Dht sensor={component} />
                                {:else if component.type === "LIGHT"}
                                    <DoorLight light={component} />
                                {:else if component.type === "BUTTON"}
                                    <DoorSensor sensor={component} />
                                {:else if component.type === "4DD"}
                                    <FSD display={component} />
                                {:else if component.type === "GYRO"}
                                    <Gyro sensor={component} />
                                {:else if component.type === "IR-RECEIVER"}
                                    <Infrared
                                        infrared={component}
                                        color={rgbComp.value}
                                    />
                                {:else if component.type === "LCD"}
                                    <LCD display={component} />
                                {:else if component.type === "PIR"}
                                    <MotionSensor sensor={component} />
                                {:else if component.type === "RGB-LIGHT"}
                                    <Rgb rgb={component} />
                                {:else if component.type === "US"}
                                    <UltrasonicSensor sensor={component} />
                                {/if}
                            {/if}
                        {/each}
                    </div>
                </div>
                <div
                    style="float:right; width: 20%; justify-content: center; margin: 50px 50px 0px 0px"
                >
                    <div class="pi-components-split">
                        {#each data as component}
                            {#if component.pi === selectedPiIdx}
                                {#if component.type === "MS"}
                                    <MembraneSwitch keypad={component} />
                                {/if}
                            {/if}
                        {/each}
                    </div>
                </div>
            </div>
        {:else}
            <div class="pi-components">
                {#each data as component}
                    {#if component.pi === selectedPiIdx}
                        {#if component.type === "BUZZER"}
                            <Buzzer buzzer={component} />
                        {:else if component.type === "DHT"}
                            <Dht sensor={component} />
                        {:else if component.type === "LIGHT"}
                            <DoorLight light={component} />
                        {:else if component.type === "BUTTON"}
                            <DoorSensor sensor={component} />
                        {:else if component.type === "4DD"}
                            <FSD display={component} />
                        {:else if component.type === "GYRO"}
                            <Gyro sensor={component} />
                        {:else if component.type === "IR-RECEIVER"}
                            <Infrared
                                infrared={component}
                                color={rgbComp.value}
                            />
                        {:else if component.type === "LCD"}
                            <LCD display={component} />
                        {:else if component.type === "MS"}
                            <MembraneSwitch keypad={component} />
                        {:else if component.type === "PIR"}
                            <MotionSensor sensor={component} />
                        {:else if component.type === "RGB-LIGHT"}
                            <Rgb rgb={component} />
                        {:else if component.type === "US"}
                            <UltrasonicSensor sensor={component} />
                        {:else}
                            <div
                                class="bg-gray-200 w-10 h-10 rounded-full m-3"
                            />
                        {/if}
                    {/if}
                {/each}
            </div>
        {/if}
        <div class="grafana-container">
            {#if selectedPiIdx === 1}
                <iframe
                    title="dash1"
                    class="dashboard"
                    src={dashboardUrl1}
                    frameborder="0"
                ></iframe>
            {:else if selectedPiIdx === 2}
                <iframe
                    title="dash2"
                    class="dashboard2"
                    src={dashboardUrl2}
                    frameborder="0"
                ></iframe>
            {:else}
                <iframe
                    title="dash3"
                    class="dashboard"
                    src={dashboardUrl3}
                    frameborder="0"
                ></iframe>
            {/if}
        </div>
    </div>
</div>

<style>

    #timePicker{
        height: auto;
    }

    .pick{
        display: flex;
        flex-direction: row;
        justify-content: space-around;
    }

    .clock-alarm {
        font-size: 20px;
        height:120px;
        min-width: 300px;
        background-color: #d9d9d9;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        /* align-self: flex-end;  */
    }

    .dashboard {
        margin: 30px;
        width: 100%;
        height: 1700px;
    }

    .dashboard2 {
        margin: 30px;
        width: 100%;
        height: 1900px;
    }

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
    .pi-components-split {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
        gap: 20px;
        width: 100%;
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
