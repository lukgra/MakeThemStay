<template>
    <h1 v-if="isEditing">Edit Employee</h1>
    <h1 v-else>New Employee</h1>

    <form @submit.prevent="submitForm">
        <!-- Renders Label + Input + Error Message -->
        <div class="form-group" v-for="field in formFields" :key="field.name">
            <!-- Question Label -->
            <label :for="field.name">{{ field.label }}</label>

            <!-- Input Field -->
            <template v-if="field.type === 'select'">
                <select
                :id="field.name"
                v-model="formData[field.name]"
                @change="validateInput(field.name)"
                :class="{'invalid': !field.isValid}"
                >
                    <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
                </select>
            </template>
            <template v-else>
                <input
                :id="field.name"
                :type="field.inputType"
                v-model="formData[field.name]"
                :placeholder="field.placeholder"
                @input="validateInput(field.name, $event)"
                :class="{'invalid': !field.isValid}"
                min="0"
                />
            </template>

            <!-- Error message -->
            <p :style="{ visibility: field.isValid ? 'hidden' : 'visible' }" class="error-message">This field is required.</p>
        </div>

        <!-- Add Employee Button -->
        <button type="submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <span v-else>{{ isEditing ? 'Save Changes' : 'Add Employee' }}</span>
        </button>
    </form>
</template>

<script>
import axios from '@/services/axios';

export default {
    data() {
        return {
            formFields: [
                { name: 'Name', label: '1. Full Name', inputType: 'text', type: 'input', placeholder: 'Enter Employee Name', isValid: true },
                { name: 'Age', label: '2. Age', inputType: 'number', type: 'input', placeholder: 'Enter Age (18-60)', isValid: true },
                { name: 'Gender', label: '3. Gender', type: 'select', options: ['Male', 'Female', 'Other'], isValid: true },
                { name: 'Years at Company', label: '4. Years spent at the company', inputType: 'number', type: 'input', placeholder: 'Enter Years', isValid: true },
                { name: 'Monthly Income', label: '5. Monthly Income', inputType: 'number', type: 'input', placeholder: 'Enter Income in $', isValid: true },
                { name: 'Overtime', label: '6. Doing Overtime?', type: 'select', options: ['Yes', 'No'], isValid: true },
                { name: 'Number of Dependents', label: '7. Number of Dependents', inputType: 'number', type: 'input', placeholder: 'Enter Number', isValid: true },
                { name: 'Job Role', label: '8. Job Role', type: 'select', options: ['Finance', 'Healthcare', 'Technology', 'Education', 'Media', 'Other'], isValid: true },
                { name: 'Work-Life Balance', label: '9. Work-Life Balance', type: 'select', options: ['Poor', 'Below Average', 'Good', 'Excellent'], isValid: true },
                { name: 'Job Satisfaction', label: '10. Job Satisfaction Level', type: 'select', options: ['Very Low', 'Low', 'Medium', 'High'], isValid: true },
                { name: 'Performance Rating', label: '11. Performance Rating', type: 'select', options: ['Low', 'Below Average', 'Average', 'High'], isValid: true },
                { name: 'Number of Promotions', label: '12. Number of Promotions Received', inputType: 'number', type: 'input', placeholder: 'Enter Number', isValid: true },
                { name: 'Distance from Home', label: '13. Distance from Home', inputType: 'number', type: 'input', placeholder: 'Enter Distance (miles)', isValid: true },
                { name: 'Education Level', label: '14. Education Level', type: 'select', options: ['High School', 'Associate Degree', 'Bachelor’s Degree', 'Master’s Degree', 'Doctorate'], isValid: true },
                { name: 'Marital Status', label: '15. Marital Status', type: 'select', options: ['Divorced', 'Married', 'Single'], isValid: true },
                { name: 'Job Level', label: '16. Job Level', type: 'select', options: ['Entry-level', 'Mid-level', 'Senior-level'], isValid: true },
                { name: 'Company Size', label: '17. Company Size', type: 'select', options: ['Small', 'Medium', 'Large'], isValid: true },
                { name: 'Company Tenure', label: '18. Company Tenure', inputType: 'number', type: 'input', placeholder: 'Enter Years', isValid: true },
                { name: 'Remote Work', label: '19. Remote Work', type: 'select', options: ['Yes', 'No'], isValid: true },
                { name: 'Leadership Opportunities', label: '20. Leadership Opportunities', type: 'select', options: ['Yes', 'No'], isValid: true },
                { name: 'Innovation Opportunities', label: '21. Innovation Opportunities', type: 'select', options: ['Yes', 'No'], isValid: true },
                { name: 'Company Reputation', label: '22. Company Reputation', type: 'select', options: ['Very Poor', 'Poor', 'Good', 'Excellent'], isValid: true },
                { name: 'Employee Recognition', label: '23. Employee Recognition', type: 'select', options: ['Very Low', 'Low', 'Medium', 'High'], isValid: true }
            ],
            formData: {},
            loading: false,
            isEditing: false
        };
    },

    created() {
        const employeeId = this.$route.params.employeeId;
        if (employeeId) {
            this.isEditing = true;
            this.loadEmployeeData(employeeId);
        }
        else {
            this.formData = {};
            this.isEditing = false;
            this.formFields.forEach(field => {
                this.formData[field.name] = null;
            });
        }
    },

    methods: {
        async loadEmployeeData(id) {
            try {
                const response = await axios.get(`/employee/${id}`)
                this.formData = response.data;
                console.log(this.formData);
            }
            catch (error) {
                console.error('Error loading employee data:', error);
            }
        },

        validateInput(name) {
            const field = this.formFields.find(field => field.name === name);
            const value = this.formData[name];
            
            if (value !== null && value !== undefined && value !== '') {
                if (field.inputType === 'number' && value < 0) {
                    field.isValid = false;
                }
                else {
                    field.isValid = true;
                }
            }
            else {
                field.isValid = false;  // Set as invalid if the field is empty
            }
        },

        async submitForm() {
            this.loading = true; // Animation
            let isValid = true; // Form validation
            let firstInvalidField = null;
            const invalidFields = [];

            // Check all fields inside the form
            this.formFields.forEach(field => {
                if (!this.formData[field.isValid]) {
                    this.validateInput(field.name);  // Validate each field

                    if (!field.isValid) {
                        isValid = false;

                        if (!firstInvalidField) {
                          firstInvalidField = document.getElementById(field.name);
                        }
                    }
                }
            });

            if (!isValid) {
              if (firstInvalidField) {
                firstInvalidField.scrollIntoView({
                  behavior: 'smooth',
                  block: 'center',
                });
              }
              this.loading = false; // Animation
              return;
            }

            // Proceed with form submission if everything is valid
            try {
                const response = await axios.post('/add', {features: this.formData});
                this.loading = false
                this.$router.push('/employees')
            }
            catch (error) {
                console.error('Error predicting data:', error);
                this.loading = false
            }
        }
    }
};
</script>

<style scoped>
h1 {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
}

form {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 400px;
    margin: auto;
    padding-bottom: 40px; /* Add padding to the bottom of the form */
}

.form-group {
    display: flex;
    flex-direction: column;
}

label {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 8px;
}

input, select {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
}

input.invalid, select.invalid {
    border-color: red;
}

.error-message {
    color: red;
    font-size: 14px;
    margin-top: 5px;
    min-height: 18px;
    visibility: hidden;
}

.error-message.visible {
    visibility: visible;
}

button {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 12px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 5px;
    margin-bottom: 20px; /* Add margin to the bottom of the button */
    display: flex;
    align-items: center; /* Make sure the spinner aligns with the text */
    justify-content: center;
}

button:hover {
    background-color: #369f6e;
}

button:disabled {
    background-color: #b2dfdb;
    cursor: not-allowed;
}

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 2s linear infinite;
    margin-right: 10px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>