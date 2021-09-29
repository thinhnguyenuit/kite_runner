<template>
  <div id="app">
    <KrvHeader />
    <router-view></router-view>
    <RwvFooter />
  </div>
</template>

<script>
import KrvHeader from "@/components/TheHeader";
import RwvFooter from "@/components/TheFooter";

export default {
  name: "App",
  components: {
    KrvHeader,
    RwvFooter,
  },
};
</script>

<style></style>
