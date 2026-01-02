<template>
  <div class="app-container">
    <h1>SHAPE INSIGHT</h1>

    <div v-if="!currentUser" class="auth-container card">
      <div class="auth-tabs">
        <div
          class="auth-tab"
          :class="{ active: authMode === 'login' }"
          @click="authMode = 'login'"
        >
          Login
        </div>
        <div
          class="auth-tab"
          :class="{ active: authMode === 'register' }"
          @click="authMode = 'register'"
        >
          Register
        </div>
      </div>

      <div v-if="authMode === 'login'">
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>Username</label>
            <input
              v-model.trim="loginForm.username"
              class="form-control"
              placeholder="Enter username"
            />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input
              type="password"
              v-model="loginForm.password"
              class="form-control"
              placeholder="Enter password"
            />
          </div>
          <button class="button primary" type="submit" :disabled="loading">
            {{ loading ? "Logging in..." : "Login Now" }}
          </button>
          <div v-if="loginForm.error" class="error-text">
            {{ loginForm.error }}
          </div>
        </form>
      </div>

      <div v-else>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>Username</label>
            <input
              v-model.trim="registerForm.username"
              class="form-control"
              placeholder="Enter username"
            />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input
              type="password"
              v-model="registerForm.password"
              class="form-control"
              placeholder="Enter password"
            />
          </div>
          <div class="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              v-model="registerForm.confirmPassword"
              class="form-control"
              placeholder="Enter password again"
            />
          </div>
          <button class="button primary" type="submit" :disabled="loading">
            {{ loading ? "Registering..." : "Register & Login" }}
          </button>
          <div v-if="registerForm.error" class="error-text">
            {{ registerForm.error }}
          </div>
        </form>
      </div>
    </div>

    <div v-else class="portal-container card">
      <div class="header-actions">
        <div class="user-info">
          <span class="badge" :class="currentUser.isAdmin ? 'badge-admin' : 'badge-user'">
            {{ currentUser.isAdmin ? "Admin" : "User" }}
          </span>
          <strong>{{ currentUser.username }}</strong>
        </div>
        <button class="button ghost" @click="handleLogout">Logout</button>
      </div>

      <AdminPortal v-if="currentUser.isAdmin" />
      <UserPortal v-else />
    </div>
  </div>
</template>

<script setup>
/**
 * Main application component handling Authentication and Portal switching.
 */
import { reactive, ref } from "vue";
import axios from "axios";
import AdminPortal from "./components/AdminPortal.vue";
import UserPortal from "./components/UserPortal.vue";

const currentUser = ref(null);
const authMode = ref("login");
const loading = ref(false);

const loginForm = reactive({
  username: "",
  password: "",
  error: ""
});

const registerForm = reactive({
  username: "",
  password: "",
  confirmPassword: "",
  error: ""
});

/**
 * Applies or removes the Auth token from axios defaults.
 */
function applyToken(token) {
  if (token) {
    axios.defaults.headers.common.Authorization = `Token ${token}`;
  } else {
    delete axios.defaults.headers.common.Authorization;
  }
}

/**
 * Sets the current user state upon successful login/register.
 */
function handleLoginSuccess(data) {
  currentUser.value = {
    username: data.username,
    token: data.token,
    isAdmin: data.is_admin
  };
  applyToken(data.token);
}

function handleLogout() {
  applyToken(null);
  currentUser.value = null;
}

/**
 * Handles the login form submission.
 */
async function handleLogin() {
  loginForm.error = "";
  if (!loginForm.username || !loginForm.password) {
    loginForm.error = "Please enter username and password";
    return;
  }

  loading.value = true;
  try {
    const response = await axios.post("/api/auth/login/", {
      username: loginForm.username,
      password: loginForm.password
    });
    handleLoginSuccess(response.data);
    loginForm.username = "";
    loginForm.password = "";
  } catch (error) {
    loginForm.error = error.response?.data?.detail || "Login failed, please check your credentials";
  } finally {
    loading.value = false;
  }
}

/**
 * Handles the registration form submission.
 */
async function handleRegister() {
  registerForm.error = "";
  if (!registerForm.username || !registerForm.password || !registerForm.confirmPassword) {
    registerForm.error = "Please fill in all fields";
    return;
  }
  if (registerForm.password !== registerForm.confirmPassword) {
    registerForm.error = "Passwords do not match";
    return;
  }
  if (registerForm.password.length < 6) {
    registerForm.error = "Password must be at least 6 characters";
    return;
  }

  loading.value = true;
  try {
    const response = await axios.post("/api/auth/register/", {
      username: registerForm.username,
      password: registerForm.password
    });
    handleLoginSuccess(response.data);
    registerForm.username = "";
    registerForm.password = "";
    registerForm.confirmPassword = "";
  } catch (error) {
    registerForm.error = error.response?.data?.detail || "Registration failed, username may already exist";
  } finally {
    loading.value = false;
  }
}
</script>
