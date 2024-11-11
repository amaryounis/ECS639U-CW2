<template>
    <div>
        <button class="btn btn-primary mb-3" @click="openModal()">Add Player</button>
        <ul class="list-group mb-3">
            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="player in dataList" :key="player.id">
                <span>{{ player.name }}</span>
                <div>
                    <button class="btn btn-warning btn-sm me-2" @click="openModal(player)">Edit</button>
                    <button class="btn btn-danger btn-sm" @click="deletePlayer(player.id)">Delete</button>
                </div>
            </li>
        </ul>

        <!-- Modal for Adding/Editing -->
        <div class="modal fade" id="playerModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">{{ isEditing ? 'Edit' : 'Add' }} Player</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <input v-model="formData.name" class="form-control mb-2" placeholder="Name" />
                        <input v-model="formData.position" class="form-control mb-2" placeholder="Position" />
                        <input v-model="formData.nationality" class="form-control mb-2" placeholder="Nationality" />
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="savePlayer">{{ isEditing ? 'Save Changes' : 'Add Player' }}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    props: ['dataList'],
    data() {
        return {
            formData: { name: '', position: '', nationality: '' },
            isEditing: false,
            editingPlayerId: null,
        }
    },
    methods: {
        openModal(player = null) {
            this.isEditing = !!player;
            this.editingPlayerId = player ? player.id : null;
            this.formData = player ? { ...player } : { name: '', position: '', nationality: '' };
            new bootstrap.Modal(document.getElementById('playerModal')).show();
        },
        async savePlayer() {
            const url = this.isEditing ? `http://localhost:8000/api/player/${this.editingPlayerId}/` : 'http://localhost:8000/api/player/';
            const method = this.isEditing ? 'PUT' : 'POST';

            await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.formData),
            });
            this.updateList();
            bootstrap.Modal.getInstance(document.getElementById('playerModal')).hide();
        },
        async deletePlayer(id) {
            await fetch(`http://localhost:8000/api/player/delete/${id}/`, { method: 'DELETE' });
            this.updateList();
        },
        async updateList() {
            const response = await fetch('http://localhost:8000/api/players/');
            const updatedList = await response.json();
            this.$emit('update-list', { model: 'player', list: updatedList.players });
        },
    },
}
</script>
