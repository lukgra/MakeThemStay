<template>
    <div>
        <h1>Employee Management Panel</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Chance of Leaving</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <template v-for="employee in employees" :key="employee.id">
                    <tr>
                        <td>{{ employee.id }}</td>
                        <td>{{ employee.name }}</td>
                        <td>{{ employee.leave_chance }}%</td>
                        <td>
                            <button @click="toggleDetails(employee.id)">Details</button>
                            <button @click="editEmployee(employee.id)">Edit</button>
                            <button @click="deleteEmployee(employee.id)">Delete</button>
                        </td>
                    </tr>

                    <!-- Details row for the employee, conditionally rendered -->
                    <tr v-show="detailsVisible === employee.id" class="details-row">
                        <td colspan="4">
                            <p><strong>Features with the biggest impact:</strong> {{ employee.position }}</p>
                            <ul>
                                <li v-for="(feature, index) in employee.exp_features" :key="index">
                                    {{ feature }}: <strong>{{ employee.features[feature] }}</strong>
                                </li>
                            </ul>
                        </td>
                    </tr>
                </template>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from '@/services/axios';

export default {
    data() {
        return {
            employees: [],
            detailsVisible: null,
        };
    },
    mounted() {
        this.fetchEmployees();
    },
    methods: {
        async fetchEmployees() {
            try {
                const response = await axios.get('/all-employees');
                this.employees = response.data || [];
            }
            catch (error) {
                console.error('Error fetching employees:', error);
                this.employees = [];
            }
        },
        
        async deleteEmployee(id) {
            try {
                await axios.delete(`/delete/${id}`);
                this.fetchEmployees();
            } catch (error) {
                console.error('Error deleting employee:', error);
            }
        },

        toggleDetails(id) {
            this.detailsVisible = this.detailsVisible === id ? null : id;
        },

        editEmployee(id) {
            this.$router.push({ name: 'EditEmployee', params: { employeeId: id } });
        }
    }
};
</script>

<style scoped>
button {
    margin: 5px;
    padding: 10px;
    background-color: #42b983;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
}

button:hover {
    background-color: #369f6e;
}

table {
    width: 100%;
    border-collapse: collapse; /* Merge borders between cells */
    margin-top: 20px;
    border-radius: 10px; /* Rounded corners for the table */
    border: 1px solid #ddd; /* Border for the entire table */
    overflow: hidden; /* Prevent overflow of content */
}

th, td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd; /* Cell borders */
}

th {
    background-color: #42b983; /* Matching button green */
    color: white;
    font-weight: bold;
    font-size: 18px; /* Font size matching form labels */
}

td {
    background-color: #d0d0d0; /* Even darker background for table data */
    color: #333; /* Dark text color for better contrast */
}

.details-row {
    overflow: hidden;
    height: 0;
    transition: height 0.5s ease-in-out, opacity 0.5s ease;
}

.details-content {
    padding: 15px;
    background-color: #f9f9f9; /* Light background for details */
    border-radius: 5px;
    border-top: 1px solid #ddd;
    opacity: 0;
}

.details-row.show {
    height: auto;
    opacity: 1;
}
</style>