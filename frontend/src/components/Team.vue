<template>
    <div>
        <button class="btn btn-primary mb-3" @click="openModal()">Add Team</button>
        <ul class="list-group mb-3">
            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="team in dataList" :key="team.id">
                <span>{{ team.name }} - {{ team.city }}</span>
                <div>
                    <button class="btn btn-warning btn-sm me-2" @click="openModal(team)">Edit</button>
                    <button class="btn btn-danger btn-sm" @click="deleteTeam(team.id)">Delete</button>
                </div>
            </li>
        </ul>

        <!-- Modal for Adding/Editing -->
        <div class="modal fade" id="teamModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">{{ isEditing ? 'Edit' : 'Add' }} Team</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <input v-model="formData.name" class="form-control mb-2" placeholder="Name" />
                        <input v-model="formData.city" class="form-control mb-2" placeholder="City" />
                        <input v-model="formData.founded" class="form-control mb-2" type="number" placeholder="Founded Year" />
                        <textarea v-model="formData.description" class="form-control" placeholder="Description"></textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="saveTeam">{{ isEditing ? 'Save Changes' : 'Add Team' }}</button>
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
            formData: { name: '', city: '', founded: '', description: '' },
            isEditing: false,
            editingTeamId: null,
        }
    },
    methods: {
        openModal(team = null) {
            this.isEditing = !!team;
            this.editingTeamId = team ? team.id : null;
            this.formData = team ? { ...team } : { name: '', city: '', founded: '', description: '' };
            new bootstrap.Modal(document.getElementById('teamModal')).show();
        },
        async saveTeam() {
            const url = this.isEditing ? `http://localhost:8000/api/team/${this.editingTeamId}/` : 'http://localhost:8000/api/team/';
            const method = this.isEditing ? 'PUT' : 'POST';

            await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.formData),
            });
            this.updateList();
            bootstrap.Modal.getInstance(document.getElementById('teamModal')).hide();
        },
        async deleteTeam(id) {
            await fetch(`http://localhost:8000/api/team/delete/${id}/`, { method: 'DELETE' });
            this.updateList();
        },
        async updateList() {
            const response = await fetch('http://localhost:8000/api/teams/');
            const updatedList = await response.json();
            this.$emit('update-list', { model: 'team', list: updatedList.teams });
        },
    },
}
</script>
