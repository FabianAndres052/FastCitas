<template>
  <div class="pagina-bienvenida" :class="{ saliendo }">

    <!-- Fondo con grid animado -->
    <div class="fondo-grid"></div>
    <div class="fondo-gradiente"></div>

    <!-- Fase 1: Problema -->
    <Transition name="fase">
      <div class="fase centrada" v-if="faseActual === 1" key="f1">
        <div class="chip chip-rojo">
          <span class="punto-parpadeante"></span>
          Problema real · Colombia
        </div>
        <h1 class="titulo-gigante">
          <span class="linea-gris">Son las</span>
          <span class="linea-blanca">4:00 AM</span>
        </h1>
        <p class="parrafo-central">Cientos de pacientes hacen fila bajo la lluvia por un turno que se agota en 10 minutos.</p>
        <div class="lista-problemas">
          <div class="item-problema" v-for="(p, i) in problemas" :key="i" :style="{ animationDelay: i * 180 + 'ms' }">
            <span class="icono-x">✕</span>{{ p }}
          </div>
        </div>
      </div>
    </Transition>

    <!-- Fase 2: Transición -->
    <Transition name="fase">
      <div class="fase centrada" v-if="faseActual === 2" key="f2">
        <div class="orbita">
          <div class="circulo-centro">
            <i class="pi pi-bolt"></i>
          </div>
          <div class="anillo anillo-1"></div>
          <div class="anillo anillo-2"></div>
        </div>
        <h2 class="titulo-transicion">Existe una mejor manera.</h2>
        <p class="parrafo-central">¿Y si pudieras agendar desde casa, en segundos?</p>
      </div>
    </Transition>

    <!-- Fase 3: Solución -->
    <Transition name="fase">
      <div class="fase centrada" v-if="faseActual === 3" key="f3">
        <div class="logo-marca">
          <div class="logo-icono">
            <i class="pi pi-calendar-plus"></i>
          </div>
          <span class="logo-texto">FastCitas</span>
        </div>
        <p class="parrafo-central">Agendamiento médico digital para centros de salud pública de Colombia.</p>
        <div class="lista-soluciones">
          <div class="item-solucion" v-for="(s, i) in soluciones" :key="i" :style="{ animationDelay: i * 150 + 'ms' }">
            <span class="icono-check">✓</span>{{ s }}
          </div>
        </div>
        <div class="progreso-wrap">
          <div class="barra-prog">
            <div class="barra-fill" :style="{ width: progreso + '%' }"></div>
          </div>
          <span class="texto-prog">{{ Math.round(progreso) }}%</span>
        </div>
      </div>
    </Transition>

    <!-- Indicadores de fase -->
    <div class="indicadores">
      <span class="dot" :class="{ activo: faseActual === 1 }"></span>
      <span class="dot" :class="{ activo: faseActual === 2 }"></span>
      <span class="dot" :class="{ activo: faseActual === 3 }"></span>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const enrutador = useRouter()
const faseActual = ref(1)
const saliendo = ref(false)
const progreso = ref(0)

const problemas = [
  'Filas desde las 4AM bajo la lluvia',
  'Turnos agotados en menos de 10 minutos',
  'Sin historial médico digital',
  'Horas perdidas sin atención garantizada',
]

const soluciones = [
  'Agenda en 30 segundos desde tu celular',
  'Disponible 24/7, sin filas ni madrugadas',
  'Historial completo de tus citas',
  'Notificaciones y gestión en tiempo real',
]

onMounted(() => {
  setTimeout(() => { faseActual.value = 2 }, 3200)
  setTimeout(() => { faseActual.value = 3 }, 5400)
  setTimeout(() => {
    let p = 0
    const iv = setInterval(() => {
      p += 1.8
      progreso.value = Math.min(p, 100)
      if (p >= 100) {
        clearInterval(iv)
        saliendo.value = true
        setTimeout(() => enrutador.push('/login'), 500)
      }
    }, 35)
  }, 5700)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }

.pagina-bienvenida {
  min-height: 100vh;
  background: #080c14;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
  transition: opacity 0.5s ease;
}

.pagina-bienvenida.saliendo { opacity: 0; transform: scale(0.98); transition: opacity 0.5s, transform 0.5s; }

/* FONDO */
.fondo-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(56,139,253,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,139,253,0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
}

.fondo-gradiente {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 60% 60% at 50% 50%, rgba(56,139,253,0.06) 0%, transparent 70%);
  pointer-events: none;
}

/* FASE */
.fase {
  position: absolute;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.centrada {
  flex-direction: column;
  gap: 1.8rem;
  text-align: center;
  max-width: 580px;
  margin: 0 auto;
}

/* CHIP */
.chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.35rem 0.9rem;
  border-radius: 99px;
}

.chip-rojo {
  background: rgba(248,81,73,0.08);
  border: 1px solid rgba(248,81,73,0.25);
  color: #f85149;
}

.punto-parpadeante {
  width: 6px;
  height: 6px;
  background: #f85149;
  border-radius: 50%;
  animation: parpadear 1.2s ease infinite;
}

@keyframes parpadear {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.2; }
}

/* TÍTULOS */
.titulo-gigante {
  display: flex;
  flex-direction: column;
  line-height: 1.05;
  gap: 0.1rem;
}

.linea-gris {
  font-size: 2.4rem;
  font-weight: 300;
  color: #484f58;
}

.linea-blanca {
  font-size: 5rem;
  font-weight: 700;
  color: #e6edf3;
  letter-spacing: -3px;
}

.titulo-transicion {
  font-size: 2.8rem;
  font-weight: 700;
  color: #e6edf3;
  letter-spacing: -1.5px;
}

.parrafo-central {
  font-size: 1rem;
  color: #8b949e;
  line-height: 1.65;
  font-weight: 400;
  max-width: 440px;
}

/* LISTAS */
.lista-problemas, .lista-soluciones {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  width: 100%;
  max-width: 420px;
}

.item-problema, .item-solucion {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.65rem 1rem;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #cdd9e5;
  animation: entrar 0.4s ease both;
  text-align: left;
}

.item-problema {
  background: rgba(248,81,73,0.05);
  border: 1px solid rgba(248,81,73,0.12);
}

.item-solucion {
  background: rgba(63,185,80,0.05);
  border: 1px solid rgba(63,185,80,0.12);
}

.icono-x { color: #f85149; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; }
.icono-check { color: #3fb950; font-size: 0.85rem; font-weight: 700; flex-shrink: 0; }

@keyframes entrar {
  from { opacity: 0; transform: translateX(-16px); }
  to { opacity: 1; transform: translateX(0); }
}

/* ÓRBITA */
.orbita {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.circulo-centro {
  width: 64px;
  height: 64px;
  background: rgba(56,139,253,0.1);
  border: 1px solid rgba(56,139,253,0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.circulo-centro i { font-size: 1.6rem; color: #388bfd; }

.anillo {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(56,139,253,0.15);
  animation: girar 4s linear infinite;
}

.anillo-1 { width: 90px; height: 90px; animation-duration: 3.5s; }
.anillo-2 { width: 120px; height: 120px; animation-duration: 6s; animation-direction: reverse; }

@keyframes girar {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* LOGO */
.logo-marca {
  display: flex;
  align-items: center;
  gap: 0.9rem;
}

.logo-icono {
  width: 52px;
  height: 52px;
  background: rgba(56,139,253,0.1);
  border: 1px solid rgba(56,139,253,0.25);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icono i { font-size: 1.5rem; color: #388bfd; }

.logo-texto {
  font-size: 2.2rem;
  font-weight: 700;
  color: #e6edf3;
  letter-spacing: -1px;
}

/* PROGRESO */
.progreso-wrap {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  width: 100%;
  max-width: 320px;
}

.barra-prog {
  flex: 1;
  height: 2px;
  background: #21262d;
  border-radius: 99px;
  overflow: hidden;
}

.barra-fill {
  height: 100%;
  background: linear-gradient(90deg, #388bfd, #a371f7);
  border-radius: 99px;
  transition: width 0.035s linear;
}

.texto-prog {
  font-size: 0.72rem;
  color: #484f58;
  font-weight: 500;
  min-width: 30px;
  text-align: right;
}

/* INDICADORES */
.indicadores {
  position: absolute;
  bottom: 2.5rem;
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #21262d;
  transition: background 0.3s, transform 0.3s;
}

.dot.activo {
  background: #388bfd;
  transform: scale(1.4);
}

/* TRANSICIONES ENTRE FASES */
.fase-enter-active { transition: opacity 0.6s ease, transform 0.6s ease; }
.fase-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.fase-enter-from { opacity: 0; transform: translateY(24px); }
.fase-leave-to { opacity: 0; transform: translateY(-16px); }
</style>