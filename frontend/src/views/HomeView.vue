<template>
  <div class="pagina-inicio">

    <!-- NAVBAR -->
    <nav class="navbar">
      <div class="nav-logo">
        <svg viewBox="0 0 80 80" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
          <polygon points="40,2 76,21 76,59 40,78 4,59 4,21" fill="none" stroke="#1a2744" stroke-width="1"/>
          <rect x="29" y="14" width="22" height="52" rx="7" fill="#1a3a6e"/>
          <rect x="14" y="29" width="52" height="22" rx="7" fill="#1a3a6e"/>
          <rect x="31" y="16" width="18" height="48" rx="6" fill="#388bfd"/>
          <rect x="16" y="31" width="48" height="18" rx="6" fill="#388bfd"/>
          <rect x="31" y="31" width="18" height="18" rx="4" fill="#60a5fa"/>
          <polyline class="pulso-linea" points="4,40 14,40 20,26 28,54 32,40"
            fill="none" stroke="#388bfd" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <polyline class="pulso-linea pulso-delay" points="48,40 52,26 60,54 66,40 76,40"
            fill="none" stroke="#388bfd" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="nav-nombre">FastCitas</span>
      </div>
      <div class="nav-derecha">
        <div class="nav-usuario">
          <div class="avatar">{{ usuario.nombre?.charAt(0).toUpperCase() }}</div>
          <span class="nav-saludo">{{ usuario.nombre }}</span>
        </div>
        <button class="boton-salir" @click="cerrarSesion">
          <i class="pi pi-sign-out"></i> Salir
        </button>
      </div>
    </nav>

    <!-- CARRUSEL -->
    <div class="carrusel-wrapper">
      <div class="carrusel-track">
        <span v-for="(item, i) in carruselItems.concat(carruselItems)" :key="i" class="carrusel-item">
          <i :class="item.icono"></i> {{ item.texto }}
        </span>
      </div>
    </div>

    <!-- HERO BANNER -->
    <div class="hero-banner">
      <div class="hero-izq">
        <div class="hero-saludo-fila">
          <span class="hero-saludo-texto">{{ saludo }},</span>
          <span class="hero-nombre-texto">{{ usuario.nombre?.split(' ')[0] }}</span>
          <span class="hero-punto">.</span>
        </div>
        <p class="hero-sub">{{ fraseDelDia }}</p>
        <div class="hero-chips">
          <span class="hero-chip"><i class="pi pi-map-marker"></i> Colombia</span>
          <span class="hero-chip"><i class="pi pi-shield"></i> Cuenta verificada</span>
          <span class="hero-chip chip-verde"><i class="pi pi-circle-fill"></i> Sistema activo</span>
        </div>
      </div>
      <div class="hero-der">
        <div class="reloj-bloque">
          <p class="reloj-hora">{{ horaActual }}</p>
          <p class="reloj-fecha">{{ fechaActual }}</p>
        </div>
        <div class="hero-stat-mini">
          <div class="mini-stat">
            <i class="pi pi-users"></i>
            <span>{{ doctores.length }} médicos</span>
          </div>
          <div class="mini-stat">
            <i class="pi pi-calendar-check"></i>
            <span>{{ citas.length }} citas tuyas</span>
          </div>
        </div>
      </div>
    </div>

    <div class="contenido">

      <!-- STATS RÁPIDAS -->
      <div class="grid-stats">
        <div class="stat-card" v-for="s in statsUsuario" :key="s.label">
          <div class="stat-icono" :style="{ background: s.bg, borderColor: s.borde }">
            <i :class="['pi', s.icono]" :style="{ color: s.color }"></i>
          </div>
          <div>
            <p class="stat-num">{{ s.valor }}</p>
            <p class="stat-label">{{ s.label }}</p>
          </div>
        </div>
      </div>

      <!-- DOCTORES DISPONIBLES -->
      <div class="seccion-card">
        <div class="card-cabeza">
          <i class="pi pi-users cabeza-icono"></i>
          <div>
            <h2 class="card-titulo">Nuestros médicos</h2>
            <p class="card-sub">Selecciona un doctor para agendar tu cita</p>
          </div>
        </div>

        <div v-if="cargandoDoctores" class="doctores-grid">
          <div class="skeleton-doctor" v-for="n in 4" :key="n">
            <Skeleton height="120px" borderRadius="12px" />
          </div>
        </div>

        <div v-else class="doctores-grid">
          <div
            v-for="doc in doctores"
            :key="doc.id"
            class="doctor-card"
            :class="{ seleccionado: doctorSeleccionado?.id === doc.id }"
            @click="seleccionarDoctor(doc)"
          >
            <div class="doctor-avatar" :style="{ background: colorAvatar(doc.especialidad) }">
              {{ doc.foto_iniciales }}
            </div>
            <div class="doctor-info">
              <p class="doctor-nombre">{{ doc.nombre }}</p>
              <p class="doctor-especialidad">{{ doc.especialidad }}</p>
              <p class="doctor-contacto"><i class="pi pi-phone"></i> {{ doc.telefono }}</p>
            </div>
            <div class="doctor-check" v-if="doctorSeleccionado?.id === doc.id">
              <i class="pi pi-check-circle"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- AGENDAR CITA -->
      <Transition name="deslizar">
        <div class="seccion-card" v-if="doctorSeleccionado">
          <div class="card-cabeza">
            <i class="pi pi-calendar-plus cabeza-icono"></i>
            <div>
              <h2 class="card-titulo">Agendar con {{ doctorSeleccionado.nombre }}</h2>
              <p class="card-sub">{{ doctorSeleccionado.especialidad }}</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="campo">
              <label>Fecha</label>
              <input
                type="date"
                v-model="nuevaCita.fecha"
                class="inp-fecha"
                :disabled="cargando"
                :min="hoy"
                @change="cargarHorarios"
              />
            </div>

            <div class="campo">
              <label>Hora disponible</label>
              <div v-if="!nuevaCita.fecha" class="hint-fecha">
                <i class="pi pi-info-circle"></i> Selecciona primero una fecha
              </div>
              <div v-else-if="cargandoHorarios" class="hint-fecha">
                <i class="pi pi-spin pi-spinner"></i> Cargando horarios...
              </div>
              <div v-else class="horarios-grid">
                <button
                  v-for="h in horariosDisponibles"
                  :key="h"
                  class="btn-hora disponible"
                  :class="{ activo: nuevaCita.hora === h }"
                  @click="nuevaCita.hora = h"
                >{{ h }}</button>
                <button
                  v-for="h in horariosOcupados"
                  :key="h"
                  class="btn-hora ocupado"
                  disabled
                >{{ h }}</button>
              </div>
            </div>
          </div>

          <button class="boton-agendar" @click="agendarCita" :disabled="cargando || !nuevaCita.fecha || !nuevaCita.hora">
            <span v-if="!cargando" class="boton-contenido">
              Confirmar cita <i class="pi pi-check icono-boton"></i>
            </span>
            <span v-else class="boton-contenido">
              <i class="pi pi-spin pi-spinner"></i> Agendando...
            </span>
            <span class="boton-brillo"></span>
          </button>
        </div>
      </Transition>

      <!-- MIS CITAS -->
      <div class="seccion-card">
        <div class="card-cabeza">
          <i class="pi pi-list cabeza-icono"></i>
          <div>
            <h2 class="card-titulo">Mis citas</h2>
            <p class="card-sub">Historial y estado de tus citas médicas</p>
          </div>
        </div>

        <div v-if="cargandoCitas" class="lista-skeleton">
          <Skeleton height="3.5rem" borderRadius="10px" v-for="n in 3" :key="n" />
        </div>

        <div v-else-if="citas.length === 0" class="sin-citas">
          <div class="sin-citas-icono"><i class="pi pi-calendar"></i></div>
          <p class="sin-citas-titulo">Sin citas agendadas</p>
          <p class="sin-citas-sub">Selecciona un médico arriba para agendar tu primera cita</p>
        </div>

        <div v-else class="citas-lista">
          <TransitionGroup name="lista">
            <div class="cita-fila" v-for="c in citas" :key="c.id">
              <div class="cita-avatar" :style="{ background: colorAvatar(c.especialidad) }">
                {{ c.doctor_iniciales }}
              </div>
              <div class="cita-info">
                <p class="cita-doctor">{{ c.doctor_nombre }}</p>
                <p class="cita-detalle">{{ c.especialidad }} · {{ c.fecha }} · {{ c.hora }}</p>
              </div>
              <span :class="['badge-estado', `estado-${c.estado}`]">{{ c.estado }}</span>
              <button
                class="boton-cancelar"
                @click="cancelarCita(c.id)"
                v-if="c.estado !== 'cancelada'"
                :disabled="cargando"
                title="Cancelar cita"
              >
                <i class="pi pi-trash"></i>
              </button>
            </div>
          </TransitionGroup>
        </div>
      </div>

    </div>
    <Toast />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import axios from 'axios'

const enrutador = useRouter()
const notificacion = useToast()
const usuario = ref(JSON.parse(localStorage.getItem('usuario') || '{}'))
const citas = ref([])
const doctores = ref([])
const doctorSeleccionado = ref(null)
const horariosDisponibles = ref([])
const horariosOcupados = ref([])
const cargando = ref(false)
const cargandoCitas = ref(false)
const cargandoDoctores = ref(false)
const cargandoHorarios = ref(false)
const hoy = new Date().toISOString().split('T')[0]
const nuevaCita = ref({ fecha: '', hora: '' })
const horaActual = ref('')
const fechaActual = ref('')
let intervaloReloj = null

const saludo = computed(() => {
  const h = new Date().getHours()
  if (h >= 5 && h < 12) return 'Buenos días'
  if (h >= 12 && h < 18) return 'Buenas tardes'
  return 'Buenas noches'
})

const fraseDelDia = computed(() => {
  const frases = [
    'Tu salud es tu mayor inversión. Agenda hoy.',
    'Prevenir es mejor que curar. Estamos aquí para ti.',
    'Un chequeo a tiempo puede cambiar todo.',
    'Cuídate hoy para estar bien mañana.',
    'Tu bienestar es nuestra prioridad.',
    'La salud no se improvisa, se agenda.',
    'Cada cita es un paso hacia una vida mejor.',
  ]
  return frases[new Date().getDay() % frases.length]
})

const actualizarReloj = () => {
  const ahora = new Date()
  horaActual.value = ahora.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  fechaActual.value = ahora.toLocaleDateString('es-CO', { weekday: 'long', day: 'numeric', month: 'long' })
}

const carruselItems = ref([
  { icono: 'pi pi-heart', texto: 'Medicina General' },
  { icono: 'pi pi-star', texto: 'Pediatría' },
  { icono: 'pi pi-heart-fill', texto: 'Cardiología' },
  { icono: 'pi pi-eye', texto: 'Oftalmología' },
  { icono: 'pi pi-user', texto: 'Dermatología' },
  { icono: 'pi pi-verified', texto: 'Ginecología' },
  { icono: 'pi pi-shield', texto: 'Odontología' },
  { icono: 'pi pi-plus', texto: 'Neurología' },
  { icono: 'pi pi-clock', texto: 'Disponible 24/7' },
  { icono: 'pi pi-calendar-check', texto: 'Agenda en 30 segundos' },
  { icono: 'pi pi-map-marker', texto: 'Centros de salud Colombia' },
  { icono: 'pi pi-mobile', texto: 'Desde tu celular' },
])

const coloresEspecialidad = {
  'Medicina General': '#1a3a6e',
  'Pediatría': '#1a4a3a',
  'Cardiología': '#4a1a1a',
  'Dermatología': '#3a2a1a',
  'Neurología': '#2a1a4a',
  'Ginecología': '#3a1a3a',
  'Oftalmología': '#1a3a4a',
  'Odontología': '#2a3a1a',
}

const colorAvatar = (especialidad) => coloresEspecialidad[especialidad] || '#1a3a6e'

const statsUsuario = computed(() => [
  { label: 'Total citas', valor: citas.value.length, icono: 'pi-calendar', color: '#388bfd', bg: 'rgba(56,139,253,0.08)', borde: 'rgba(56,139,253,0.2)' },
  { label: 'Pendientes', valor: citas.value.filter(c => c.estado === 'pendiente').length, icono: 'pi-clock', color: '#fbbf24', bg: 'rgba(251,191,36,0.08)', borde: 'rgba(251,191,36,0.2)' },
  { label: 'Confirmadas', valor: citas.value.filter(c => c.estado === 'confirmada').length, icono: 'pi-check-circle', color: '#3fb950', bg: 'rgba(63,185,80,0.08)', borde: 'rgba(63,185,80,0.2)' },
  { label: 'Canceladas', valor: citas.value.filter(c => c.estado === 'cancelada').length, icono: 'pi-times-circle', color: '#f85149', bg: 'rgba(248,81,73,0.08)', borde: 'rgba(248,81,73,0.2)' },
])

const obtenerDoctores = async () => {
  cargandoDoctores.value = true
  try {
    const res = await axios.get('/doctores/')
    doctores.value = res.data
  } catch {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los doctores', life: 3000 })
  } finally {
    cargandoDoctores.value = false
  }
}

const seleccionarDoctor = (doc) => {
  if (doctorSeleccionado.value?.id === doc.id) {
    doctorSeleccionado.value = null
    nuevaCita.value = { fecha: '', hora: '' }
    horariosDisponibles.value = []
    horariosOcupados.value = []
  } else {
    doctorSeleccionado.value = doc
    nuevaCita.value = { fecha: '', hora: '' }
    horariosDisponibles.value = []
    horariosOcupados.value = []
  }
}

const cargarHorarios = async () => {
  if (!doctorSeleccionado.value || !nuevaCita.value.fecha) return
  cargandoHorarios.value = true
  nuevaCita.value.hora = ''
  try {
    const res = await axios.get(`/doctores/${doctorSeleccionado.value.id}/horarios?fecha=${nuevaCita.value.fecha}`)
    horariosDisponibles.value = res.data.disponibles
    horariosOcupados.value = res.data.ocupados
  } catch {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los horarios', life: 3000 })
  } finally {
    cargandoHorarios.value = false
  }
}

const obtenerCitas = async () => {
  cargandoCitas.value = true
  try {
    const res = await axios.get(`/citas/paciente/${usuario.value.id}`)
    citas.value = res.data
  } catch {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las citas', life: 3000 })
  } finally {
    cargandoCitas.value = false
  }
}

const agendarCita = async () => {
  if (!nuevaCita.value.fecha || !nuevaCita.value.hora) return
  cargando.value = true
  try {
    await axios.post('/citas/', {
      paciente_id: usuario.value.id,
      doctor_id: doctorSeleccionado.value.id,
      especialidad: doctorSeleccionado.value.especialidad,
      fecha: nuevaCita.value.fecha,
      hora: nuevaCita.value.hora
    })
    notificacion.add({ severity: 'success', summary: '¡Cita agendada!', detail: `${doctorSeleccionado.value.nombre} — ${nuevaCita.value.fecha} ${nuevaCita.value.hora}`, life: 3000 })
    nuevaCita.value = { fecha: '', hora: '' }
    doctorSeleccionado.value = null
    horariosDisponibles.value = []
    await obtenerCitas()
  } catch (e) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: e.response?.data?.detail || 'No se pudo agendar', life: 3000 })
  } finally {
    cargando.value = false
  }
}

const cancelarCita = async (idCita) => {
  cargando.value = true
  try {
    await axios.delete(`/citas/${idCita}`)
    notificacion.add({ severity: 'info', summary: 'Cita cancelada', detail: 'La cita fue eliminada correctamente', life: 3000 })
    await obtenerCitas()
  } catch {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo cancelar la cita', life: 3000 })
  } finally {
    cargando.value = false
  }
}

const cerrarSesion = () => {
  localStorage.removeItem('usuario')
  enrutador.push('/login')
}

onMounted(() => {
  obtenerDoctores()
  obtenerCitas()
  actualizarReloj()
  intervaloReloj = setInterval(actualizarReloj, 1000)
})

onUnmounted(() => {
  clearInterval(intervaloReloj)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }

.pagina-inicio { min-height: 100vh; background: #080c14; color: #e6edf3; }

/* NAVBAR */
.navbar {
  background: #0d1117; border-bottom: 1px solid #21262d;
  padding: 0.9rem 2rem; display: flex; justify-content: space-between; align-items: center;
  position: sticky; top: 0; z-index: 10;
}
.nav-logo { display: flex; align-items: center; gap: 0.7rem; }
.nav-nombre { font-size: 1.1rem; font-weight: 700; color: #e6edf3; letter-spacing: -0.5px; }
.nav-derecha { display: flex; align-items: center; gap: 1rem; }
.nav-usuario { display: flex; align-items: center; gap: 0.6rem; }
.avatar {
  width: 32px; height: 32px; background: #1a3a6e; border: 1px solid #2d5fa8;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; font-weight: 700; color: #60a5fa;
}
.nav-saludo { font-size: 0.85rem; color: #8b949e; }
.boton-salir {
  display: flex; align-items: center; gap: 0.4rem; padding: 0.4rem 0.9rem;
  background: transparent; border: 1px solid #21262d; border-radius: 8px; color: #8b949e;
  font-size: 0.8rem; font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.2s;
}
.boton-salir:hover { border-color: #f85149; color: #f85149; background: rgba(248,81,73,0.05); }

/* PULSO */
.pulso-linea { stroke-dasharray: 80; stroke-dashoffset: 80; animation: dibujarPulso 2s ease-in-out infinite; }
.pulso-delay { animation-delay: 0.4s; }
@keyframes dibujarPulso {
  0%   { stroke-dashoffset: 80; opacity: 0; }
  10%  { opacity: 1; }
  50%  { stroke-dashoffset: 0; opacity: 1; }
  80%  { stroke-dashoffset: 0; opacity: 0.3; }
  100% { stroke-dashoffset: 80; opacity: 0; }
}

/* CARRUSEL */
.carrusel-wrapper { width: 100%; background: #0d1117; border-bottom: 1px solid #161b22; padding: 0.55rem 0; overflow: hidden; }
.carrusel-track { display: flex; gap: 3rem; animation: deslizar 32s linear infinite; width: max-content; }
.carrusel-item { display: flex; align-items: center; gap: 0.45rem; color: #30363d; font-size: 0.75rem; font-weight: 500; letter-spacing: 0.04em; white-space: nowrap; }
.carrusel-item i { color: #1d4ed8; font-size: 0.7rem; }
@keyframes deslizar { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

/* HERO BANNER */
.hero-banner {
  max-width: 900px; margin: 1.8rem auto 0;
  padding: 0 1.5rem;
  display: flex; justify-content: space-between; align-items: center; gap: 1.5rem;
}
.hero-izq { flex: 1; }
.hero-saludo-fila {
  display: flex; align-items: baseline; gap: 0.4rem;
  flex-wrap: wrap; margin-bottom: 0.5rem;
}
.hero-saludo-texto { font-size: 1.6rem; font-weight: 300; color: #8b949e; letter-spacing: -0.5px; }
.hero-nombre-texto { font-size: 1.6rem; font-weight: 700; color: #e6edf3; letter-spacing: -0.5px; }
.hero-punto { font-size: 1.6rem; font-weight: 700; color: #388bfd; }
.hero-sub { font-size: 0.82rem; color: #484f58; margin-bottom: 1rem; font-style: italic; }
.hero-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.hero-chip {
  display: flex; align-items: center; gap: 0.35rem;
  padding: 0.25rem 0.7rem; background: #0d1117; border: 1px solid #21262d;
  border-radius: 99px; font-size: 0.7rem; color: #484f58;
}
.hero-chip i { font-size: 0.65rem; }
.chip-verde { border-color: rgba(63,185,80,0.2); color: #3fb950; }
.chip-verde i { color: #3fb950; font-size: 0.5rem; }
.hero-der { display: flex; flex-direction: column; align-items: flex-end; gap: 0.8rem; flex-shrink: 0; }
.reloj-bloque { text-align: right; }
.reloj-hora { font-size: 2rem; font-weight: 700; color: #e6edf3; letter-spacing: -1px; line-height: 1; font-variant-numeric: tabular-nums; }
.reloj-fecha { font-size: 0.72rem; color: #484f58; text-transform: capitalize; margin-top: 0.2rem; }
.hero-stat-mini { display: flex; gap: 0.7rem; }
.mini-stat {
  display: flex; align-items: center; gap: 0.35rem;
  padding: 0.3rem 0.7rem; background: rgba(56,139,253,0.06);
  border: 1px solid rgba(56,139,253,0.12); border-radius: 8px;
  font-size: 0.72rem; color: #388bfd;
}
.mini-stat i { font-size: 0.75rem; }

/* CONTENIDO */
.contenido { max-width: 900px; margin: 0 auto; padding: 1.5rem 1.5rem 2rem; display: flex; flex-direction: column; gap: 1.5rem; }

/* STATS */
.grid-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.stat-card {
  background: #0d1117; border: 1px solid #21262d; border-radius: 14px;
  padding: 1.1rem; display: flex; align-items: center; gap: 0.9rem;
  transition: border-color 0.2s, transform 0.2s;
}
.stat-card:hover { border-color: #30363d; transform: translateY(-2px); }
.stat-icono { width: 40px; height: 40px; border: 1px solid; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.stat-num { font-size: 1.5rem; font-weight: 700; color: #e6edf3; line-height: 1; margin-bottom: 0.15rem; }
.stat-label { font-size: 0.72rem; color: #484f58; }

/* CARDS */
.seccion-card { background: #0d1117; border: 1px solid #21262d; border-radius: 16px; padding: 1.8rem; }
.card-cabeza { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1.2rem; border-bottom: 1px solid #161b22; }
.cabeza-icono { font-size: 1.3rem; color: #388bfd; background: rgba(56,139,253,0.08); border: 1px solid rgba(56,139,253,0.15); padding: 0.6rem; border-radius: 10px; }
.card-titulo { font-size: 1rem; font-weight: 600; color: #e6edf3; margin-bottom: 0.15rem; }
.card-sub { font-size: 0.78rem; color: #484f58; }

/* DOCTORES */
.doctores-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1rem; }
.doctor-card {
  background: #0a0f1a; border: 1px solid #21262d; border-radius: 12px;
  padding: 1.1rem; cursor: pointer; position: relative;
  transition: border-color 0.25s, transform 0.2s, background 0.2s;
  display: flex; flex-direction: column; align-items: center; gap: 0.7rem; text-align: center;
}
.doctor-card:hover { border-color: #388bfd; transform: translateY(-3px); background: #0d1420; }
.doctor-card.seleccionado { border-color: #388bfd; background: rgba(56,139,253,0.06); }
.doctor-avatar { width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; font-weight: 700; color: #e6edf3; border: 2px solid rgba(255,255,255,0.08); }
.doctor-nombre { font-size: 0.82rem; font-weight: 600; color: #e6edf3; }
.doctor-especialidad { font-size: 0.72rem; color: #388bfd; font-weight: 500; }
.doctor-contacto { font-size: 0.7rem; color: #484f58; display: flex; align-items: center; gap: 0.3rem; justify-content: center; }
.doctor-check { position: absolute; top: 0.6rem; right: 0.6rem; color: #388bfd; font-size: 1rem; animation: aparecer 0.2s ease; }
@keyframes aparecer { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }
.skeleton-doctor { border-radius: 12px; overflow: hidden; }

/* HORARIOS */
.form-grid { display: grid; grid-template-columns: 200px 1fr; gap: 1.5rem; margin-bottom: 1.2rem; align-items: start; }
.campo label { display: block; font-size: 0.78rem; font-weight: 500; color: #8b949e; margin-bottom: 0.45rem; }
.inp-fecha { width: 100%; padding: 0.55rem 0.8rem; background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; font-size: 0.85rem; font-family: 'Inter', sans-serif; cursor: pointer; transition: border-color 0.2s; }
.inp-fecha:hover, .inp-fecha:focus { border-color: #388bfd; outline: none; }
.inp-fecha::-webkit-calendar-picker-indicator { filter: invert(0.5); cursor: pointer; }
.hint-fecha { font-size: 0.78rem; color: #484f58; display: flex; align-items: center; gap: 0.4rem; padding: 0.7rem; background: #0a0f1a; border: 1px solid #21262d; border-radius: 8px; }
.horarios-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.btn-hora { padding: 0.35rem 0.7rem; border-radius: 7px; font-size: 0.75rem; font-weight: 600; font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.2s; border: 1px solid; }
.btn-hora.disponible { background: #0a0f1a; border-color: #21262d; color: #8b949e; }
.btn-hora.disponible:hover { border-color: #388bfd; color: #388bfd; background: rgba(56,139,253,0.06); }
.btn-hora.disponible.activo { background: #1a3a6e; border-color: #388bfd; color: #e6edf3; }
.btn-hora.ocupado { background: rgba(248,81,73,0.04); border-color: rgba(248,81,73,0.15); color: #30363d; cursor: not-allowed; text-decoration: line-through; }

/* BOTÓN AGENDAR */
.boton-agendar { position: relative; padding: 0.75rem 1.5rem; background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 10px; color: #e6edf3; font-size: 0.9rem; font-weight: 600; font-family: 'Inter', sans-serif; cursor: pointer; overflow: hidden; transition: all 0.25s; }
.boton-agendar:hover:not(:disabled) { background: #1d4ed8; border-color: #388bfd; transform: translateY(-2px); }
.boton-agendar:disabled { opacity: 0.3; cursor: not-allowed; }
.boton-contenido { display: flex; align-items: center; gap: 0.5rem; position: relative; z-index: 1; }
.boton-brillo { position: absolute; top: 0; left: -100%; width: 60%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent); transform: skewX(-20deg); transition: left 0.5s ease; pointer-events: none; }
.boton-agendar:hover .boton-brillo { left: 150%; }
.icono-boton { transition: transform 0.25s; }
.boton-agendar:hover .icono-boton { transform: translateX(4px); }

/* LISTA CITAS */
.citas-lista { display: flex; flex-direction: column; gap: 0.7rem; }
.cita-fila { display: flex; align-items: center; gap: 1rem; padding: 0.9rem 1rem; background: #0a0f1a; border: 1px solid #21262d; border-radius: 10px; transition: border-color 0.2s; }
.cita-fila:hover { border-color: #30363d; }
.cita-avatar { width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #e6edf3; }
.cita-info { flex: 1; }
.cita-doctor { font-size: 0.85rem; font-weight: 600; color: #e6edf3; }
.cita-detalle { font-size: 0.72rem; color: #484f58; margin-top: 0.1rem; }

/* BADGES */
.badge-estado { padding: 0.25rem 0.65rem; border-radius: 99px; font-size: 0.72rem; font-weight: 600; text-transform: capitalize; }
.estado-pendiente { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.25); color: #fbbf24; }
.estado-confirmada { background: rgba(63,185,80,0.1); border: 1px solid rgba(63,185,80,0.25); color: #3fb950; }
.estado-cancelada { background: rgba(248,81,73,0.1); border: 1px solid rgba(248,81,73,0.25); color: #f85149; }

.boton-cancelar { background: transparent; border: 1px solid #21262d; border-radius: 7px; color: #484f58; padding: 0.35rem 0.6rem; cursor: pointer; font-size: 0.8rem; transition: all 0.2s; flex-shrink: 0; }
.boton-cancelar:hover:not(:disabled) { border-color: #f85149; color: #f85149; background: rgba(248,81,73,0.05); }
.boton-cancelar:disabled { opacity: 0.3; cursor: not-allowed; }

/* SIN CITAS */
.sin-citas { text-align: center; padding: 3rem 1rem; display: flex; flex-direction: column; align-items: center; gap: 0.6rem; }
.sin-citas-icono { width: 56px; height: 56px; background: rgba(56,139,253,0.06); border: 1px solid rgba(56,139,253,0.12); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; color: #388bfd; margin-bottom: 0.5rem; }
.sin-citas-titulo { font-size: 0.95rem; font-weight: 600; color: #484f58; }
.sin-citas-sub { font-size: 0.78rem; color: #30363d; }
.lista-skeleton { display: flex; flex-direction: column; gap: 0.7rem; }

/* TRANSICIONES */
.deslizar-enter-active { transition: opacity 0.4s ease, transform 0.4s ease; }
.deslizar-enter-from { opacity: 0; transform: translateY(-16px); }
.lista-enter-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.lista-enter-from { opacity: 0; transform: translateX(-12px); }
.lista-leave-active { transition: opacity 0.2s; }
.lista-leave-to { opacity: 0; }

@media (max-width: 640px) {
  .grid-stats { grid-template-columns: repeat(2, 1fr); }
  .form-grid { grid-template-columns: 1fr; }
  .doctores-grid { grid-template-columns: repeat(2, 1fr); }
  .navbar { padding: 0.9rem 1rem; }
  .nav-saludo { display: none; }
  .hero-banner { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .hero-der { align-items: flex-start; }
  .reloj-hora { font-size: 1.5rem; }
}
</style>