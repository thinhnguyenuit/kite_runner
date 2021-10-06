<template>
  <footer>
    <div class="container">
      <router-link class="logo-font" :to="{ name: 'home', params: {} }">
        Kite Runner
      </router-link>
      <span class="attribution">
        Source code:
        <a
          rel="noopener noreferrer"
          target="blank"
          href="https://github.com/thinhnguyenuit/kite_runner"
          >Github</a
        >
      </span>
    </div>
  </footer>
</template>

<script>
export default {
  name: "RwvFooter",
};
</script>
