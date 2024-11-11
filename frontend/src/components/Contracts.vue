<template>
    <div>
        <button class="btn btn-primary mb-3" @click="openModal()">Add Contract</button>
        <ul class="list-group mb-3">
            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="contract in dataList" :key="contract.id">
                <span>{{ contract.player_name }} - {{ contract.team_name }} ({{ contract.contract_start_date }} to {{ contract.contract_end_date }}, Salary: {{ contract.salary }})</span>
                <div>
                    <button class="btn btn-warning btn-sm me-2" @click="openModal(contract)">Edit</button>
                    <button class="btn btn-danger btn-sm" @click="deleteContract(contract.id)">Delete</button>
                </div>
            </li>
        </ul>

        <!-- Modal for Adding/Editing Contracts -->
        <div class="modal fade" id="contractModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">{{ isEditing ? 'Edit' : 'Add' }} Contract</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <label>Player</label>
                        <select v-model="formData.player_id" class="form-control mb-2">
                            <option v-for="player in players" :value="player.id" :key="player.id">{{ player.name }}</option>
                        </select>

                        <label>Team</label>
                        <select v-model="formData.team_id" class="form-control mb-2">
                            <option v-for="team in teams" :value="team.id" :key="team.id">{{ team.name }}</option>
                        </select>

                        <label>Contract Start Date</label>
                        <input v-model="formData.contract_start_date" type="date" class="form-control mb-2" />

                        <label>Contract End Date</label>
                        <input v-model="formData.contract_end_date" type="date" class="form-control mb-2" />

                        <label>Salary</label>
                        <input v-model="formData.salary" type="number" class="form-control mb-2" placeholder="Salary" />

                        <div class="form-check">
                            <input v-model="formData.active" class="form-check-input" type="checkbox" id="active">
                            <label class="form-check-label" for="active">Active</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="saveContract">{{ isEditing ? 'Save Changes' : 'Add Contract' }}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['dataList', 'players', 'teams'],
    data() {
        return {
            formData: {
                player_id: '',
                team_id: '',
                contract_start_date: '',
                contract_end_date: '',
                salary: '',
                active: true,
            },
            isEditing: false,
            editingContractId: null,
        }
    },
    methods: {
        openModal(contract = null) {
            this.isEditing = !!contract;
            this.editingContractId = contract ? contract.id : null;
            this.formData = contract
                ? {
                    player_id: contract.player_id,
                    team_id: contract.team_id,
                    contract_start_date: contract.contract_start_date,
                    contract_end_date: contract.contract_end_date,
                    salary: contract.salary,
                    active: contract.active,
                }
                : {
                    player_id: '',
                    team_id: '',
                    contract_start_date: '',
                    contract_end_date: '',
                    salary: '',
                    active: true,
                };
            new bootstrap.Modal(document.getElementById('contractModal')).show();
        },
        async saveContract() {
            const url = this.isEditing
                ? `http://localhost:8000/api/contract/${this.editingContractId}/`
                : 'http://localhost:8000/api/contract/';
            const method = this.isEditing ? 'PUT' : 'POST';

            await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.formData),
            });
            this.updateList();
            bootstrap.Modal.getInstance(document.getElementById('contractModal')).hide();
        },
        async deleteContract(id) {
            await fetch(`http://localhost:8000/api/contract/delete/${id}/`, { method: 'DELETE' });
            this.updateList();
        },
        async updateList() {
            const response = await fetch('http://localhost:8000/api/contracts/');
            const updatedList = await response.json();
            this.$emit('update-list', { model: 'contract', list: updatedList.contracts });
        },
    },
}
</script>
