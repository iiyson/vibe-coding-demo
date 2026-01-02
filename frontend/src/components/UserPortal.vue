<template>
  <div class="user-portal">
    <div class="section-title">Shape Gallery</div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Created At</th>
            <th>Name</th>
            <th>Shape</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td class="timestamp-cell">
              {{ formatTimestamp(item.timestamp) }}
            </td>
            <td style="font-weight: 500;">
              {{ item.name }}
            </td>
            <td>
              <ShapeCanvas :type="item.shape_type" :color="item.color" />
            </td>
          </tr>
          <tr v-if="items.length === 0">
            <td colspan="3" style="text-align: center; color: var(--text-muted); padding: 40px;">
              No data available
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="error" class="error-text">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * User Portal component for viewing shape data items.
 */
import { onMounted, onUnmounted, ref } from "vue";
import axios from "axios";
import ShapeCanvas from "./ShapeCanvas.vue";

const items = ref([]);
const error = ref("");
let pollTimer = null;

/**
 * Fetches the list of shape items from the server.
 */
function loadItems() {
  axios
    .get("/api/items/")
    .then((response) => {
      items.value = response.data;
      error.value = "";
    })
    .catch((e) => {
      if (e.response?.status === 401) {
        error.value = "Session expired";
      } else {
        error.value = "Failed to load data";
      }
    });
}

/**
 * Formats ISO timestamp to local readable string.
 */
function formatTimestamp(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString("en-US", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  });
}

onMounted(() => {
  loadItems();
  // Poll for updates every 5 seconds
  pollTimer = setInterval(loadItems, 5000);
});

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer);
});
</script>

<style scoped>
.section-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 24px;
  color: var(--text-main);
}
</style>
