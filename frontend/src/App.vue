<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-900">
    <nav class="bg-acreage-dark p-4 shadow-lg text-white">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold tracking-tight">ACREAGE <span class="text-blue-400">.</span></h1>
        <span class="text-xs bg-blue-500/20 px-2 py-1 rounded border border-blue-500/30">ML-Powered Analytics</span>
      </div>
    </nav>

    <main class="container mx-auto py-8 px-4 grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <section class="lg:col-span-4 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 class="text-xl font-semibold mb-6 border-b pb-2">Property Specifications</h2>
        <form @submit.prevent="getPrediction" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Luas Tanah (m²)</label>
            <input v-model="form.luas_tanah" type="number" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2.5 bg-gray-50">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Luas Bangunan (m²)</label>
            <input v-model="form.luas_bangunan" type="number" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2.5 bg-gray-50">
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Kamar Tidur</label>
              <input v-model="form.kamar_tidur" type="number" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2.5 bg-gray-50">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Kamar Mandi</label>
              <input v-model="form.kamar_mandi" type="number" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2.5 bg-gray-50">
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Skor Lokasi (1-3)</label>
            <select v-model="form.lokasi_skor" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2.5 bg-gray-50">
              <option value="1">1 - Pinggiran Kota</option>
              <option value="2">2 - Menengah</option>
              <option value="3">3 - Pusat Kota Strategis</option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Pilih seberapa strategis lokasi properti.</p>
          </div>

          <button type="submit" class="w-full bg-blue-600 text-white py-3 mt-4 rounded-lg font-semibold hover:bg-blue-700 transition duration-200 shadow-md">
            Analyze Price
          </button>
        </form>
      </section>

      <section class="lg:col-span-8 space-y-6">
        <div class="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-8 rounded-xl shadow-md flex justify-between items-center relative overflow-hidden">
          <div class="z-10">
            <p class="text-blue-200 uppercase text-xs font-bold tracking-widest mb-1">Estimated Market Value</p>
            <h3 class="text-4xl md:text-5xl font-bold">
              Rp {{ predictionResult || '0' }} <span class="text-xl font-light">Million</span>
            </h3>
          </div>
          <div class="absolute right-[-20px] bottom-[-20px] opacity-10">
            <svg class="w-40 h-40" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg>
          </div>
        </div>

        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-80 flex flex-col items-center justify-center text-gray-400">
          <svg class="w-12 h-12 mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          <p class="italic">Chart Visualisasi (Feature Importance) akan muncul di sini.</p>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// State untuk menyimpan input user
const form = ref({
  luas_tanah: 100,
  luas_bangunan: 80,
  kamar_tidur: 3,
  kamar_mandi: 2,
  lokasi_skor: 2
})

// State untuk menyimpan hasil prediksi dari API
const predictionResult = ref(0)

// Fungsi yang dijalankan saat tombol "Analyze Price" ditekan
const getPrediction = async () => {
  // Untuk sementara kita log dulu ke console.
  // Di langkah selanjutnya, kita ganti ini dengan request Axios ke FastAPI
  console.log("Data yang siap dikirim ke backend:", form.value)
  alert("Layout siap! Buka console browser untuk melihat data form yang akan dikirim.")
}
</script>