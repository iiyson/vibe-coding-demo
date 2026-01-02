<template>
  <canvas ref="canvasRef" width="60" height="60" class="shape-canvas"></canvas>
</template>

<script setup>
import { onMounted, watch, ref } from "vue";

const props = defineProps({
  type: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    required: true,
  },
});

const canvasRef = ref(null);

function draw() {
  const canvas = canvasRef.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = props.color || "#ccc";
  ctx.beginPath();

  if (props.type === "circle") {
    ctx.arc(w / 2, h / 2, w / 2 - 5, 0, Math.PI * 2);
  } else if (props.type === "square") {
    ctx.rect(5, 5, w - 10, h - 10);
  } else if (props.type === "triangle") {
    ctx.moveTo(w / 2, 5);
    ctx.lineTo(5, h - 5);
    ctx.lineTo(w - 5, h - 5);
    ctx.closePath();
  }

  ctx.fill();
}

onMounted(draw);
watch(() => [props.type, props.color], draw);
</script>

<style scoped>
.shape-canvas {
  display: block;
  margin: 0 auto;
  border-radius: 4px;
}
</style>
