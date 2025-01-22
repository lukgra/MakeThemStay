import { createRouter, createWebHistory } from 'vue-router';
import EmployeeForm from '../views/EmployeeForm.vue';
import EmployeeList from '../views/EmployeeList.vue';

const routes = [    
    { path: '/employees', component: EmployeeList },
    { path: '/new-employee', component: EmployeeForm },
    { path: '/edit-employee/:employeeId', name: 'EditEmployee', component: EmployeeForm }
];

export default createRouter({
    history: createWebHistory(),
    routes,
});