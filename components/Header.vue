<template>
  <b-navbar type="dark" variant="dark" :sticky="true">
    <b-navbar-nav>
      <li class="nav-item">
        <NuxtLink to="/" class="nav-link">Home</NuxtLink>
      </li>
    </b-navbar-nav>
    <b-navbar-nav class="ml-auto">
      <NuxtLink class="btn btn-outline-light" to="/graph">See Graph</NuxtLink>
    </b-navbar-nav>
  </b-navbar>
</template>