<script setup>
import { ref, onMounted, watch } from 'vue'
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

// --- HELPER: FORMAT RUPIAH ---
const formatRupiah = (number) => {
  const fullValue = number * 1000000;
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(fullValue);
}

// --- HELPER: DEBOUNCE FUNCTION ---
const debounce = (fn, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      fn(...args);
    }, delay);
  };
};

// --- API CALLS ---
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

// --- REAL-TIME WATCHER ---
const debouncedPredict = debounce(() => {
  getPrediction();
}, 300);

watch(form, () => {
  debouncedPredict();
}, { deep: true });


// --- CHART LOGIC ---
const renderChart = (labels, values) => {
  const ctx = document.getElementById('importanceChart')
  if (chartInstance) chartInstance.destroy()
  
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels.map(l => {
        const normalizedKey = String(l).toLowerCase().replace(/\s+/g, '_');
        const proLabels = {
          luas_tanah: 'Lot Area',
          luas_bangunan: 'Building Area',
          kamar_tidur: 'Bedrooms',
          kamar_mandi: 'Bathrooms',
          lokasi: 'Location Tier',
          lokasi_skor: 'Location Tier'
        };
        return proLabels[normalizedKey] || String(l).toUpperCase();
      }),
      datasets: [{
        label: ' Feature Impact (%)',
        data: values,
        backgroundColor: '#3b82f6', 
        hoverBackgroundColor: '#60a5fa', 
        borderRadius: 50, 
        barPercentage: 0.4, 
        borderSkipped: false 
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          titleFont: { size: 12, family: 'Inter, sans-serif', color: '#94a3b8' },
          bodyFont: { size: 14, weight: 'bold', family: 'Inter, sans-serif' },
          padding: 12,
          cornerRadius: 8,
          displayColors: false,
          borderColor: 'rgba(59, 130, 246, 0.2)',
          borderWidth: 1
        }
      },
      animation: {
        duration: 400, 
        easing: 'easeOutQuart'
      },
      scales: {
        x: {
          grid: { display: false, drawBorder: false },
          ticks: { display: false }
        },
        y: {
          grid: { display: false, drawBorder: false }, 
          ticks: { 
            color: '#94a3b8', 
            font: { size: 11, weight: '600', family: 'Inter, sans-serif', tracking: 'widest' },
            padding: 10 
          }
        }
      }
    }
  })
}

onMounted(() => {
  loadAnalytics();
  getPrediction(); 
})
</script>

<template>
  <div class="flex flex-col min-h-screen bg-[#0f172a] font-sans selection:bg-blue-500 selection:text-white">
    
    <nav class="sticky top-0 z-50 bg-[#0f172a]/80 backdrop-blur-md border-b border-slate-800 px-6 py-4">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
          </div>
          <h1 class="text-xl font-bold tracking-tight text-white uppercase">
            Acreage<span class="text-blue-500">.</span>
          </h1>
        </div>
        <div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/50 border border-slate-700">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span class="text-[10px] font-bold text-slate-300 tracking-widest uppercase">Live ML Engine</span>
        </div>
      </div>
    </nav>

    <main class="flex-grow w-full max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      
      <div class="mb-8">
        <h2 class="text-3xl font-light text-white tracking-tight">Property Valuation <span class="font-bold text-blue-500">Engine</span></h2>
        <p class="mt-2 text-sm text-slate-400">Interact with the parameters below to generate real-time market estimations.</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <section class="lg:col-span-4 bg-[#1e293b] rounded-2xl border border-slate-700/50 shadow-2xl p-6 h-fit relative overflow-hidden">
          <div class="absolute -top-24 -right-24 w-48 h-48 bg-blue-600/10 rounded-full blur-3xl"></div>

          <div class="flex items-center justify-between mb-8">
            <h3 class="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Live Simulator</h3>
            <svg v-if="isLoading" class="animate-spin h-4 w-4 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          </div>

          <form @submit.prevent class="space-y-8 relative z-10">
            
            <div class="space-y-3">
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1.5">Lot Area (m²)</label>
              <div class="relative bg-slate-800/50 rounded-xl p-3 border border-slate-700/50 mb-3 shadow-inner">
                <input v-model="form.luas_tanah" type="number" 
                  class="w-full text-center text-6xl font-black text-blue-400 font-mono focus:outline-none bg-transparent"
                  min="30" max="1000">
                <span class="absolute right-4 bottom-2 text-sm font-semibold text-slate-500 font-mono">m²</span>
              </div>
              <input v-model="form.luas_tanah" type="range" min="30" max="1000" step="5" class="custom-slider w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer">
            </div>

            <div class="space-y-3">
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1.5">Building Area (m²)</label>
              <div class="relative bg-slate-800/50 rounded-xl p-3 border border-slate-700/50 mb-3 shadow-inner">
                <input v-model="form.luas_bangunan" type="number" 
                  class="w-full text-center text-6xl font-black text-blue-400 font-mono focus:outline-none bg-transparent"
                  min="20" max="800">
                <span class="absolute right-4 bottom-2 text-sm font-semibold text-slate-500 font-mono">m²</span>
              </div>
              <input v-model="form.luas_bangunan" type="range" min="20" max="800" step="5" class="custom-slider w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer">
            </div>

            <div class="grid grid-cols-2 gap-6">
              <div class="space-y-3">
                <label class="flex justify-between items-center text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                  <span>Beds</span>
                  <span class="text-blue-400 font-mono text-lg font-bold">{{ form.kamar_tidur }}</span>
                </label>
                <input v-model="form.kamar_tidur" type="range" min="1" max="10" step="1" class="custom-slider w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer">
              </div>
              <div class="space-y-3">
                <label class="flex justify-between items-center text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                  <span>Baths</span>
                  <span class="text-blue-400 font-mono text-lg font-bold">{{ form.kamar_mandi }}</span>
                </label>
                <input v-model="form.kamar_mandi" type="range" min="1" max="10" step="1" class="custom-slider w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer">
              </div>
            </div>

            <div class="space-y-3 pt-2">
              <label class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Strategic Tier</label>
              <div class="relative">
                <select v-model="form.lokasi_skor" class="w-full rounded-xl border border-slate-600 bg-slate-800/50 px-4 py-3 text-white appearance-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all cursor-pointer">
                  <option value="1">Tier 1 • Outskirts / Rural</option>
                  <option value="2">Tier 2 • Urban Residential</option>
                  <option value="3">Tier 3 • Central Business District</option>
                </select>
                <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-400">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </div>
              </div>
            </div>
            
          </form>
        </section>

        <section class="lg:col-span-8 space-y-6">
          
          <div class="relative bg-gradient-to-br from-blue-900 to-[#0f172a] rounded-2xl border border-blue-500/20 shadow-2xl p-8 sm:p-10 overflow-hidden group transition-all duration-300">
            <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjEiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wNSkiLz48L3N2Zz4=')] [mask-image:linear-gradient(to_bottom,white,transparent)]"></div>
            
            <div class="relative z-10 flex flex-col h-full justify-between">
              <div>
                <div class="flex items-center gap-2 mb-2">
                  <span class="h-px w-6 bg-blue-500 transition-all duration-300" :class="{'w-12 bg-emerald-400': isLoading}"></span>
                  <p class="text-blue-400 text-xs font-bold uppercase tracking-[0.2em] transition-colors" :class="{'text-emerald-400': isLoading}">
                    {{ isLoading ? 'Calculating...' : 'Predicted Asset Value' }}
                  </p>
                </div>
                
                <h3 class="text-5xl sm:text-6xl lg:text-7xl font-black text-white tracking-tighter mt-4 flex items-baseline gap-2 transition-all duration-300" :class="{'opacity-50 blur-[2px] scale-[0.98]': isLoading}">
                  <span class="bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                    {{ formatRupiah(predictionResult) }}
                  </span>
                </h3>
              </div>

              <div class="mt-8 flex items-center justify-between border-t border-slate-700/50 pt-6">
                <p class="text-xs text-slate-400 font-mono tracking-wide">
                  MODEL: <span class="text-blue-400">RANDOM_FOREST_REGRESSOR</span>
                </p>
                <div class="w-12 h-12 rounded-full border border-slate-700 flex items-center justify-center bg-[#0f172a]" :class="{'animate-pulse border-blue-500': isLoading}">
                  <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-[#1e293b] rounded-2xl border border-slate-700/50 p-6 shadow-xl">
            <div class="flex justify-between items-end mb-6">
              <div>
                <h3 class="text-sm font-bold text-white uppercase tracking-wider mb-1">Explainable AI (XAI)</h3>
                <p class="text-[11px] text-slate-400">Algorithmic feature importance distribution</p>
              </div>
            </div>
            <div class="h-[260px] w-full">
              <canvas id="importanceChart"></canvas>
            </div>
          </div>

        </section>
      </div>
    </main>

    <footer class="border-t border-slate-800 bg-[#0f172a] py-8 mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-2">
          <span class="text-xl font-bold tracking-tight text-white italic uppercase">Acreage<span class="text-blue-500">.</span></span>
          <span class="px-2 py-0.5 rounded-md bg-slate-800 text-[10px] font-mono text-slate-400 border border-slate-700">v2.1.0</span>
        </div>
        <div class="text-center md:text-right">
          <p class="text-[11px] font-medium text-slate-400 tracking-widest uppercase">
            &copy; 2026 Engineered by <span class="text-blue-400 font-bold">Samuel</span>
          </p>
          <p class="text-[10px] text-slate-600 mt-1 font-mono">
            STACK: VUE 3 / FASTAPI / SCIKIT-LEARN
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Custom Styling untuk Slider */
.custom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6; 
  cursor: pointer;
  border: 2px solid #0f172a;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
  transition: transform 0.1s ease-in-out;
}
.custom-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #0f172a;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
  transition: transform 0.1s ease-in-out;
}
.custom-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}
.custom-slider::-moz-range-thumb:hover {
  transform: scale(1.2);
}

/* Menghilangkan panah pada input number */
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none; 
  margin: 0; 
}
input[type=number] {
  -moz-appearance: textfield;
}
</style>