<template>
  <div class="admin-portal">
    <div class="section-title">Data Management</div>
    <form @submit.prevent="handleSubmit" class="data-form">
      <div class="form-grid">
        <div class="form-group">
          <label>Name</label>
          <input v-model.trim="form.name" class="form-control" placeholder="Enter shape name" />
        </div>
        <div class="form-group">
          <label>Shape Type</label>
          <select v-model="form.shape_type" class="form-control">
            <option value="circle">Circle</option>
            <option value="square">Square</option>
            <option value="triangle">Triangle</option>
          </select>
        </div>
        <div class="form-group">
          <label>Color (CSS Color)</label>
          <input v-model.trim="form.color" class="form-control" placeholder="e.g. red, #ff0000, blue" />
        </div>
        <div class="form-group">
          <label>Timestamp</label>
          <input type="datetime-local" v-model="form.timestamp" class="form-control" />
        </div>
      </div>
      <div class="form-actions">
        <button class="button primary" type="submit" style="width: auto; min-width: 120px;">
          {{ editingId ? "Save Changes" : "Add Data" }}
        </button>
        <button
          v-if="editingId"
          type="button"
          class="button ghost"
          @click="resetForm"
        >
          Cancel
        </button>
      </div>
      <div v-if="error" class="error-text" style="text-align: left;">
        {{ error }}
      </div>
    </form>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Color</th>
            <th>Shape</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td style="font-weight: 500;">{{ item.name }}</td>
            <td>{{ item.color }}</td>
            <td>
              <ShapeCanvas :type="item.shape_type" :color="item.color" />
            </td>
            <td class="timestamp-cell">{{ formatTimestamp(item.timestamp) }}</td>
            <td>
              <div style="display: flex; gap: 8px;">
                <button class="button ghost" style="padding: 4px 12px;" @click="startEdit(item)">
                  Edit
                </button>
                <button class="button danger" style="padding: 4px 12px; background-color: #fee2e2; color: #b91c1c; border: none;" @click="deleteItem(item.id)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="items.length === 0">
            <td colspan="5" style="text-align: center; color: var(--text-muted); padding: 40px;">
              No data available
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
/**
 * Admin Portal component for managing shape data items.
 */
import { onMounted, onUnmounted, reactive, ref } from "vue";
import axios from "axios";
import ShapeCanvas from "./ShapeCanvas.vue";

const items = ref([]);
const editingId = ref(null);
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
    })
    .catch(() => {
      error.value = "Failed to load data";
    });
}

onMounted(() => {
  loadItems();
  // Poll for updates every 3 seconds
  pollTimer = setInterval(loadItems, 3000);
});

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer);
});

const form = reactive({
  name: "",
  color: "",
  shape_type: "circle",
  timestamp: ""
});

/**
 * Validates the form data before submission.
 */
function validateForm() {
  if (!form.name || !form.color || !form.timestamp || !form.shape_type) {
    error.value = "Please fill in all fields";
    return false;
  }
  if (form.name.length > 100) {
    error.value = "Name cannot exceed 100 characters";
    return false;
  }
  if (form.color.length > 50) {
    error.value = "Color cannot exceed 50 characters";
    return false;
  }
  error.value = "";
  return true;
}

/**
 * Converts local datetime-local value to ISO format.
 */
function toIsoTimestamp(value) {
  if (!value) return null;
  const date = new Date(value);
  return date.toISOString();
}

/**
 * Formats ISO timestamp to local readable string.
 */
function formatTimestamp(ts) {
  if (!ts) return "-";
  return new Date(ts).toLocaleString("en-US", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  });
}

/**
 * Handles form submission for both creating and updating items.
 */
function handleSubmit() {
  if (!validateForm()) return;

  const postData = {
    name: form.name,
    color: form.color,
    shape_type: form.shape_type,
    timestamp: toIsoTimestamp(form.timestamp)
  };

  const request = editingId.value
    ? axios.put(`/api/items/${editingId.value}/`, postData)
    : axios.post("/api/items/", postData);

  request
    .then(() => {
      resetForm();
      loadItems();
    })
    .catch((e) => {
      if (e.response?.status === 400) {
        error.value = "Submission failed: Invalid data format";
      } else if (e.response?.status === 403) {
        error.value = "Permission denied";
      } else {
        error.value = "Operation failed, please try again later";
      }
    });
}

/**
 * Deletes an item by ID.
 */
function deleteItem(id) {
  if (!confirm("Are you sure you want to delete this item?")) return;
  axios
    .delete(`/api/items/${id}/`)
    .then(() => loadItems())
    .catch(() => {
      error.value = "Failed to delete item";
    });
}

/**
 * Populates the form with item data for editing.
 */
function startEdit(item) {
  editingId.value = item.id;
  form.name = item.name;
  form.color = item.color;
  form.shape_type = item.shape_type;
  form.timestamp = item.timestamp ? item.timestamp.slice(0, 16) : "";
  error.value = "";
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetForm() {
  editingId.value = null;
  form.name = "";
  form.color = "";
  form.shape_type = "circle";
  form.timestamp = "";
  error.value = "";
}
</script>

<style scoped>
.section-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 24px;
  color: var(--text-main);
}
.data-form {
  background: #f8fafc;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 32px;
}
.form-actions {
  display: flex;
  gap: 12px;
}

</style>
 
