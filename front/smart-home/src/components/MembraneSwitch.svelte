<script lang="ts">
    export let keypad: {
        id: number;
        type: string;
        name: string;
        area: string;
        code: string;
    };

    const numbers = [
        "1",
        "2",
        "3",
        "A",
        "4",
        "5",
        "6",
        "B",
        "7",
        "8",
        "9",
        "C",
        "*",
        "0",
        "#",
        "D",
    ];

    let display = "";
    let isDisplayingResults = false;
    let message = "";

    const handleClear = () => {
        display = "";
        isDisplayingResults = false;
        message = "";
    };

    const handleNumberClick = (number: string) => {
        if (isDisplayingResults || display.length === 12) {
            handleClear();
        }

        display = `${display}${number}`;
    };

    const ok = () => {
        if (!display) return;
        // :TODO send func
        message = keypad.code === display ? "CORRECT" : "INCORRECT";
        isDisplayingResults = true;
    };
</script>

<div class="card">
    <h1>{keypad.type} {keypad.name}</h1>
    <p>Area {keypad.area}</p>

    <div class="input-container">
        <div class="results">
            {display}
        </div>
        <button class="button" on:click={ok}>OK</button>
        <button class="btn-cancel" on:click={handleClear}> X </button>
    </div>

    <div class="dms">
        <div class="digits">
            <div class="numbers">
                {#each numbers as number (number)}
                    <button
                        class={`btn ${
                            "ABCD*#".includes(number) ? "btn-red" : "btn-blue"
                        }`}
                        on:click={() => handleNumberClick(number)}
                    >
                        {number}
                    </button>
                {/each}
            </div>
        </div>
    </div>

    <div class={`message ${message === "CORRECT" ? "correct" : "incorrect"}`}>{message}</div>
</div>

<style>
    .card {
        background-color: #d9d9d9;
        border-radius: 5px;
        padding: 10px;

        width: 300px;
        height: 450px;
        margin: 5px;
    }

    .input-container {
        margin-bottom: 20px;
        display: flex;
        flex-direction: row;
    }

    .results {
        padding: 5px;
        width: 180px;
        height: 40px;
        border-radius: 10px;
        outline: none;
        border: 1px solid gray;
        font-size: 20px;
        background-color: white;
        color: black;
        font-size: 20px;
        display: flex;
        flex-direction: row-reverse;
        margin-right: 5px;
    }

    .button {
        padding: 5px;
        font-size: 20px;
        background-color: rgb(0, 255, 64);
        border-radius: 10px;
        border: none;
        color: white;
        margin-right: 3px;
    }

    .btn-cancel {
        padding: 5px;
        width: 40px;
        font-size: 20px;
        background-color: rgb(151, 151, 151);
        border-radius: 10px;
        border: none;
        color: white;
    }

    .dms {
        background-color: rgb(28, 28, 28);
        width: 270px;
        padding: 15px;
        border-radius: 7px;
    }
    .digits {
        display: flex;
    }
    .numbers {
        display: flex;
        flex-wrap: wrap;
        width: 250px;
    }
    .btn {
        width: 50px;
        height: 50px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        color: white;
        margin: 5px;
        border: 2px solid white;
    }
    .btn-lg {
        width: 110px;
    }
    .btn-xlg {
        width: 170px;
        background-color: rgb(114, 113, 113);
    }

    .btn-red {
        background-color: rgb(255, 0, 0);
    }
    .btn-blue {
        background-color: rgb(4, 0, 255);
    }

    .message{
        margin-top: 10px;
        font-size: 24px;
        text-align: center;
    }

    .correct{
        color: rgb(0, 187, 0);
    }

    .incorrect{
        color: rgb(216, 4, 0);
    }
</style>
