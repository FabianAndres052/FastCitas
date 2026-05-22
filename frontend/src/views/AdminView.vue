<template>
  <div class="pagina-admin">
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
        </svg>
        <span class="nav-nombre">FastCitas <span class="badge-admin">Admin</span></span>
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

    <!-- CUERPO PRINCIPAL -->
    <div class="contenido">
      <!-- SKELETON DE CARGA (Fijo por 2 segundos) -->
      <div v-if="cargando" class="skeleton-wrapper">
        <div class="skeleton-header">
          <Skeleton height="3rem" width="40%" class="mb-4" />
        </div>
        <div class="skeleton-grid">
          <Skeleton height="8rem" v-for="i in 4" :key="i" class="skeleton-card" />
        </div>
        <Skeleton height="20rem" class="mt-4" />
      </div>

      <!-- CONTENIDO REAL -->
      <div v-else class="admin-content">
        <div class="seccion-titulo">
          <h1>Panel de Administración</h1>
          <p>Gestión global de citas médicas y estados del sistema.</p>
        </div>

        <!-- TABS DE CONTROL -->
        <div class="tabs-control">
          <button
            :class="['tab-btn', { activo: tabActiva === 'citas' }]"
            @click="tabActiva = 'citas'"
          >
            <i class="pi pi-calendar"></i>
            <span>Gestión de Citas</span>
          </button>
          <button
            :class="['tab-btn', { activo: tabActiva === 'doctores' }]"
            @click="tabActiva = 'doctores'"
          >
            <i class="pi pi-users"></i>
            <span>Gestión de Médicos</span>
          </button>
        </div>

        <!-- VISTA DE GESTIÓN DE CITAS -->
        <div v-if="tabActiva === 'citas'">
          <!-- STATS -->
          <div class="grid-stats">
            <div
              class="stat-card"
              v-for="s in statsAdmin"
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

          <!-- TABLA DE CITAS -->
          <div class="seccion-card">
            <div class="card-cabeza">
              <i class="pi pi-table cabeza-icono"></i>
              <div>
                <h2 class="card-titulo">Todas las citas del sistema</h2>
                <p class="card-sub">Visualiza, confirma, cancela o elimina citas agendadas.</p>
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

            <div v-if="citas.length === 0" class="sin-datos">
              <i class="pi pi-calendar-times"></i>
              <p>No hay citas registradas en el sistema.</p>
            </div>

            <div v-else-if="citasFiltradas.length === 0" class="sin-datos">
              <i class="pi pi-filter-slash"></i>
              <p>No hay citas con el estado seleccionado: <strong>{{ filtroEstado }}</strong></p>
            </div>

            <div v-else class="tabla-wrapper">
              <table class="tabla-admin">
                <thead>
                  <tr>
                    <th>Paciente</th>
                    <th>Médico</th>
                    <th>Especialidad</th>
                    <th>Fecha y Hora</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="c in citasFiltradas" :key="c.id">
                    <td><strong class="texto-blanco">{{ c.paciente_nombre }}</strong></td>
                    <td>{{ c.doctor_nombre }}</td>
                    <td><span class="badge-especialidad">{{ c.especialidad }}</span></td>
                    <td>{{ c.fecha }} a las {{ c.hora }}</td>
                    <td>
                      <span :class="['badge-estado', `estado-${c.estado}`]">{{ c.estado }}</span>
                    </td>
                    <td>
                      <div class="acciones-fila">
                        <button 
                          v-if="c.estado === 'pendiente'" 
                          class="btn-accion btn-confirmar" 
                          @click="cambiarEstado(c.id, 'confirmada')"
                          title="Confirmar Cita"
                        >
                          <i class="pi pi-check"></i>
                        </button>
                        <button 
                          v-if="c.estado !== 'cancelada'" 
                          class="btn-accion btn-cancelar" 
                          @click="cambiarEstado(c.id, 'cancelada')"
                          title="Cancelar Cita"
                        >
                          <i class="pi pi-times"></i>
                        </button>
                        <button 
                          class="btn-accion btn-eliminar" 
                          @click="eliminarCita(c.id)"
                          title="Eliminar Cita"
                        >
                          <i class="pi pi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- VISTA DE GESTIÓN DE MÉDICOS -->
        <div v-else-if="tabActiva === 'doctores'">
          <!-- STATS DOCTORES -->
          <div class="grid-stats">
            <div
              class="stat-card"
              v-for="s in statsDoctores"
              :key="s.label"
              :class="{ 'stat-activa': filtroDoctor === s.filtro }"
              @click="filtroDoctor = s.filtro"
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

          <!-- TABLA DE DOCTORES -->
          <div class="seccion-card">
            <div class="card-cabeza">
              <i class="pi pi-users cabeza-icono"></i>
              <div>
                <h2 class="card-titulo">Todos los médicos del sistema</h2>
                <p class="card-sub">Controla la visibilidad pública de los médicos en el sistema.</p>
              </div>
            </div>

            <!-- BANNER FILTRO ACTIVO -->
            <Transition name="deslizar">
              <div class="banner-filtro" v-if="filtroDoctor !== ''">
                <div class="filtro-info">
                  <i class="pi pi-filter"></i>
                  <span>Mostrando médicos con visibilidad: <strong class="filtro-valor">{{ filtroDoctor }}</strong></span>
                </div>
                <button class="btn-limpiar-filtro" @click="filtroDoctor = ''">
                  Limpiar filtro <i class="pi pi-times"></i>
                </button>
              </div>
            </Transition>

            <div v-if="doctores.length === 0" class="sin-datos">
              <i class="pi pi-user-minus"></i>
              <p>No hay médicos registrados en el sistema.</p>
            </div>

            <div v-else-if="doctoresFiltrados.length === 0" class="sin-datos">
              <i class="pi pi-filter-slash"></i>
              <p>No hay médicos con la visibilidad seleccionada: <strong>{{ filtroDoctor }}</strong></p>
            </div>

            <div v-else class="tabla-wrapper">
              <table class="tabla-admin">
                <thead>
                  <tr>
                    <th>Médico</th>
                    <th>Correo Electrónico</th>
                    <th>Especialidad</th>
                    <th>Teléfono</th>
                    <th>Visibilidad</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="d in doctoresFiltrados" :key="d.id">
                    <td>
                      <div style="display: flex; align-items: center; gap: 0.6rem;">
                        <div class="doctor-avatar-mini" :style="{ background: colorAvatar(d.especialidad) }">
                          {{ d.foto_iniciales }}
                        </div>
                        <strong class="texto-blanco">{{ d.nombre }}</strong>
                      </div>
                    </td>
                    <td>{{ d.email }}</td>
                    <td><span class="badge-especialidad">{{ d.especialidad }}</span></td>
                    <td>{{ d.telefono }}</td>
                    <td>
                      <span :class="['badge-estado', d.activo === 1 ? 'estado-confirmada' : 'estado-pendiente']">
                        {{ d.activo === 1 ? 'Visible' : 'Oculto' }}
                      </span>
                    </td>
                    <td>
                      <button
                        :class="['btn-toggle-activo', d.activo === 1 ? 'ocultar' : 'mostrar']"
                        @click="toggleActivo(d.id)"
                        :title="d.activo === 1 ? 'Ocultar doctor de la lista de agendamiento' : 'Mostrar doctor en la lista de agendamiento'"
                      >
                        <i :class="['pi', d.activo === 1 ? 'pi-eye-slash' : 'pi-eye']"></i>
                        <span>{{ d.activo === 1 ? 'Ocultar' : 'Habilitar' }}</span>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
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
                <p class="sidebar-rol">{{ usuario.rol === 'admin' ? 'Administrador' : usuario.rol === 'doctor' ? 'Médico' : 'Paciente' }}</p>
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
            <div class="modal-icono"><i class="pi pi-info-circle"></i></div>
            <div style="flex:1">
              <p class="modal-titulo">Acerca de Nosotros</p>
              <p class="modal-sub">Sobre FastCitas</p>
            </div>
            <button class="modal-cerrar" @click="mostrarModalAcerca = false"><i class="pi pi-times"></i></button>
          </div>
          <div class="acerca-cuerpo">
            <p><strong>FastCitas</strong> es la plataforma líder en agendamiento digital de citas médicas para centros de salud pública de Colombia, diseñada para erradicar las largas filas desde las 4:00 AM.</p>
            <p>Nuestra misión es hacer la salud pública accesible, digna y moderna para todos.</p>
            <hr class="divisor-acerca" />
            <p class="contacto-titulo"><strong>Contacto de Soporte</strong></p>
            <p class="contacto-item"><i class="pi pi-envelope"></i> soporte@fastcitas.com</p>
            <p class="contacto-item"><i class="pi pi-phone"></i> +57 (300) 123-4567</p>
            <p class="contacto-item"><i class="pi pi-map-marker"></i> Bogotá, Colombia</p>
          </div>
        </div>
      </div>
    </Transition>

    <Toast />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import axios from 'axios'

const enrutador = useRouter()
const notificacion = useToast()

const usuario = ref(JSON.parse(localStorage.getItem('usuario') || '{}'))
const cargando = ref(true)
const citas = ref([])
const filtroEstado = ref('')

const tabActiva = ref('citas')
const doctores = ref([])
const filtroDoctor = ref('')

const mostrarSidebar = ref(false)
const mostrarModalPerfil = ref(false)
const mostrarModalPassword = ref(false)
const mostrarModalAcerca = ref(false)

const nuevaContrasena = ref('')
const confirmarContrasena = ref('')
const cargandoPassword = ref(false)

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

const statsAdmin = computed(() => [
  { label: 'Total Citas', valor: citas.value.length, icono: 'pi-calendar', color: '#388bfd', bg: 'rgba(56,139,253,0.08)', borde: 'rgba(56,139,253,0.2)', filtro: '' },
  { label: 'Pendientes', valor: citas.value.filter(c => c.estado === 'pendiente').length, icono: 'pi-clock', color: '#fbbf24', bg: 'rgba(251,191,36,0.08)', borde: 'rgba(251,191,36,0.2)', filtro: 'pendiente' },
  { label: 'Confirmadas', valor: citas.value.filter(c => c.estado === 'confirmada').length, icono: 'pi-check-circle', color: '#3fb950', bg: 'rgba(63,185,80,0.08)', borde: 'rgba(63,185,80,0.2)', filtro: 'confirmada' },
  { label: 'Canceladas', valor: citas.value.filter(c => c.estado === 'cancelada').length, icono: 'pi-times-circle', color: '#f85149', bg: 'rgba(248,81,73,0.08)', borde: 'rgba(248,81,73,0.2)', filtro: 'cancelada' },
])

const statsDoctores = computed(() => [
  { label: 'Total Médicos', valor: doctores.value.length, icono: 'pi-users', color: '#388bfd', bg: 'rgba(56,139,253,0.08)', borde: 'rgba(56,139,253,0.2)', filtro: '' },
  { label: 'Visibles', valor: doctores.value.filter(d => d.activo === 1).length, icono: 'pi-eye', color: '#3fb950', bg: 'rgba(63,185,80,0.08)', borde: 'rgba(63,185,80,0.2)', filtro: 'visible' },
  { label: 'Ocultos', valor: doctores.value.filter(d => d.activo === 0).length, icono: 'pi-eye-slash', color: '#fbbf24', bg: 'rgba(251,191,36,0.08)', borde: 'rgba(251,191,36,0.2)', filtro: 'oculto' }
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

const citasFiltradas = computed(() => {
  if (!filtroEstado.value) return citas.value
  return citas.value.filter(c => c.estado === filtroEstado.value)
})

const doctoresFiltrados = computed(() => {
  if (!filtroDoctor.value) return doctores.value
  const act = filtroDoctor.value === 'visible' ? 1 : 0
  return doctores.value.filter(d => d.activo === act)
})

const obtenerCitas = async () => {
  try {
    const res = await axios.get('/citas/')
    citas.value = res.data
  } catch (error) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las citas', life: 3000 })
  }
}

const obtenerDoctores = async () => {
  try {
    const res = await axios.get('/doctores/todos')
    doctores.value = res.data
  } catch (error) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los doctores', life: 3000 })
  }
}

const toggleActivo = async (docId) => {
  try {
    await axios.put(`/doctores/${docId}/toggle-activo`)
    notificacion.add({ severity: 'success', summary: 'Éxito', detail: 'Visibilidad del doctor actualizada', life: 2000 })
    await obtenerDoctores()
  } catch (error) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo cambiar la visibilidad del doctor', life: 3000 })
  }
}

const cambiarEstado = async (id, nuevoEstado) => {
  try {
    await axios.put(`/citas/${id}/estado`, null, { params: { estado: nuevoEstado } })
    notificacion.add({ severity: 'success', summary: 'Estado actualizado', detail: `Cita marcada como ${nuevoEstado}`, life: 2000 })
    await obtenerCitas()
  } catch (error) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo actualizar el estado', life: 3000 })
  }
}

const eliminarCita = async (id) => {
  if (!confirm('¿Estás seguro de que deseas eliminar esta cita permanentemente?')) return
  try {
    await axios.delete(`/citas/${id}`)
    notificacion.add({ severity: 'info', summary: 'Cita eliminada', detail: 'La cita fue borrada del sistema', life: 2000 })
    await obtenerCitas()
  } catch (error) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar la cita', life: 3000 })
  }
}

const cerrarSesion = () => {
  localStorage.removeItem('usuario')
  enrutador.push('/login')
}

onMounted(() => {
  obtenerCitas()
  obtenerDoctores()
  // Retardo de 2 segundos para el esqueleto como solicitó el usuario
  setTimeout(() => {
    cargando.value = false
  }, 2000)
})
</script>

<style scoped>
.pagina-admin { min-height: 100vh; background: #080c14; color: #e6edf3; }

/* NAVBAR */
.navbar {
  background: #0d1117; border-bottom: 1px solid #21262d;
  padding: 0.9rem 2rem; display: flex; justify-content: space-between; align-items: center;
  position: sticky; top: 0; z-index: 10;
}
.nav-logo { display: flex; align-items: center; gap: 0.7rem; }
.nav-nombre { font-size: 1.1rem; font-weight: 700; color: #e6edf3; letter-spacing: -0.5px; display: flex; align-items: center; gap: 0.5rem; }
.badge-admin { background: rgba(56,139,253,0.15); border: 1px solid rgba(56,139,253,0.3); color: #388bfd; padding: 0.15rem 0.5rem; border-radius: 99px; font-size: 0.7rem; font-weight: 600; }

.nav-derecha { display: flex; align-items: center; gap: 1rem; }
.nav-usuario { display: flex; align-items: center; gap: 0.6rem; }
.avatar {
  width: 32px; height: 32px; background: #1a3a6e; border: 1px solid #2d5fa8;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; font-weight: 700; color: #60a5fa;
}
.nav-saludo { font-size: 0.85rem; color: #8b949e; }

/* CONTENIDO */
.contenido { max-width: 1000px; margin: 0 auto; padding: 2rem 1.5rem; }
.seccion-titulo { margin-bottom: 2rem; }
.seccion-titulo h1 { font-size: 1.8rem; font-weight: 700; color: #e6edf3; margin-bottom: 0.4rem; letter-spacing: -0.5px; }
.seccion-titulo p { font-size: 0.9rem; color: #8b949e; }

/* SKELETONS */
.skeleton-wrapper { display: flex; flex-direction: column; gap: 1.5rem; }
.skeleton-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.skeleton-card { border-radius: 14px; }

/* STATS */
.grid-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.stat-card {
  background: #0d1117; border: 1px solid #21262d; border-radius: 14px;
  padding: 1.2rem; display: flex; align-items: center; gap: 1rem;
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
.stat-icono { width: 44px; height: 44px; border: 1px solid; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }
.stat-num { font-size: 1.8rem; font-weight: 700; color: #e6edf3; line-height: 1; margin-bottom: 0.2rem; }
.stat-label { font-size: 0.75rem; color: #8b949e; font-weight: 500; }

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

/* CARD DE TABLA */
.seccion-card { background: #0d1117; border: 1px solid #21262d; border-radius: 16px; padding: 1.8rem; }
.card-cabeza { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1.2rem; border-bottom: 1px solid #161b22; }
.cabeza-icono { font-size: 1.3rem; color: #388bfd; background: rgba(56,139,253,0.08); border: 1px solid rgba(56,139,253,0.15); padding: 0.6rem; border-radius: 10px; }
.card-titulo { font-size: 1rem; font-weight: 600; color: #e6edf3; margin-bottom: 0.15rem; }
.card-sub { font-size: 0.78rem; color: #8b949e; }

/* TABLA */
.tabla-wrapper { overflow-x: auto; }
.tabla-admin { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
.tabla-admin th { padding: 0.9rem 1rem; color: #8b949e; font-weight: 600; border-bottom: 1px solid #21262d; }
.tabla-admin td { padding: 1rem; border-bottom: 1px solid #161b22; color: #c9d1d9; }
.texto-blanco { color: #f0f6fc; }
.badge-especialidad { background: rgba(110,118,129,0.1); border: 1px solid rgba(110,118,129,0.2); color: #8b949e; padding: 0.15rem 0.5rem; border-radius: 6px; font-size: 0.72rem; }

/* BADGES ESTADO */
.badge-estado { padding: 0.2rem 0.6rem; border-radius: 99px; font-size: 0.7rem; font-weight: 600; text-transform: capitalize; display: inline-block; }
.estado-pendiente { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.25); color: #fbbf24; }
.estado-confirmada { background: rgba(63,185,80,0.1); border: 1px solid rgba(63,185,80,0.25); color: #3fb950; }
.estado-cancelada { background: rgba(248,81,73,0.1); border: 1px solid rgba(248,81,73,0.25); color: #f85149; }

/* ACCIONES */
.acciones-fila { display: flex; gap: 0.4rem; }
.btn-accion { background: transparent; border: 1px solid #21262d; border-radius: 6px; color: #8b949e; padding: 0.35rem 0.55rem; cursor: pointer; font-size: 0.8rem; transition: all 0.2s; }
.btn-confirmar:hover { border-color: #3fb950; color: #3fb950; background: rgba(63,185,80,0.05); }
.btn-cancelar:hover { border-color: #fbbf24; color: #fbbf24; background: rgba(251,191,36,0.05); }
.btn-eliminar:hover { border-color: #f85149; color: #f85149; background: rgba(248,81,73,0.05); }

.sin-datos { text-align: center; padding: 3rem 1rem; color: #8b949e; display: flex; flex-direction: column; align-items: center; gap: 0.7rem; }
.sin-datos i { font-size: 2rem; color: #30363d; }

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

/* TRANSICIONES MODAL FADE */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-active .modal-caja, .modal-fade-leave-active .modal-caja {
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.modal-fade-enter-from .modal-caja, .modal-fade-leave-to .modal-caja {
  transform: scale(0.95);
}

/* TRANSICIONES */
.deslizar-enter-active { transition: opacity 0.4s ease, transform 0.4s ease; }
.deslizar-enter-from { opacity: 0; transform: translateY(-16px); }

.campo label { display: block; font-size: 0.78rem; font-weight: 500; color: #8b949e; margin-bottom: 0.45rem; }
.inp {
  width: 100%; padding: 0.55rem 0.8rem;
  background: #161b22; border: 1px solid #30363d; border-radius: 8px;
  color: #e6edf3; font-size: 0.85rem; font-family: 'Inter', sans-serif;
  transition: border-color 0.2s;
}
.inp:hover, .inp:focus { border-color: #388bfd; outline: none; }

.tabs-control {
  display: flex;
  background: #0d1117;
  border: 1px solid #21262d;
  padding: 0.35rem;
  border-radius: 12px;
  gap: 0.35rem;
  margin-bottom: 2rem;
  width: fit-content;
}
.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: #8b949e;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: 'Inter', sans-serif;
}
.tab-btn:hover {
  color: #e6edf3;
  background: rgba(255, 255, 255, 0.02);
}
.tab-btn.activo {
  color: #e6edf3;
  background: #1a3a6e;
  border: 1px solid #2d5fa8;
  box-shadow: 0 4px 12px rgba(26, 58, 110, 0.25);
}

.doctor-avatar-mini {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.72rem;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.btn-toggle-activo {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: transparent;
  border: 1px solid #21262d;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  color: #8b949e;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}
.btn-toggle-activo.mostrar:hover {
  border-color: #3fb950;
  color: #3fb950;
  background: rgba(63, 185, 80, 0.05);
}
.btn-toggle-activo.ocultar:hover {
  border-color: #f85149;
  color: #f85149;
  background: rgba(248, 81, 73, 0.05);
}

@media (max-width: 768px) {
  .skeleton-grid { grid-template-columns: 1fr; }
  .grid-stats { grid-template-columns: repeat(2, 1fr); }
  .navbar { padding: 0.9rem 1rem; }
  .nav-saludo { display: none; }
  .tabs-control { width: 100%; }
  .tab-btn { flex: 1; justify-content: center; }
}
@media (max-width: 480px) {
  .grid-stats { grid-template-columns: 1fr; }
}
</style>