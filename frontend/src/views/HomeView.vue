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
        <button class="btn-hamburguesa" @click="mostrarSidebar = true">
          <i class="pi pi-bars"></i>
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
          <span class="hero-nombre-texto">{{ nombreAMostrar }}</span>
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
          <div class="mini-stat" v-if="usuario.rol === 'doctor'">
            <i class="pi pi-calendar"></i>
            <span>{{ citasDoctor.length }} consultas</span>
          </div>
          <div class="mini-stat" v-else>
            <i class="pi pi-users"></i>
            <span>{{ doctores.length }} médicos</span>
          </div>
          <div class="mini-stat" v-if="usuario.rol !== 'doctor'">
            <i class="pi pi-calendar-check"></i>
            <span>{{ citas.length }} citas tuyas</span>
          </div>
        </div>
      </div>
    </div>

    <div class="contenido">

      <!-- VISTA DEL DOCTOR -->
      <div v-if="usuario.rol === 'doctor'" class="doctor-dashboard-cuerpo" style="display: flex; flex-direction: column; gap: 1.5rem; width: 100%;">
        
        <!-- STATS DOCTOR -->
        <div class="grid-stats">
          <div
            class="stat-card"
            v-for="s in statsDoctor"
            :key="s.label"
            :class="{ 'stat-activa': filtroEstado === s.filtro }"
            @click="filtroEstado = s.filtro"
          >
            <div class="stat-icono" :style="{ background: s.bg, borderColor: s.borde }">
              <i :class="['pi', s.icono]" :style="{ color: s.color }"></i>
            </div>
            <div>
              <p class="stat-num">{{ s.valor }}</p>
              <p class="stat-label">{{ s.label }}</p>
            </div>
          </div>
        </div>

        <!-- LISTADO DE SOLICITUDES PARA EL DOCTOR -->
        <div class="seccion-card">
          <div class="card-cabeza">
            <i class="pi pi-calendar cabeza-icono"></i>
            <div>
              <h2 class="card-titulo">Citas solicitadas por tus pacientes</h2>
              <p class="card-sub">Confirma o rechaza las citas que los pacientes agendaron contigo.</p>
            </div>
          </div>

          <!-- BANNER FILTRO ACTIVO -->
          <Transition name="deslizar">
            <div class="banner-filtro" v-if="filtroEstado !== ''">
              <div class="filtro-info">
                <i class="pi pi-filter"></i>
                <span>Mostrando citas en estado: <strong class="filtro-valor">{{ filtroEstado }}</strong></span>
              </div>
              <button class="btn-limpiar-filtro" @click="filtroEstado = ''">
                Limpiar filtro <i class="pi pi-times"></i>
              </button>
            </div>
          </Transition>

          <div v-if="cargandoCitasDoctor" class="sin-citas">
            <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: #388bfd;"></i>
            <p>Cargando solicitudes de citas...</p>
          </div>

          <div v-else-if="citasDoctor.length === 0" class="sin-citas">
            <div class="sin-citas-icono"><i class="pi pi-calendar-times"></i></div>
            <p class="sin-citas-titulo">Sin solicitudes de citas</p>
            <p class="sin-citas-sub">Cuando los pacientes soliciten citas médicas con tu perfil, aparecerán en esta sección.</p>
          </div>

          <div v-else-if="citasDoctorFiltradas.length === 0" class="sin-citas">
            <div class="sin-citas-icono"><i class="pi pi-filter-slash"></i></div>
            <p class="sin-citas-titulo">Sin citas encontradas</p>
            <p class="sin-citas-sub">No tienes citas con el estado seleccionado: <strong>{{ filtroEstado }}</strong></p>
          </div>

          <div v-else class="tabla-wrapper">
            <table class="tabla-admin">
              <thead>
                <tr>
                  <th>Paciente</th>
                  <th>Correo Electrónico</th>
                  <th>Especialidad</th>
                  <th>Fecha y Hora</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in citasDoctorFiltradas" :key="c.id">
                  <td><strong class="texto-blanco">{{ c.paciente_nombre }}</strong></td>
                  <td>{{ c.paciente_email }}</td>
                  <td><span class="badge-especialidad">{{ c.especialidad }}</span></td>
                  <td>{{ c.fecha }} a las {{ c.hora }}</td>
                  <td>
                    <span :class="['badge-estado', `estado-${c.estado}`]">{{ c.estado }}</span>
                  </td>
                  <td>
                    <div class="acciones-fila" v-if="c.estado === 'pendiente'">
                      <button 
                        class="btn-accion btn-confirmar" 
                        @click="cambiarEstadoCitaDoctor(c.id, 'confirmada')"
                        title="Aceptar Cita"
                      >
                        <i class="pi pi-check"></i> Aceptar
                      </button>
                      <button 
                        class="btn-accion btn-eliminar" 
                        @click="cambiarEstadoCitaDoctor(c.id, 'cancelada')"
                        title="Rechazar Cita"
                      >
                        <i class="pi pi-times"></i> Rechazar
                      </button>
                    </div>
                    <div v-else style="color: #484f58; font-size: 0.8rem; font-style: italic; padding-left: 0.5rem;">
                      Finalizada
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- VISTA DEL PACIENTE -->
      <div v-else class="paciente-dashboard-cuerpo" style="display: flex; flex-direction: column; gap: 1.5rem; width: 100%;">

        <!-- STATS RÁPIDAS -->
        <div class="grid-stats">
          <div
            class="stat-card"
            v-for="s in statsUsuario"
            :key="s.label"
            :class="{ 'stat-activa': filtroEstado === s.filtro }"
            @click="filtroEstado = s.filtro"
          >
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

          <!-- BANNER FILTRO ACTIVO -->
          <Transition name="deslizar">
            <div class="banner-filtro" v-if="filtroEstado">
              <div class="filtro-info">
                <i class="pi pi-filter"></i>
                <span>Mostrando citas en estado: <strong class="filtro-valor">{{ filtroEstado }}</strong></span>
              </div>
              <button class="btn-limpiar-filtro" @click="filtroEstado = ''">
                Limpiar filtro <i class="pi pi-times"></i>
              </button>
            </div>
          </Transition>

          <div v-if="cargandoCitas" class="lista-skeleton">
            <Skeleton height="3.5rem" borderRadius="10px" v-for="n in 3" :key="n" />
          </div>

          <div v-else-if="citas.length === 0" class="sin-citas">
            <div class="sin-citas-icono"><i class="pi pi-calendar"></i></div>
            <p class="sin-citas-titulo">Sin citas agendadas</p>
            <p class="sin-citas-sub">Selecciona un médico arriba para agendar tu primera cita</p>
          </div>

          <div v-else-if="citasFiltradas.length === 0" class="sin-citas">
            <div class="sin-citas-icono"><i class="pi pi-filter-slash"></i></div>
            <p class="sin-citas-titulo">Sin citas encontradas</p>
            <p class="sin-citas-sub">No tienes citas con el estado seleccionado: <strong>{{ filtroEstado }}</strong></p>
          </div>

          <div v-else class="citas-lista">
            <TransitionGroup name="lista">
              <div class="cita-fila" v-for="c in citasFiltradas" :key="c.id">
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

    </div>

    <!-- SIDEBAR DRAWER -->
    <Transition name="sidebar-fade">
      <div class="sidebar-overlay" v-if="mostrarSidebar" @click.self="mostrarSidebar = false">
        <div class="sidebar-caja">
          <div class="sidebar-header">
            <div class="sidebar-perfil">
              <div class="sidebar-avatar">{{ usuario.nombre?.charAt(0).toUpperCase() }}</div>
              <div>
                <p class="sidebar-nombre">{{ usuario.nombre }}</p>
                <p class="sidebar-rol">{{ usuario.rol === 'doctor' ? 'Médico' : usuario.rol === 'admin' ? 'Administrador' : 'Paciente' }}</p>
              </div>
            </div>
            <button class="sidebar-cerrar" @click="mostrarSidebar = false">
              <i class="pi pi-times"></i>
            </button>
          </div>

          <div class="sidebar-menu">
            <button class="menu-item" @click="abrirPerfil">
              <i class="pi pi-user"></i> Ver Perfil
            </button>
            <button class="menu-item" @click="abrirCambiarPassword">
              <i class="pi pi-lock"></i> Cambiar Contraseña
            </button>
            <button class="menu-item" @click="abrirAcercaDe">
              <i class="pi pi-info-circle"></i> Acerca de Nosotros
            </button>
            <hr class="menu-divisor" />
            <button class="menu-item menu-item-salir" @click="cerrarSesion">
              <i class="pi pi-sign-out"></i> Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- VER PERFIL MODAL -->
    <Transition name="modal-fade">
      <div class="modal-overlay" v-if="mostrarModalPerfil" @click.self="mostrarModalPerfil = false">
        <div class="modal-caja">
          <div class="modal-cabeza">
            <div class="modal-icono"><i class="pi pi-user"></i></div>
            <div style="flex:1">
              <p class="modal-titulo">Mi Perfil</p>
              <p class="modal-sub">Información de tu cuenta</p>
            </div>
            <button class="modal-cerrar" @click="mostrarModalPerfil = false"><i class="pi pi-times"></i></button>
          </div>
          <div class="perfil-datos">
            <div class="dato-grupo">
              <label>Nombre Completo</label>
              <p>{{ usuario.nombre }}</p>
            </div>
            <div class="dato-grupo">
              <label>Correo Electrónico</label>
              <p>{{ usuario.email }}</p>
            </div>
            <div class="dato-grupo">
              <label>Fecha de Nacimiento</label>
              <p>{{ usuario.fecha_nacimiento || 'No registrada' }}</p>
            </div>
            <div class="dato-grupo">
              <label>Rol de Cuenta</label>
              <p><span class="badge-rol">{{ usuario.rol }}</span></p>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- CAMBIAR CONTRASEÑA MODAL -->
    <Transition name="modal-fade">
      <div class="modal-overlay" v-if="mostrarModalPassword" @click.self="mostrarModalPassword = false">
        <div class="modal-caja">
          <div class="modal-cabeza">
            <div class="modal-icono"><i class="pi pi-lock"></i></div>
            <div style="flex:1">
              <p class="modal-titulo">Cambiar Contraseña</p>
              <p class="modal-sub">Escribe tu nueva contraseña</p>
            </div>
            <button class="modal-cerrar" @click="mostrarModalPassword = false"><i class="pi pi-times"></i></button>
          </div>
          <div class="campo">
            <label>Nueva Contraseña</label>
            <InputText v-model="nuevaContrasena" type="password" placeholder="Mínimo 6 caracteres" class="inp" :disabled="cargandoPassword" style="width: 100%;" />
          </div>
          <div class="campo" style="margin-top: 1rem;">
            <label>Confirmar Nueva Contraseña</label>
            <InputText v-model="confirmarContrasena" type="password" placeholder="Repite la contraseña" class="inp" :disabled="cargandoPassword" style="width: 100%;" />
          </div>
          <div class="modal-acciones" style="margin-top: 1.5rem;">
            <button class="btn-modal-cancelar" @click="mostrarModalPassword = false">Cancelar</button>
            <button class="btn-modal-ok" @click="actualizarPassword" :disabled="cargandoPassword">
              <span v-if="!cargandoPassword"><i class="pi pi-check"></i> Guardar</span>
              <span v-else><i class="pi pi-spin pi-spinner"></i> Guardando...</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ACERCA DE NOSOTROS MODAL -->
    <Transition name="modal-fade">
      <div class="modal-overlay" v-if="mostrarModalAcerca" @click.self="mostrarModalAcerca = false">
        <div class="modal-caja">
          <div class="modal-cabeza">
            <div class="modal-icono" style="width:60px;height:60px;">
              <svg viewBox="0 0 80 80" width="56" height="56" xmlns="http://www.w3.org/2000/svg">
                <polygon points="40,2 76,21 76,59 40,78 4,59 4,21" fill="none" stroke="#1a2744" stroke-width="1"/>
                <rect x="29" y="14" width="22" height="52" rx="7" fill="#1a3a6e"/>
                <rect x="14" y="29" width="48" height="22" rx="7" fill="#1a3a6e"/>
                <rect x="31" y="16" width="18" height="48" rx="6" fill="#388bfd"/>
                <rect x="16" y="31" width="48" height="18" rx="6" fill="#388bfd"/>
                <rect x="31" y="31" width="18" height="18" rx="4" fill="#60a5fa"/>
                <circle cx="40" cy="40" r="5" fill="none" stroke="#93c5fd" stroke-width="1.2" opacity="0.6"/>
                <circle cx="40" cy="40" r="2" fill="#bfdbfe"/>
                <polyline class="pulso-linea" points="4,40 14,40 20,26 28,54 32,40"
                  fill="none" stroke="#388bfd" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline class="pulso-linea pulso-delay" points="48,40 52,26 60,54 66,40 76,40"
                  fill="none" stroke="#388bfd" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div style="flex:1">
              <p class="modal-titulo">Acerca de Nosotros</p>
              <p class="modal-sub">Usuario: {{ usuario.nombre }}</p>
            </div>
            <button class="modal-cerrar" @click="mostrarModalAcerca = false"><i class="pi pi-times"></i></button>
          </div>
          <div class="acerca-cuerpo">
            <p><strong>FastCitas</strong> es la plataforma líder en agendamiento digital de citas médicas para centros de salud pública de Colombia, diseñada para erradicar las largas filas desde las 4:00 AM.</p>
            <p>Nuestra misión es hacer la salud pública accesible, digna y moderna para todos.</p>
            <hr class="divisor-acerca" />
            <p class="contacto-titulo"><strong>Contacto de Soporte</strong></p>
            <p class="contacto-item"><i class="pi pi-envelope"></i> soporte@fastcitas.com</p>
            <p class="contacto-item"><i class="pi pi-phone"></i> +57 3126245955</p>
            <p class="contacto-item"><i class="pi pi-map-marker"></i> Santa Marta, Colombia</p>
          </div>
        </div>
      </div>
    </Transition>

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
const filtroEstado = ref('')

const mostrarSidebar = ref(false)
const mostrarModalPerfil = ref(false)
const mostrarModalPassword = ref(false)
const mostrarModalAcerca = ref(false)

const nuevaContrasena = ref('')
const confirmarContrasena = ref('')
const cargandoPassword = ref(false)

// Doctor variables
const citasDoctor = ref([])
const cargandoCitasDoctor = ref(false)

const abrirPerfil = () => {
  mostrarSidebar.value = false
  mostrarModalPerfil.value = true
}

const abrirCambiarPassword = () => {
  mostrarSidebar.value = false
  mostrarModalPassword.value = true
}

const abrirAcercaDe = () => {
  mostrarSidebar.value = false
  mostrarModalAcerca.value = true
}

const actualizarPassword = async () => {
  if (!nuevaContrasena.value || nuevaContrasena.value.length < 6) {
    notificacion.add({ severity: 'warn', summary: 'Atención', detail: 'La contraseña debe tener al menos 6 caracteres', life: 3000 })
    return
  }
  if (nuevaContrasena.value !== confirmarContrasena.value) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'Las contraseñas no coinciden', life: 3000 })
    return
  }
  cargandoPassword.value = true
  try {
    await axios.put('/auth/cambiar-password', { email: usuario.value.email, nueva_password: nuevaContrasena.value })
    notificacion.add({ severity: 'success', summary: '¡Éxito!', detail: 'Contraseña actualizada correctamente', life: 2000 })
    nuevaContrasena.value = ''
    confirmarContrasena.value = ''
    mostrarModalPassword.value = false
  } catch (error) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'No se pudo cambiar la contraseña', life: 3000 })
  } finally {
    cargandoPassword.value = false
  }
}

const nombreAMostrar = computed(() => {
  const nombreComp = usuario.value.nombre || ''
  if (nombreComp.toLowerCase().startsWith('dr. ') || nombreComp.toLowerCase().startsWith('dra. ')) {
    const partes = nombreComp.split(' ')
    if (partes.length > 1) {
      return `${partes[0]} ${partes[1]}`
    }
  }
  return nombreComp.split(' ')[0]
})

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
  { label: 'Total citas', valor: citas.value.length, icono: 'pi-calendar', color: '#388bfd', bg: 'rgba(56,139,253,0.08)', borde: 'rgba(56,139,253,0.2)', filtro: '' },
  { label: 'Pendientes', valor: citas.value.filter(c => c.estado === 'pendiente').length, icono: 'pi-clock', color: '#fbbf24', bg: 'rgba(251,191,36,0.08)', borde: 'rgba(251,191,36,0.2)', filtro: 'pendiente' },
  { label: 'Confirmadas', valor: citas.value.filter(c => c.estado === 'confirmada').length, icono: 'pi-check-circle', color: '#3fb950', bg: 'rgba(63,185,80,0.08)', borde: 'rgba(63,185,80,0.2)', filtro: 'confirmada' },
  { label: 'Canceladas', valor: citas.value.filter(c => c.estado === 'cancelada').length, icono: 'pi-times-circle', color: '#f85149', bg: 'rgba(248,81,73,0.08)', borde: 'rgba(248,81,73,0.2)', filtro: 'cancelada' },
])

const citasFiltradas = computed(() => {
  if (!filtroEstado.value) return citas.value
  return citas.value.filter(c => c.estado === filtroEstado.value)
})

const statsDoctor = computed(() => [
  { label: 'Total citas', valor: citasDoctor.value.length, icono: 'pi-calendar', color: '#388bfd', bg: 'rgba(56,139,253,0.08)', borde: 'rgba(56,139,253,0.2)', filtro: '' },
  { label: 'Pendientes', valor: citasDoctor.value.filter(c => c.estado === 'pendiente').length, icono: 'pi-clock', color: '#fbbf24', bg: 'rgba(251,191,36,0.08)', borde: 'rgba(251,191,36,0.2)', filtro: 'pendiente' },
  { label: 'Confirmadas', valor: citasDoctor.value.filter(c => c.estado === 'confirmada').length, icono: 'pi-check-circle', color: '#3fb950', bg: 'rgba(63,185,80,0.08)', borde: 'rgba(63,185,80,0.2)', filtro: 'confirmada' },
  { label: 'Canceladas', valor: citasDoctor.value.filter(c => c.estado === 'cancelada').length, icono: 'pi-times-circle', color: '#f85149', bg: 'rgba(248,81,73,0.08)', borde: 'rgba(248,81,73,0.2)', filtro: 'cancelada' },
])

const citasDoctorFiltradas = computed(() => {
  if (!filtroEstado.value) return citasDoctor.value
  return citasDoctor.value.filter(c => c.estado === filtroEstado.value)
})

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

const obtenerCitasDoctor = async () => {
  if (!usuario.value.doctor_id) return
  cargandoCitasDoctor.value = true
  try {
    const res = await axios.get(`/citas/doctor/${usuario.value.doctor_id}`)
    citasDoctor.value = res.data
  } catch {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar tus citas', life: 3000 })
  } finally {
    cargandoCitasDoctor.value = false
  }
}

const cambiarEstadoCitaDoctor = async (idCita, nuevoEstado) => {
  cargando.value = true
  try {
    await axios.put(`/citas/${idCita}/estado`, null, { params: { estado: nuevoEstado } })
    notificacion.add({
      severity: 'success',
      summary: nuevoEstado === 'confirmada' ? 'Cita confirmada' : 'Cita cancelada',
      detail: `La cita fue marcada como ${nuevoEstado}`,
      life: 3000
    })
    await obtenerCitasDoctor()
  } catch {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo actualizar el estado de la cita', life: 3000 })
  } finally {
    cargando.value = false
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
  if (usuario.value.rol === 'doctor') {
    obtenerCitasDoctor()
  } else {
    obtenerDoctores()
    obtenerCitas()
  }
  actualizarReloj()
  intervaloReloj = setInterval(actualizarReloj, 1000)
})

onUnmounted(() => {
  clearInterval(intervaloReloj)
})
</script>

<style scoped>
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
  transition: all 0.2s ease;
  cursor: pointer;
  user-select: none;
}
.stat-card:hover { border-color: #388bfd; transform: translateY(-2px); }
.stat-card.stat-activa {
  background: rgba(56, 139, 253, 0.04);
  border-color: #388bfd;
  box-shadow: 0 0 12px rgba(56, 139, 253, 0.15);
}
.stat-icono { width: 40px; height: 40px; border: 1px solid; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.stat-num { font-size: 1.5rem; font-weight: 700; color: #e6edf3; line-height: 1; margin-bottom: 0.15rem; }
.stat-label { font-size: 0.72rem; color: #484f58; }

/* BANNER FILTRO ACTIVO */
.banner-filtro {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(56, 139, 253, 0.06);
  border: 1px solid rgba(56, 139, 253, 0.18);
  padding: 0.75rem 1rem;
  border-radius: 10px;
  margin-bottom: 1.2rem;
  font-size: 0.82rem;
}
.filtro-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #8b949e;
}
.filtro-info i {
  color: #388bfd;
}
.filtro-valor {
  color: #388bfd;
  text-transform: uppercase;
  font-weight: 700;
}
.btn-limpiar-filtro {
  background: transparent;
  border: 1px solid rgba(56, 139, 253, 0.3);
  color: #388bfd;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  transition: all 0.2s;
}
.btn-limpiar-filtro:hover {
  background: #388bfd;
  color: #e6edf3;
  border-color: #388bfd;
}

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

/* HAMBURGER & SIDEBAR STYLE */
.btn-hamburguesa {
  background: transparent;
  border: none;
  color: #8b949e;
  font-size: 1.4rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.btn-hamburguesa:hover {
  color: #388bfd;
  background: rgba(56, 139, 253, 0.08);
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(8, 12, 20, 0.6);
  backdrop-filter: blur(4px);
  z-index: 150;
  display: flex;
  justify-content: flex-end;
}
.sidebar-caja {
  width: 280px;
  background: #0d1117;
  border-left: 1px solid #21262d;
  height: 100%;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  box-shadow: -10px 0 40px rgba(0, 0, 0, 0.5);
}
.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.sidebar-perfil {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  text-align: left;
}
.sidebar-avatar {
  width: 48px;
  height: 48px;
  background: #1a3a6e;
  border: 2px solid #2d5fa8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 700;
  color: #60a5fa;
}
.sidebar-nombre {
  font-size: 0.95rem;
  font-weight: 700;
  color: #e6edf3;
  line-height: 1.2;
}
.sidebar-rol {
  font-size: 0.72rem;
  color: #388bfd;
  font-weight: 600;
  text-transform: uppercase;
  margin-top: 0.15rem;
}
.sidebar-cerrar {
  background: transparent;
  border: none;
  color: #484f58;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 6px;
  transition: all 0.2s;
}
.sidebar-cerrar:hover {
  color: #e6edf3;
}

.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.menu-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #8b949e;
  font-size: 0.88rem;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
}
.menu-item:hover {
  background: rgba(56, 139, 253, 0.08);
  color: #388bfd;
}
.menu-divisor {
  border: 0;
  height: 1px;
  background: #21262d;
  margin: 0.5rem 0;
}
.menu-item-salir:hover {
  background: rgba(248, 81, 73, 0.08);
  color: #f85149;
}

/* MODALES */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(8, 12, 20, 0.88);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}
.modal-caja {
  width: 100%;
  max-width: 400px;
  background: #0d1117;
  border: 1px solid #21262d;
  border-radius: 18px;
  padding: 2rem;
  box-shadow: 0 24px 80px rgba(0,0,0,0.6);
  text-align: left;
}
.modal-cabeza {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.modal-icono {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  flex-shrink: 0;
  background: rgba(56,139,253,0.1);
  border: 1px solid rgba(56,139,253,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: #388bfd;
}
.modal-titulo {
  font-size: 0.95rem;
  font-weight: 700;
  color: #e6edf3;
  margin-bottom: 0.2rem;
}
.modal-sub {
  font-size: 0.75rem;
  color: #484f58;
}
.modal-cerrar {
  margin-left: auto;
  background: transparent;
  border: none;
  color: #484f58;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 6px;
}
.modal-cerrar:hover {
  color: #e6edf3;
}

.perfil-datos, .acerca-cuerpo {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  margin-top: 1rem;
}
.dato-grupo label {
  display: block;
  font-size: 0.72rem;
  color: #484f58;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 0.25rem;
}
.dato-grupo p {
  font-size: 0.88rem;
  color: #e6edf3;
  font-weight: 500;
}
.badge-rol {
  display: inline-block;
  background: rgba(56, 139, 253, 0.15);
  border: 1px solid rgba(56, 139, 253, 0.3);
  color: #388bfd;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
  text-transform: uppercase;
  font-size: 0.7rem;
  font-weight: 700;
}
.divisor-acerca {
  border: 0;
  height: 1px;
  background: #21262d;
  margin: 0.3rem 0;
}
.contacto-titulo {
  font-size: 0.82rem;
  color: #e6edf3;
}
.contacto-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.85rem;
  color: #8b949e;
}
.contacto-item i {
  color: #388bfd;
}

/* ACCIONES DE MODAL */
.modal-acciones {
  display: flex;
  gap: 0.7rem;
  margin-top: 1.3rem;
}
.btn-modal-cancelar {
  flex: 1;
  padding: 0.55rem;
  background: transparent;
  border: 1px solid #21262d;
  border-radius: 8px;
  color: #8b949e;
  font-size: 0.82rem;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
}
.btn-modal-ok {
  flex: 1;
  padding: 0.55rem;
  background: #1a3a6e;
  border: 1px solid #2d5fa8;
  border-radius: 8px;
  color: #e6edf3;
  font-size: 0.82rem;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}
.btn-modal-ok:hover:not(:disabled) {
  background: #1d4ed8;
  border-color: #388bfd;
}
.btn-modal-ok:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* TRANSICIONES SIDEBAR */
.sidebar-fade-enter-active, .sidebar-fade-leave-active {
  transition: opacity 0.25s ease;
}
.sidebar-fade-enter-from, .sidebar-fade-leave-to {
  opacity: 0;
}
.sidebar-fade-enter-active .sidebar-caja, .sidebar-fade-leave-active .sidebar-caja {
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.sidebar-fade-enter-from .sidebar-caja {
  transform: translateX(100%);
}
.sidebar-fade-leave-to .sidebar-caja {
  transform: translateX(100%);
}

/* TRANSICIONES */
.deslizar-enter-active { transition: opacity 0.4s ease, transform 0.4s ease; }
.deslizar-enter-from { opacity: 0; transform: translateY(-16px); }
.lista-enter-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.lista-enter-from { opacity: 0; transform: translateX(-12px); }
.lista-leave-active { transition: opacity 0.2s; }
.lista-leave-to { opacity: 0; }

/* TABLA DE CITAS - VISTA DOCTOR */
.tabla-wrapper {
  overflow-x: auto;
  margin-top: 1rem;
  border-radius: 12px;
  background: #0d1117;
  border: 1px solid #21262d;
}
.tabla-admin {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.85rem;
}
.tabla-admin th {
  padding: 1rem 1.2rem;
  color: #8b949e;
  font-weight: 600;
  border-bottom: 1px solid #21262d;
  letter-spacing: 0.02em;
  white-space: nowrap;
}
.tabla-admin td {
  padding: 1.1rem 1.2rem;
  border-bottom: 1px solid #161b22;
  color: #c9d1d9;
  vertical-align: middle;
}
.texto-blanco {
  color: #f0f6fc;
}
.badge-especialidad {
  background: rgba(110, 118, 129, 0.1);
  border: 1px solid rgba(110, 118, 129, 0.2);
  color: #8b949e;
  padding: 0.2rem 0.55rem;
  border-radius: 6px;
  font-size: 0.72rem;
}

/* ACCIONES DE TABLA */
.acciones-fila {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}
.btn-accion {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: transparent;
  border: 1px solid #21262d;
  border-radius: 8px;
  color: #8b949e;
  padding: 0.45rem 0.8rem;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
  user-select: none;
}
.btn-confirmar {
  background: rgba(63, 185, 80, 0.1) !important;
  border-color: rgba(63, 185, 80, 0.3) !important;
  color: #3fb950 !important;
}
.btn-confirmar:hover {
  background: #3fb950 !important;
  border-color: #3fb950 !important;
  color: #ffffff !important;
}
.btn-eliminar {
  background: rgba(248, 81, 73, 0.1) !important;
  border-color: rgba(248, 81, 73, 0.3) !important;
  color: #f85149 !important;
}
.btn-eliminar:hover {
  background: #f85149 !important;
  border-color: #f85149 !important;
  color: #ffffff !important;
}

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