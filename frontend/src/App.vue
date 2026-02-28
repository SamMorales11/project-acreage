<script setup>
import { ref, onMounted } from 'vue'
import api from './services/api'
import Chart from 'chart.js/auto'

const form = ref({
  luas_tanah: 100,
  luas_bangunan: 80,
  kamar_tidur: 3,
  kamar_mandi: 2,
  lokasi_skor: 2
})

const predictionResult = ref(0)
const isLoading = ref(false)
let chartInstance = null

/**
 * HELPER: Mengubah angka menjadi format Rupiah (Rp xx.xxx.xxx)
 */
const formatRupiah = (number) => {
  // Kita kalikan 1.000.000 karena model mengembalikan nilai dalam satuan "Juta"
  const fullValue = number * 1000000;
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(fullValue);
}

const getPrediction = async () => {
  isLoading.value = true
  try {
    const payload = {
      luas_tanah: Number(form.value.luas_tanah),
      luas_bangunan: Number(form.value.luas_bangunan),
      kamar_tidur: Number(form.value.kamar_tidur),
      kamar_mandi: Number(form.value.kamar_mandi),
      lokasi_skor: Number(form.value.lokasi_skor)
    }
    
    const response = await api.predictPrice(payload)
    predictionResult.value = response.data.estimasi_harga
  } catch (error) {
    console.error("Gagal mengambil prediksi:", error)
    alert("Gagal terhubung ke server AI.")
  } finally {
    isLoading.value = false
  }
}

const loadAnalytics = async () => {
  try {
    const response = await api.getAnalytics()
    if (response.data.labels && response.data.labels.length > 0) {
      renderChart(response.data.labels, response.data.values)
    }
  } catch (error) {
    console.error("Gagal memuat data analitik:", error)
  }
}

const renderChart = (labels, values) => {
  const ctx = document.getElementById('importanceChart')
  if (chartInstance) chartInstance.destroy()
  
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels.map(l => l.replace('_', ' ').toUpperCase()),
      datasets: [{
        label: 'Tingkat Pengaruh (%)',
        data: values,
        backgroundColor: '#3b82f6',
        borderRadius: 8,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false }
      }
    }
  })
}

onMounted(() => {
  loadAnalytics()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-900">
    <nav class="bg-acreage-dark p-4 shadow-lg text-white">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold tracking-tight italic uppercase">Acreage <span class="text-blue-400">.</span></h1>
        <div class="flex items-center space-x-2">
          <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          <span class="text-xs font-mono uppercase tracking-widest text-gray-300">ML Engine Active</span>
        </div>
      </div>
    </nav>

    <main class="container mx-auto py-8 px-4 grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <section class="lg:col-span-4 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
        <h2 class="text-lg font-bold mb-6 text-gray-800 uppercase tracking-tight">Property Specs</h2>
        <form @submit.prevent="getPrediction" class="space-y-5">
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Luas Tanah (m²)</label>
            <input v-model="form.luas_tanah" type="number" class="w-full rounded-lg border-gray-200 bg-gray-50 p-3 focus:ring-2 focus:ring-blue-500 outline-none transition">
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Luas Bangunan (m²)</label>
            <input v-model="form.luas_bangunan" type="number" class="w-full rounded-lg border-gray-200 bg-gray-50 p-3 focus:ring-2 focus:ring-blue-500 outline-none transition">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Bedrooms</label>
              <input v-model="form.kamar_tidur" type="number" class="w-full rounded-lg border-gray-200 bg-gray-50 p-3 focus:ring-2 focus:ring-blue-500 outline-none transition">
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Bathrooms</label>
              <input v-model="form.kamar_mandi" type="number" class="w-full rounded-lg border-gray-200 bg-gray-50 p-3 focus:ring-2 focus:ring-blue-500 outline-none transition">
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Location Tier</label>
            <select v-model="form.lokasi_skor" class="w-full rounded-lg border-gray-200 bg-gray-50 p-3 focus:ring-2 focus:ring-blue-500 outline-none transition">
              <option value="1">Tier 1 - Pinggiran</option>
              <option value="2">Tier 2 - Urban/Menengah</option>
              <option value="3">Tier 3 - Pusat Bisnis (CBD)</option>
            </select>
          </div>
          <button type="submit" :disabled="isLoading" 
            class="w-full bg-blue-600 text-white py-4 rounded-xl font-bold uppercase tracking-widest text-sm hover:bg-blue-700 transition-all shadow-lg disabled:opacity-50">
            {{ isLoading ? 'Predicting...' : 'Analyze Price' }}
          </button>
        </form>
      </section>

      <section class="lg:col-span-8 space-y-6">
        <div class="bg-gradient-to-br from-blue-600 to-indigo-800 text-white p-10 rounded-2xl shadow-xl relative overflow-hidden">
          <div class="relative z-10">
            <p class="text-blue-100 text-xs font-black uppercase tracking-[0.2em] mb-2 opacity-80">Estimated Market Value</p>
            <h3 class="text-4xl md:text-5xl font-black tracking-tighter">
              {{ formatRupiah(predictionResult) }}
            </h3>
            <p class="mt-4 text-sm text-blue-200 italic font-light">*Berdasarkan analisis algoritma Random Forest Regressor</p>
          </div>
          <div class="absolute -right-10 -bottom-10 opacity-10">
            <svg class="w-64 h-64" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg>
          </div>
        </div>

        <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <h3 class="text-sm font-black text-gray-400 uppercase tracking-widest mb-6">Model Explanation (XAI)</h3>
          <div class="h-[300px] w-full">
            <canvas id="importanceChart"></canvas>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>