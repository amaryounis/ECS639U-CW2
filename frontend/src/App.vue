<template>
    <div class="container pt-3">
        <h1 class="text-center border rounded bg-light p-3 mb-4">Player Contracts System</h1>

        <!-- Bootstrap Tabs -->
        <ul class="nav nav-tabs" role="tablist">
            <li class="nav-item">
                <a class="nav-link active" data-bs-toggle="tab" href="#model-a-tab" role="tab">Players</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-bs-toggle="tab" href="#model-b-tab" role="tab">Teams</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-bs-toggle="tab" href="#relationship-tab" role="tab">Contracts</a>
            </li>
        </ul>

        <!-- Tab Content -->
        <div class="tab-content pt-3">
            <div class="tab-pane fade show active" id="model-a-tab" role="tabpanel">
                <Player @update-list="handleUpdate" :data-list="playerList" />
            </div>
            <div class="tab-pane fade" id="model-b-tab" role="tabpanel">
                <Team @update-list="handleUpdate" :data-list="teamList" />
            </div>
            <div class="tab-pane fade" id="relationship-tab" role="tabpanel">
                <Contracts @update-list="handleUpdate" :data-list="contractList" :players="playerList" :teams="teamList" />
            </div>
        </div>
    </div>
</template>

<script>
import Player from './components/Player.vue';
import Team from './components/Team.vue';
import Contracts from './components/Contracts.vue';

export default {
    components: {
        Player,
        Team,
        Contracts,
    },
    data() {
        return {
            playerList: [],
            teamList: [],
            contractList: [],
        };
    },
    mounted() {
        this.fetchData('players', 'playerList');
        this.fetchData('teams', 'teamList');
        this.fetchData('contracts', 'contractList');
    },
    methods: {
        async fetchData(endpoint, listName) {
            try {
                const response = await fetch(`http://localhost:8000/api/${endpoint}/`);
                if (!response.ok) {
                    console.error(`Error fetching ${endpoint}:`, await response.text());
                    throw new Error(`Failed to fetch ${endpoint}`);
                }
                const data = await response.json();
                this[listName] = data[endpoint];
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        },
        handleUpdate({ model, list }) {
            this[`${model}List`] = list;
        },
    },
};
</script>
