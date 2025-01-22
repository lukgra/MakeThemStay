<template>
    <div id="app">
        <header>
            <h1>
                <router-link to="/" class="logo">MakeThemStay!</router-link>
            </h1>
            <nav>
                <router-link to="/new-employee">Add Employee</router-link>
                <router-link to="/employees">Employee List</router-link>
            </nav>
        </header>
        <main>
            <div v-if="$route.path === '/'">
                <p class="description">
                    <b>Welcome to <i>MakeThemStay!</i></b>
                </p>
                <br>
                <p class="sub_description">
                    An app made for companies that somehow can't figure out why their employees leave...<br>
                    For starters, You can add a new employee in the top right corner
                </p>
            </div>
            <router-view :key="$route.fullPath" />
        </main>
    </div>
</template>

<script>
    export default {
        name: "App",
    };
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

/* General */
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    color: #e0e0e0;
    background-color: #2c3e50;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

html, body {
    margin: 0;
}

/* Header & Navigation Bar */
header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #1e2a38;
    padding: 20px 40px;
    position: fixed; /* Fixes the header at the top */
    top: 0;
    width: 100%; /* Ensures the header spans the full width */
    z-index: 1000; /* Keeps the header above other content */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Optional: Add shadow for visual separation */
    box-sizing: border-box; /* Ensures padding is included in width calculation */
}

.logo {
    text-decoration: none;
    color: inherit;
}

nav {
    display: flex;
    gap: 15px;
}

nav a {
    color: white;
    text-decoration: none;
    font-size: 16px;
    padding: 10px 15px;
    border-radius: 5px;
    transition: background-color 0.3s ease, color 0.3s ease;
}

nav a:hover {
    background-color: #34495e;
}

/* nav a.router-link-active {
    background-color: #42b983;
    color: white;
    font-weight: bold;
    border-radius: 5px;
} */

header h1 {
    margin: 0;
    font-size: 36px;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
    color: #ffffff;
    letter-spacing: 3px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
    padding: 5px 0;
}

/* Main Content */
main {
    padding: 150px; /* Optional padding for main content */
}

/* Description */
.description {
    margin: 40px 40px;
    font-size: 40px;
    color: #e0e0e0;
    text-align: center;
    line-height: 1.6;
}

.sub_description {
    margin: 40px 40px;
    font-size: 32px;
    color: #e0e0e0;
    text-align: center;
    line-height: 1.6; /* Increase line height for more space between lines */
}
</style>