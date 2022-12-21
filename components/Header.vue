<template>
  <b-navbar type="dark" variant="dark" :sticky="true">
    <b-navbar-nav>
      <li class="nav-item">
        <NuxtLink to="/" class="nav-link">Home</NuxtLink>
      </li>
    </b-navbar-nav>
    <b-navbar-nav class="ml-auto">
      <span v-if="$route.path == '/'">
        <NuxtLink class="btn btn-outline-light" to="/graph">See Graph</NuxtLink>
      </span>
      <span v-else-if="$route.path == '/graph'">
        <NuxtLink class="btn btn-outline-light" v-b-toggle.graph-info to="#info">Graph Info</NuxtLink>
      </span>
    </b-navbar-nav>
  </b-navbar>
</template>