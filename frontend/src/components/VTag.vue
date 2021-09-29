<template>
  <router-link :to="homeRoute" :class="className" v-text="name"></router-link>
</template>

<script>
export default {
  name: "KrvTag",
  props: {
    name: {
      type: String,
      required: true,
    },
    className: {
      type: String,
      default: "tag-pill tag-default",
    },
  },
  computed: {
    homeRoute: () => ({ name: "home-tag", params: { tag: name } }),
  },
};
</script>
