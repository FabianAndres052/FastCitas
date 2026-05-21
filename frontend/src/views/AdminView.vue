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
          <polyline class="pulso-linea" points="4,40 14,40 20,26 28,54 32,40"
            fill="none" stroke="#388bfd" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <polyline class="pulso-linea pulso-delay" points="48,40 52,26 60,54 66,40 76,40"
            fill="none" stroke="#388bfd" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="nav-nombre">FastCitas</span>
        <span class="nav-badge">Admin</span>
      </div>
      <div class="nav-derecha">

        <!-- AVATAR CON MENÚ DESPLEGABLE -->
        <div class="nav-usuario" @click="menuUsuarioAbierto = !menuUsuarioAbierto" v-click-outside="() => menuUsuarioAbierto = false">
          <div class="avatar">A</div>
          <span class="nav-saludo">Administrador</span>
          <i :class="['pi', menuUsuarioAbierto ? 'pi-chevron-up' : 'pi-chevron-down', 'nav-chevron']"></i>

          <!-- DROPDOWN MENÚ -->
          <Transition name="menu-drop">
            <div class="menu-usuario" v-if="menuUsuarioAbierto" @click.stop>
              <div class="menu-header">
                <div class="menu-avatar-grande">A</div>
                <div>
                  <p class="menu-nombre">Administrador</p>
                  <p class="menu-rol">admin@fastcitas.com</p>
                </div>
              </div>
              <div class="menu-separador"></div>
              <button class="menu-item" @click="abrirPerfil">
                <i class="pi pi-user"></i> Ver mi perfil
              </button>
              <button class="menu-item" @click="abrirCambiarContrasena">
                <i class="pi pi-lock"></i> Cambiar contraseña
              </button>
              <div class="menu-separador"></div>
              <button class="menu-item menu-item-rojo" @click="cerrarSesion">
                <i class="pi pi-sign-out"></i> Cerrar sesión
              </button>
            </div>
          </Transition>
        </div>

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
          <span class="hero-nombre-texto">Administrador</span>
          <span class="hero-punto">.</span>
        </div>
        <p class="hero-sub">Panel de control · Gestión centralizada del sistema FastCitas</p>
        <div class="hero-chips">
          <span class="hero-chip"><i class="pi pi-shield"></i> Acceso total</span>
          <span class="hero-chip"><i class="pi pi-database"></i> Base de datos activa</span>
          <span class="hero-chip chip-verde"><i class="pi pi-circle-fill"></i> Sistema en línea</span>
          <span class="hero-chip chip-amarillo" v-if="citas.filter(c => c.estado === 'pendiente').length > 0">
            <i class="pi pi-clock"></i> {{ citas.filter(c => c.estado === 'pendiente').length }} pendientes
          </span>
        </div>
      </div>
      <div class="hero-der">
        <div class="reloj-bloque">
          <p class="reloj-hora">{{ horaActual }}</p>
          <p class="reloj-fecha">{{ fechaActual }}</p>
        </div>
        <div class="hero-stat-mini">
          <div class="mini-stat"><i class="pi pi-users"></i><span>{{ doctores.length }} médicos</span></div>
          <div class="mini-stat"><i class="pi pi-calendar"></i><span>{{ citas.length }} citas</span></div>
          <div class="mini-stat"><i class="pi pi-user"></i><span>{{ pacientes.length }} pacientes</span></div>
        </div>
      </div>
    </div>

    <div class="contenido">

      <!-- STATS CLICABLES -->
      <div class="grid-stats">
        <div
          class="stat-card"
          v-for="s in stats"
          :key="s.label"
          :class="{ 'stat-activa': filtroEstadoActivo === s.filtro }"
          @click="aplicarFiltroStat(s.filtro)"
          :title="s.accion"
          style="cursor:pointer"
        >
          <div class="stat-icono" :style="{ background: s.bg, borderColor: s.borde }">
            <i :class="['pi', s.icono]" :style="{ color: s.color }"></i>
          </div>
          <div style="flex:1">
            <p class="stat-num">{{ s.valor }}</p>
            <p class="stat-label">{{ s.label }}</p>
          </div>
          <div class="stat-hint" v-if="filtroEstadoActivo === s.filtro">
            <i class="pi pi-filter-fill" style="color:#388bfd; font-size:0.7rem"></i>
          </div>
          <div class="stat-flecha" v-else>
            <i class="pi pi-arrow-right" :style="{ color: s.color, fontSize: '0.7rem' }"></i>
          </div>
        </div>
      </div>

      <!-- INDICADOR DE FILTRO ACTIVO -->
      <Transition name="fade">
        <div class="filtro-activo-banner" v-if="filtroEstadoActivo !== null">
          <i class="pi pi-filter"></i>
          Mostrando citas <strong>{{ filtroEstadoActivo === '' ? 'de todos los estados' : filtroEstadoActivo + 's' }}</strong>
          <button class="filtro-limpiar" @click="limpiarFiltroStat">
            <i class="pi pi-times"></i> Quitar filtro
          </button>
        </div>
      </Transition>

      <!-- TABS -->
      <div class="tabs-wrapper">
        <button v-for="tab in tabs" :key="tab.id" class="tab-btn"
          :class="{ activo: tabActivo === tab.id }" @click="tabActivo = tab.id">
          <i :class="['pi', tab.icono]"></i> {{ tab.label }}
          <span class="tab-badge" v-if="tab.id === 'citas' && citas.filter(c => c.estado === 'pendiente').length > 0">
            {{ citas.filter(c => c.estado === 'pendiente').length }}
          </span>
        </button>
      </div>

      <!-- TAB: CITAS -->
      <div v-if="tabActivo === 'citas'">
        <div class="seccion-card">
          <div class="card-cabeza">
            <i class="pi pi-calendar cabeza-icono"></i>
            <div style="flex:1">
              <h2 class="card-titulo">Todas las citas</h2>
              <p class="card-sub">
                {{ citasFiltradas.length }} resultado(s)
                <span v-if="filtroEstado || busquedaCitas"> · filtros activos</span>
              </p>
            </div>
            <div class="buscador-wrap">
              <i class="pi pi-search buscador-icono"></i>
              <input v-model="busquedaCitas" class="buscador-inp" placeholder="Buscar paciente o doctor..." />
            </div>
            <select v-model="filtroEstado" class="inp-mini">
              <option value="">Todos</option>
              <option value="pendiente">Pendientes</option>
              <option value="confirmada">Confirmadas</option>
              <option value="cancelada">Canceladas</option>
            </select>
          </div>

          <div v-if="cargandoCitas" class="lista-skeleton">
            <Skeleton height="3.5rem" borderRadius="10px" v-for="n in 4" :key="n" />
          </div>
          <div v-else-if="citasFiltradas.length === 0" class="sin-citas">
            <div class="sin-citas-icono"><i class="pi pi-calendar"></i></div>
            <p class="sin-citas-titulo">Sin resultados</p>
            <p class="sin-citas-sub">No hay citas que coincidan con los filtros</p>
            <button class="btn-limpiar-todo" @click="limpiarTodosFiltros">Limpiar filtros</button>
          </div>
          <div v-else class="citas-lista">
            <TransitionGroup name="lista">
              <div class="cita-fila" v-for="c in citasFiltradas" :key="c.id">
                <div class="cita-avatar" :style="{ background: colorAvatar(c.especialidad) }">
                  {{ c.doctor_nombre?.split(' ').slice(-2).map(p => p[0]).join('') }}
                </div>
                <div class="cita-info">
                  <p class="cita-doctor">{{ c.paciente_nombre }}</p>
                  <p class="cita-detalle">{{ c.doctor_nombre }} · {{ c.especialidad }} · {{ c.fecha }} {{ c.hora }}</p>
                </div>
                <span :class="['badge-estado', `estado-${c.estado}`]">{{ c.estado }}</span>
                <div class="acciones-cita">
                  <button class="btn-accion confirmar" v-if="c.estado === 'pendiente'"
                    @click="cambiarEstado(c.id, 'confirmada')" title="Confirmar cita">
                    <i class="pi pi-check"></i>
                  </button>
                  <button class="btn-accion cancelar" v-if="c.estado !== 'cancelada'"
                    @click="cambiarEstado(c.id, 'cancelada')" title="Cancelar cita">
                    <i class="pi pi-times"></i>
                  </button>
                  <button class="btn-accion eliminar" @click="eliminarCita(c.id)" title="Eliminar cita">
                    <i class="pi pi-trash"></i>
                  </button>
                </div>
              </div>
            </TransitionGroup>
          </div>
        </div>
      </div>

      <!-- TAB: ESTADÍSTICAS -->
      <div v-if="tabActivo === 'estadisticas'">
        <div class="grid-2">
          <div class="seccion-card">
            <div class="card-cabeza">
              <i class="pi pi-chart-pie cabeza-icono"></i>
              <div>
                <h2 class="card-titulo">Estado de citas</h2>
                <p class="card-sub">Distribución actual</p>
              </div>
            </div>
            <div class="dona-wrap">
              <svg viewBox="0 0 120 120" class="dona-svg">
                <circle cx="60" cy="60" r="45" fill="none" stroke="#161b22" stroke-width="18"/>
                <circle cx="60" cy="60" r="45" fill="none" stroke="#fbbf24" stroke-width="18"
                  :stroke-dasharray="`${donaSegmento('pendiente')} 283`"
                  stroke-dashoffset="70.75" transform="rotate(-90 60 60)" style="transition:stroke-dasharray 1s ease"/>
                <circle cx="60" cy="60" r="45" fill="none" stroke="#3fb950" stroke-width="18"
                  :stroke-dasharray="`${donaSegmento('confirmada')} 283`"
                  :stroke-dashoffset="`${-(donaSegmento('pendiente') - 70.75)}`"
                  transform="rotate(-90 60 60)" style="transition:stroke-dasharray 1s ease"/>
                <circle cx="60" cy="60" r="45" fill="none" stroke="#f85149" stroke-width="18"
                  :stroke-dasharray="`${donaSegmento('cancelada')} 283`"
                  :stroke-dashoffset="`${-(donaSegmento('pendiente') + donaSegmento('confirmada') - 70.75)}`"
                  transform="rotate(-90 60 60)" style="transition:stroke-dasharray 1s ease"/>
                <text x="60" y="57" text-anchor="middle" fill="#e6edf3" font-size="16" font-weight="700" font-family="Inter">{{ citas.length }}</text>
                <text x="60" y="70" text-anchor="middle" fill="#484f58" font-size="7" font-family="Inter">total</text>
              </svg>
              <div class="dona-leyenda">
                <div class="leyenda-item leyenda-clicable" @click="aplicarFiltroStat('pendiente')">
                  <span class="leyenda-dot" style="background:#fbbf24"></span>
                  <span class="leyenda-label">Pendientes</span>
                  <span class="leyenda-val">{{ citas.filter(c => c.estado === 'pendiente').length }}</span>
                </div>
                <div class="leyenda-item leyenda-clicable" @click="aplicarFiltroStat('confirmada')">
                  <span class="leyenda-dot" style="background:#3fb950"></span>
                  <span class="leyenda-label">Confirmadas</span>
                  <span class="leyenda-val">{{ citas.filter(c => c.estado === 'confirmada').length }}</span>
                </div>
                <div class="leyenda-item leyenda-clicable" @click="aplicarFiltroStat('cancelada')">
                  <span class="leyenda-dot" style="background:#f85149"></span>
                  <span class="leyenda-label">Canceladas</span>
                  <span class="leyenda-val">{{ citas.filter(c => c.estado === 'cancelada').length }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="seccion-card">
            <div class="card-cabeza">
              <i class="pi pi-chart-bar cabeza-icono"></i>
              <div>
                <h2 class="card-titulo">Citas por especialidad</h2>
                <p class="card-sub">Top especialidades</p>
              </div>
            </div>
            <div class="barras-wrap">
              <div v-for="(item, i) in citasPorEspecialidad" :key="i" class="barra-fila barra-clicable"
                @click="busquedaCitas = item.especialidad; tabActivo = 'citas'">
                <span class="barra-label">{{ item.especialidad }}</span>
                <div class="barra-track">
                  <div class="barra-fill"
                    :style="{ width: `${(item.total / maxEspecialidad) * 100}%`, background: coloresBarra[i % coloresBarra.length] }">
                  </div>
                </div>
                <span class="barra-num">{{ item.total }}</span>
              </div>
              <div v-if="citasPorEspecialidad.length === 0" class="sin-citas" style="padding:1.5rem 0">
                <p class="sin-citas-sub">Sin datos disponibles</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB: DOCTORES -->
      <div v-if="tabActivo === 'doctores'">
        <div class="seccion-card">
          <div class="card-cabeza">
            <i class="pi pi-users cabeza-icono"></i>
            <div style="flex:1">
              <h2 class="card-titulo">Médicos registrados</h2>
              <p class="card-sub">{{ doctores.length }} doctor(es) en el sistema</p>
            </div>
            <button class="boton-nuevo" @click="mostrarFormDoctor = !mostrarFormDoctor">
              <i class="pi pi-plus"></i> Nuevo doctor
            </button>
          </div>
          <Transition name="deslizar">
            <div class="form-nuevo" v-if="mostrarFormDoctor">
              <div class="form-grid-4">
                <div class="campo"><label>Nombre completo</label><input v-model="nuevoDoctor.nombre" class="inp" placeholder="Dr. Juan Pérez" /></div>
                <div class="campo"><label>Especialidad</label>
                  <select v-model="nuevoDoctor.especialidad" class="inp">
                    <option value="">Seleccionar...</option>
                    <option v-for="e in especialidades" :key="e">{{ e }}</option>
                  </select>
                </div>
                <div class="campo"><label>Correo</label><input v-model="nuevoDoctor.email" class="inp" placeholder="doctor@correo.com" type="email" /></div>
                <div class="campo"><label>Teléfono</label><input v-model="nuevoDoctor.telefono" class="inp" placeholder="3001234567" /></div>
                <div class="campo"><label>Contraseña</label><input v-model="nuevoDoctor.password" class="inp" type="password" placeholder="Contraseña" /></div>
              </div>
              <div class="form-acciones">
                <button class="boton-cancelar-form" @click="mostrarFormDoctor = false">Cancelar</button>
                <button class="boton-guardar" @click="registrarDoctor" :disabled="guardando">
                  <span v-if="!guardando"><i class="pi pi-check"></i> Guardar doctor</span>
                  <span v-else><i class="pi pi-spin pi-spinner"></i> Guardando...</span>
                </button>
              </div>
            </div>
          </Transition>
          <div class="buscador-wrap" style="margin-bottom:1rem; max-width:320px">
            <i class="pi pi-search buscador-icono"></i>
            <input v-model="busquedaDoctores" class="buscador-inp" placeholder="Buscar doctor o especialidad..." />
          </div>
          <div v-if="cargandoDoctores" class="doctores-grid">
            <div v-for="n in 4" :key="n"><Skeleton height="100px" borderRadius="12px" /></div>
          </div>
          <div v-else class="doctores-grid">
            <div class="doctor-card" v-for="doc in doctoresFiltrados" :key="doc.id">
              <div class="doctor-avatar" :style="{ background: colorAvatar(doc.especialidad) }">{{ doc.foto_iniciales }}</div>
              <div class="doctor-info">
                <p class="doctor-nombre">{{ doc.nombre }}</p>
                <p class="doctor-especialidad">{{ doc.especialidad }}</p>
                <p class="doctor-contacto"><i class="pi pi-envelope"></i> {{ doc.email }}</p>
                <p class="doctor-contacto"><i class="pi pi-phone"></i> {{ doc.telefono }}</p>
                <p class="doctor-contacto" style="color:#388bfd">
                  <i class="pi pi-calendar"></i>
                  {{ citas.filter(c => c.doctor_nombre === doc.nombre).length }} citas
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB: PACIENTES -->
      <div v-if="tabActivo === 'pacientes'">
        <div class="seccion-card">
          <div class="card-cabeza">
            <i class="pi pi-users cabeza-icono"></i>
            <div style="flex:1">
              <h2 class="card-titulo">Pacientes registrados</h2>
              <p class="card-sub">{{ pacientes.length }} paciente(s) en el sistema</p>
            </div>
          </div>
          <div class="buscador-wrap" style="margin-bottom:1rem; max-width:320px">
            <i class="pi pi-search buscador-icono"></i>
            <input v-model="busquedaPacientes" class="buscador-inp" placeholder="Buscar paciente..." />
          </div>
          <div v-if="cargandoPacientes" class="lista-skeleton">
            <Skeleton height="3.5rem" borderRadius="10px" v-for="n in 3" :key="n" />
          </div>
          <div v-else-if="pacientesFiltrados.length === 0" class="sin-citas">
            <div class="sin-citas-icono"><i class="pi pi-users"></i></div>
            <p class="sin-citas-titulo">Sin resultados</p>
          </div>
          <div v-else class="citas-lista">
            <div class="cita-fila" v-for="p in pacientesFiltrados" :key="p.id">
              <div class="cita-avatar" style="background:#1a4a3a">{{ p.nombre?.charAt(0).toUpperCase() }}</div>
              <div class="cita-info">
                <p class="cita-doctor">{{ p.nombre }}</p>
                <p class="cita-detalle">{{ p.email }}</p>
              </div>
              <span class="badge-estado estado-confirmada">paciente</span>
              <span class="badge-citas-pac">
                <i class="pi pi-calendar"></i>
                {{ citas.filter(c => c.paciente_nombre === p.nombre).length }} citas
              </span>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- MODAL PERFIL -->
    <Transition name="modal-fade">
      <div class="modal-overlay" v-if="mostrarPerfil" @click.self="mostrarPerfil = false">
        <div class="modal-caja">
          <div class="modal-cabeza">
            <div class="modal-icono"><i class="pi pi-user"></i></div>
            <div>
              <p class="modal-titulo">Mi perfil</p>
              <p class="modal-sub">Información de la cuenta administrador</p>
            </div>
            <button class="modal-cerrar" @click="mostrarPerfil = false"><i class="pi pi-times"></i></button>
          </div>
          <div class="perfil-datos">
            <div class="perfil-avatar-grande">A</div>
            <div class="perfil-fila"><span class="perfil-key"><i class="pi pi-user"></i> Nombre</span><span class="perfil-val">Administrador</span></div>
            <div class="perfil-fila"><span class="perfil-key"><i class="pi pi-envelope"></i> Correo</span><span class="perfil-val">admin@fastcitas.com</span></div>
            <div class="perfil-fila"><span class="perfil-key"><i class="pi pi-shield"></i> Rol</span><span class="badge-estado estado-confirmada">Administrador</span></div>
            <div class="perfil-fila"><span class="perfil-key"><i class="pi pi-calendar"></i> Total citas</span><span class="perfil-val">{{ citas.length }}</span></div>
            <div class="perfil-fila"><span class="perfil-key"><i class="pi pi-users"></i> Doctores</span><span class="perfil-val">{{ doctores.length }}</span></div>
            <div class="perfil-fila"><span class="perfil-key"><i class="pi pi-user"></i> Pacientes</span><span class="perfil-val">{{ pacientes.length }}</span></div>
          </div>
          <button class="btn-modal-ok" style="width:100%; margin-top:1rem" @click="mostrarPerfil = false">
            <i class="pi pi-check"></i> Cerrar
          </button>
        </div>
      </div>
    </Transition>

    <!-- MODAL CAMBIAR CONTRASEÑA -->
    <Transition name="modal-fade">
      <div class="modal-overlay" v-if="mostrarCambioContrasena" @click.self="cerrarModalContrasena">
        <div class="modal-caja">
          <!-- PASO 1 -->
          <div v-if="pasoContrasena === 1">
            <div class="modal-cabeza">
              <div class="modal-icono"><i class="pi pi-lock"></i></div>
              <div style="flex:1">
                <p class="modal-titulo">Cambiar contraseña</p>
                <p class="modal-sub">Ingresa tu correo para verificar tu identidad</p>
              </div>
              <button class="modal-cerrar" @click="cerrarModalContrasena"><i class="pi pi-times"></i></button>
            </div>
            <div class="campo">
              <label>Correo electrónico</label>
              <input v-model="emailCambio" class="inp" placeholder="admin@fastcitas.com" :disabled="cargandoModal" />
            </div>
            <div class="modal-acciones">
              <button class="btn-modal-cancelar" @click="cerrarModalContrasena">Cancelar</button>
              <button class="btn-modal-ok" @click="verificarEmailAdmin" :disabled="cargandoModal">
                <span v-if="!cargandoModal"><i class="pi pi-arrow-right"></i> Continuar</span>
                <span v-else><i class="pi pi-spin pi-spinner"></i> Verificando...</span>
              </button>
            </div>
          </div>
          <!-- PASO 2 -->
          <div v-if="pasoContrasena === 2">
            <div class="modal-cabeza">
              <div class="modal-icono modal-icono-ok"><i class="pi pi-check"></i></div>
              <div style="flex:1">
                <p class="modal-titulo">Nueva contraseña</p>
                <p class="modal-sub">Cuenta verificada · <strong>{{ emailCambio }}</strong></p>
              </div>
              <button class="modal-cerrar" @click="cerrarModalContrasena"><i class="pi pi-times"></i></button>
            </div>
            <div class="campo">
              <label>Nueva contraseña</label>
              <input v-model="nuevaContrasena" type="password" class="inp" placeholder="Mínimo 6 caracteres" :disabled="cargandoModal" />
            </div>
            <div class="campo">
              <label>Confirmar contraseña</label>
              <input v-model="confirmarContrasena" type="password" class="inp" placeholder="Repite la contraseña" :disabled="cargandoModal" />
            </div>
            <Transition name="fade">
              <p class="aviso-modal" v-if="errorContrasena"><i class="pi pi-exclamation-triangle"></i> {{ errorContrasena }}</p>
            </Transition>
            <div class="modal-acciones">
              <button class="btn-modal-cancelar" @click="pasoContrasena = 1">Atrás</button>
              <button class="btn-modal-ok" @click="cambiarContrasena" :disabled="cargandoModal">
                <span v-if="!cargandoModal"><i class="pi pi-check"></i> Guardar</span>
                <span v-else><i class="pi pi-spin pi-spinner"></i> Guardando...</span>
              </button>
            </div>
          </div>
          <!-- PASO 3 -->
          <div v-if="pasoContrasena === 3" class="modal-exito">
            <div class="exito-icono"><i class="pi pi-check-circle"></i></div>
            <p class="exito-titulo">¡Contraseña actualizada!</p>
            <p class="exito-sub">Tu contraseña fue cambiada exitosamente</p>
            <button class="btn-modal-ok" @click="cerrarModalContrasena" style="margin-top:1.2rem; width:100%">
              <i class="pi pi-check"></i> Listo
            </button>
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

const citas = ref([])
const doctores = ref([])
const pacientes = ref([])
const cargandoCitas = ref(false)
const cargandoDoctores = ref(false)
const cargandoPacientes = ref(false)
const guardando = ref(false)
const tabActivo = ref('citas')
const filtroEstado = ref('')
const filtroEstadoActivo = ref(null) // para stat cards
const mostrarFormDoctor = ref(false)
const busquedaCitas = ref('')
const busquedaDoctores = ref('')
const busquedaPacientes = ref('')
const horaActual = ref('')
const fechaActual = ref('')
let intervaloReloj = null

// Menú usuario
const menuUsuarioAbierto = ref(false)
const mostrarPerfil = ref(false)
const mostrarCambioContrasena = ref(false)
const pasoContrasena = ref(1)
const emailCambio = ref('')
const nuevaContrasena = ref('')
const confirmarContrasena = ref('')
const cargandoModal = ref(false)
const errorContrasena = ref('')

const tabs = [
  { id: 'citas', label: 'Citas', icono: 'pi-calendar' },
  { id: 'estadisticas', label: 'Estadísticas', icono: 'pi-chart-bar' },
  { id: 'doctores', label: 'Doctores', icono: 'pi-users' },
  { id: 'pacientes', label: 'Pacientes', icono: 'pi-user' },
]

const especialidades = [
  'Medicina General', 'Pediatría', 'Cardiología', 'Dermatología',
  'Neurología', 'Ginecología', 'Oftalmología', 'Odontología',
  'Ortopedia', 'Psiquiatría', 'Endocrinología'
]

const nuevoDoctor = ref({ nombre: '', especialidad: '', email: '', telefono: '', password: '' })

const carruselItems = [
  { icono: 'pi pi-shield', texto: 'Panel Administrativo' },
  { icono: 'pi pi-users', texto: 'Gestión de Doctores' },
  { icono: 'pi pi-calendar', texto: 'Control de Citas' },
  { icono: 'pi pi-chart-bar', texto: 'Estadísticas en Tiempo Real' },
  { icono: 'pi pi-check-circle', texto: 'Confirmar Citas' },
  { icono: 'pi pi-database', texto: 'Base de Datos Activa' },
  { icono: 'pi pi-clock', texto: 'Monitoreo 24/7' },
  { icono: 'pi pi-heart', texto: 'FastCitas Colombia' },
]

const coloresBarra = ['#388bfd', '#3fb950', '#fbbf24', '#a78bfa', '#f97316', '#ec4899']
const coloresEspecialidad = {
  'Medicina General': '#1a3a6e', 'Pediatría': '#1a4a3a', 'Cardiología': '#4a1a1a',
  'Dermatología': '#3a2a1a', 'Neurología': '#2a1a4a', 'Ginecología': '#3a1a3a',
  'Oftalmología': '#1a3a4a', 'Odontología': '#2a3a1a',
}
const colorAvatar = (esp) => coloresEspecialidad[esp] || '#1a3a6e'

const saludo = computed(() => {
  const h = new Date().getHours()
  if (h >= 5 && h < 12) return 'Buenos días'
  if (h >= 12 && h < 18) return 'Buenas tardes'
  return 'Buenas noches'
})

const actualizarReloj = () => {
  const ahora = new Date()
  horaActual.value = ahora.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  fechaActual.value = ahora.toLocaleDateString('es-CO', { weekday: 'long', day: 'numeric', month: 'long' })
}

// STATS con filtro al hacer clic
const stats = computed(() => [
  {
    label: 'Total citas', valor: citas.value.length,
    icono: 'pi-calendar', color: '#388bfd', bg: 'rgba(56,139,253,0.08)', borde: 'rgba(56,139,253,0.2)',
    filtro: '', accion: 'Ver todas las citas'
  },
  {
    label: 'Pendientes', valor: citas.value.filter(c => c.estado === 'pendiente').length,
    icono: 'pi-clock', color: '#fbbf24', bg: 'rgba(251,191,36,0.08)', borde: 'rgba(251,191,36,0.2)',
    filtro: 'pendiente', accion: 'Ver citas pendientes'
  },
  {
    label: 'Confirmadas', valor: citas.value.filter(c => c.estado === 'confirmada').length,
    icono: 'pi-check-circle', color: '#3fb950', bg: 'rgba(63,185,80,0.08)', borde: 'rgba(63,185,80,0.2)',
    filtro: 'confirmada', accion: 'Ver citas confirmadas'
  },
  {
    label: 'Doctores', valor: doctores.value.length,
    icono: 'pi-users', color: '#a78bfa', bg: 'rgba(167,139,250,0.08)', borde: 'rgba(167,139,250,0.2)',
    filtro: null, accion: 'Ver doctores'  // este navega al tab doctores
  },
])

const aplicarFiltroStat = (filtro) => {
  if (filtro === null) {
    // Card de doctores → navegar al tab
    tabActivo.value = 'doctores'
    return
  }
  tabActivo.value = 'citas'
  if (filtroEstadoActivo.value === filtro) {
    // Doble clic = quitar filtro
    filtroEstadoActivo.value = null
    filtroEstado.value = ''
  } else {
    filtroEstadoActivo.value = filtro
    filtroEstado.value = filtro
  }
}

const limpiarFiltroStat = () => {
  filtroEstadoActivo.value = null
  filtroEstado.value = ''
}

const limpiarTodosFiltros = () => {
  filtroEstadoActivo.value = null
  filtroEstado.value = ''
  busquedaCitas.value = ''
}

// FILTROS computados
const citasFiltradas = computed(() => {
  let lista = citas.value
  if (filtroEstado.value) lista = lista.filter(c => c.estado === filtroEstado.value)
  if (busquedaCitas.value.trim()) {
    const q = busquedaCitas.value.toLowerCase()
    lista = lista.filter(c =>
      c.paciente_nombre?.toLowerCase().includes(q) ||
      c.doctor_nombre?.toLowerCase().includes(q) ||
      c.especialidad?.toLowerCase().includes(q)
    )
  }
  return lista
})

const doctoresFiltrados = computed(() => {
  if (!busquedaDoctores.value.trim()) return doctores.value
  const q = busquedaDoctores.value.toLowerCase()
  return doctores.value.filter(d =>
    d.nombre?.toLowerCase().includes(q) || d.especialidad?.toLowerCase().includes(q)
  )
})

const pacientesFiltrados = computed(() => {
  if (!busquedaPacientes.value.trim()) return pacientes.value
  const q = busquedaPacientes.value.toLowerCase()
  return pacientes.value.filter(p =>
    p.nombre?.toLowerCase().includes(q) || p.email?.toLowerCase().includes(q)
  )
})

// GRÁFICAS
const donaSegmento = (estado) => {
  if (citas.value.length === 0) return 0
  return (citas.value.filter(c => c.estado === estado).length / citas.value.length) * 283
}

const citasPorEspecialidad = computed(() => {
  const mapa = {}
  citas.value.forEach(c => { if (c.especialidad) mapa[c.especialidad] = (mapa[c.especialidad] || 0) + 1 })
  return Object.entries(mapa).map(([especialidad, total]) => ({ especialidad, total }))
    .sort((a, b) => b.total - a.total).slice(0, 6)
})

const maxEspecialidad = computed(() =>
  citasPorEspecialidad.value.length > 0 ? Math.max(...citasPorEspecialidad.value.map(i => i.total)) : 1
)

// MENÚ USUARIO
const abrirPerfil = () => {
  menuUsuarioAbierto.value = false
  mostrarPerfil.value = true
}

const abrirCambiarContrasena = () => {
  menuUsuarioAbierto.value = false
  mostrarCambioContrasena.value = true
}

const cerrarModalContrasena = () => {
  mostrarCambioContrasena.value = false
  pasoContrasena.value = 1
  emailCambio.value = ''
  nuevaContrasena.value = ''
  confirmarContrasena.value = ''
  errorContrasena.value = ''
}

const verificarEmailAdmin = async () => {
  if (!emailCambio.value) {
    notificacion.add({ severity: 'warn', summary: 'Atención', detail: 'Ingresa tu correo', life: 3000 })
    return
  }
  cargandoModal.value = true
  try {
    const res = await axios.get('/auth/usuarios')
    const existe = res.data.find(u => u.email === emailCambio.value)
    if (!existe) {
      notificacion.add({ severity: 'error', summary: 'No encontrado', detail: 'No existe una cuenta con ese correo', life: 3000 })
      return
    }
    pasoContrasena.value = 2
  } catch {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo verificar', life: 3000 })
  } finally {
    cargandoModal.value = false
  }
}

const cambiarContrasena = async () => {
  errorContrasena.value = ''
  if (!nuevaContrasena.value || nuevaContrasena.value.length < 6) {
    errorContrasena.value = 'La contraseña debe tener al menos 6 caracteres'
    return
  }
  if (nuevaContrasena.value !== confirmarContrasena.value) {
    errorContrasena.value = 'Las contraseñas no coinciden'
    return
  }
  cargandoModal.value = true
  try {
    await axios.put('/auth/cambiar-password', { email: emailCambio.value, nueva_password: nuevaContrasena.value })
    pasoContrasena.value = 3
  } catch (e) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: e.response?.data?.detail || 'No se pudo cambiar', life: 3000 })
  } finally {
    cargandoModal.value = false
  }
}

// API
const obtenerCitas = async () => {
  cargandoCitas.value = true
  try { const res = await axios.get('/citas/'); citas.value = res.data }
  catch { notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las citas', life: 3000 }) }
  finally { cargandoCitas.value = false }
}

const obtenerDoctores = async () => {
  cargandoDoctores.value = true
  try { const res = await axios.get('/doctores/'); doctores.value = res.data }
  catch { notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los doctores', life: 3000 }) }
  finally { cargandoDoctores.value = false }
}

const obtenerPacientes = async () => {
  cargandoPacientes.value = true
  try { const res = await axios.get('/auth/usuarios'); pacientes.value = res.data.filter(u => u.rol === 'paciente') }
  catch { pacientes.value = [] }
  finally { cargandoPacientes.value = false }
}

const registrarDoctor = async () => {
  const { nombre, especialidad, email, telefono, password } = nuevoDoctor.value
  if (!nombre || !especialidad || !email || !telefono || !password) {
    notificacion.add({ severity: 'warn', summary: 'Campos requeridos', detail: 'Completa todos los campos', life: 3000 })
    return
  }
  guardando.value = true
  try {
    await axios.post('/auth/register', { nombre, especialidad, email, telefono, password, rol: 'doctor' })
    notificacion.add({ severity: 'success', summary: '¡Doctor registrado!', detail: `${nombre} agregado`, life: 3000 })
    nuevoDoctor.value = { nombre: '', especialidad: '', email: '', telefono: '', password: '' }
    mostrarFormDoctor.value = false
    await obtenerDoctores()
  } catch (e) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: e.response?.data?.detail || 'No se pudo registrar', life: 3000 })
  } finally { guardando.value = false }
}

const cambiarEstado = async (id, estado) => {
  try {
    await axios.put(`/citas/${id}/estado?estado=${estado}`)
    notificacion.add({ severity: 'success', summary: 'Estado actualizado', detail: `Cita marcada como ${estado}`, life: 3000 })
    await obtenerCitas()
  } catch { notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo actualizar', life: 3000 }) }
}

const eliminarCita = async (id) => {
  try {
    await axios.delete(`/citas/${id}`)
    notificacion.add({ severity: 'info', summary: 'Cita eliminada', detail: 'La cita fue eliminada', life: 3000 })
    await obtenerCitas()
  } catch { notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar', life: 3000 }) }
}

const cerrarSesion = () => { localStorage.removeItem('usuario'); enrutador.push('/login') }

// Directiva click-outside
const vClickOutside = {
  mounted(el, binding) {
    el._clickOutside = (e) => { if (!el.contains(e.target)) binding.value(e) }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) { document.removeEventListener('click', el._clickOutside) }
}

onMounted(() => {
  obtenerCitas(); obtenerDoctores(); obtenerPacientes()
  actualizarReloj()
  intervaloReloj = setInterval(actualizarReloj, 1000)
})
onUnmounted(() => clearInterval(intervaloReloj))
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }

.pagina-admin { min-height: 100vh; background: #080c14; color: #e6edf3; }

/* NAVBAR */
.navbar { background: #0d1117; border-bottom: 1px solid #21262d; padding: 0.9rem 2rem; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
.nav-logo { display: flex; align-items: center; gap: 0.7rem; }
.nav-nombre { font-size: 1.1rem; font-weight: 700; color: #e6edf3; letter-spacing: -0.5px; }
.nav-badge { font-size: 0.65rem; font-weight: 700; color: #388bfd; background: rgba(56,139,253,0.1); border: 1px solid rgba(56,139,253,0.2); padding: 0.15rem 0.5rem; border-radius: 99px; text-transform: uppercase; }
.nav-derecha { display: flex; align-items: center; gap: 1rem; }

/* MENÚ USUARIO */
.nav-usuario {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 0.4rem 0.8rem; border-radius: 10px; cursor: pointer;
  border: 1px solid transparent; transition: all 0.2s; position: relative;
}
.nav-usuario:hover { background: #161b22; border-color: #21262d; }
.avatar { width: 32px; height: 32px; background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700; color: #60a5fa; flex-shrink: 0; }
.nav-saludo { font-size: 0.85rem; color: #8b949e; }
.nav-chevron { font-size: 0.65rem; color: #484f58; transition: transform 0.2s; }

.menu-usuario {
  position: absolute; top: calc(100% + 8px); right: 0;
  background: #0d1117; border: 1px solid #21262d; border-radius: 14px;
  padding: 0.5rem; min-width: 220px;
  box-shadow: 0 16px 48px rgba(0,0,0,0.5); z-index: 200;
}
.menu-header { display: flex; align-items: center; gap: 0.8rem; padding: 0.6rem 0.5rem 0.8rem; }
.menu-avatar-grande { width: 38px; height: 38px; background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 700; color: #60a5fa; flex-shrink: 0; }
.menu-nombre { font-size: 0.85rem; font-weight: 600; color: #e6edf3; }
.menu-rol { font-size: 0.7rem; color: #484f58; margin-top: 0.1rem; }
.menu-separador { height: 1px; background: #21262d; margin: 0.3rem 0; }
.menu-item {
  display: flex; align-items: center; gap: 0.6rem; width: 100%;
  padding: 0.55rem 0.7rem; background: transparent; border: none; border-radius: 8px;
  color: #8b949e; font-size: 0.82rem; font-family: 'Inter', sans-serif;
  cursor: pointer; transition: all 0.15s; text-align: left;
}
.menu-item:hover { background: #161b22; color: #e6edf3; }
.menu-item i { font-size: 0.8rem; width: 16px; }
.menu-item-rojo:hover { background: rgba(248,81,73,0.08); color: #f85149; }

/* PULSO */
.pulso-linea { stroke-dasharray: 80; stroke-dashoffset: 80; animation: dibujarPulso 2s ease-in-out infinite; }
.pulso-delay { animation-delay: 0.4s; }
@keyframes dibujarPulso { 0% { stroke-dashoffset: 80; opacity: 0; } 10% { opacity: 1; } 50% { stroke-dashoffset: 0; opacity: 1; } 80% { stroke-dashoffset: 0; opacity: 0.3; } 100% { stroke-dashoffset: 80; opacity: 0; } }

/* CARRUSEL */
.carrusel-wrapper { width: 100%; background: #0d1117; border-bottom: 1px solid #161b22; padding: 0.55rem 0; overflow: hidden; }
.carrusel-track { display: flex; gap: 3rem; animation: deslizar 32s linear infinite; width: max-content; }
.carrusel-item { display: flex; align-items: center; gap: 0.45rem; color: #30363d; font-size: 0.75rem; font-weight: 500; white-space: nowrap; }
.carrusel-item i { color: #1d4ed8; font-size: 0.7rem; }
@keyframes deslizar { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

/* HERO */
.hero-banner { max-width: 960px; margin: 1.8rem auto 0; padding: 0 1.5rem; display: flex; justify-content: space-between; align-items: center; gap: 1.5rem; }
.hero-izq { flex: 1; }
.hero-saludo-fila { display: flex; align-items: baseline; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.5rem; }
.hero-saludo-texto { font-size: 1.6rem; font-weight: 300; color: #8b949e; }
.hero-nombre-texto { font-size: 1.6rem; font-weight: 700; color: #e6edf3; }
.hero-punto { font-size: 1.6rem; font-weight: 700; color: #388bfd; }
.hero-sub { font-size: 0.82rem; color: #484f58; margin-bottom: 1rem; font-style: italic; }
.hero-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.hero-chip { display: flex; align-items: center; gap: 0.35rem; padding: 0.25rem 0.7rem; background: #0d1117; border: 1px solid #21262d; border-radius: 99px; font-size: 0.7rem; color: #484f58; }
.chip-verde { border-color: rgba(63,185,80,0.2); color: #3fb950; }
.chip-verde i { color: #3fb950; font-size: 0.5rem; }
.chip-amarillo { border-color: rgba(251,191,36,0.25); color: #fbbf24; }
.hero-der { display: flex; flex-direction: column; align-items: flex-end; gap: 0.8rem; flex-shrink: 0; }
.reloj-bloque { text-align: right; }
.reloj-hora { font-size: 2rem; font-weight: 700; color: #e6edf3; letter-spacing: -1px; line-height: 1; font-variant-numeric: tabular-nums; }
.reloj-fecha { font-size: 0.72rem; color: #484f58; text-transform: capitalize; margin-top: 0.2rem; }
.hero-stat-mini { display: flex; gap: 0.7rem; }
.mini-stat { display: flex; align-items: center; gap: 0.35rem; padding: 0.3rem 0.7rem; background: rgba(56,139,253,0.06); border: 1px solid rgba(56,139,253,0.12); border-radius: 8px; font-size: 0.72rem; color: #388bfd; }

/* CONTENIDO */
.contenido { max-width: 960px; margin: 0 auto; padding: 1.5rem 1.5rem 2rem; display: flex; flex-direction: column; gap: 1.5rem; }

/* STATS CLICABLES */
.grid-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.stat-card {
  background: #0d1117; border: 1px solid #21262d; border-radius: 14px;
  padding: 1.1rem; display: flex; align-items: center; gap: 0.9rem;
  transition: border-color 0.2s, transform 0.2s, background 0.2s;
  user-select: none;
}
.stat-card:hover { border-color: #388bfd; transform: translateY(-3px); background: rgba(56,139,253,0.03); }
.stat-activa { border-color: #388bfd !important; background: rgba(56,139,253,0.06) !important; }
.stat-icono { width: 40px; height: 40px; border: 1px solid; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.stat-num { font-size: 1.5rem; font-weight: 700; color: #e6edf3; line-height: 1; margin-bottom: 0.15rem; }
.stat-label { font-size: 0.72rem; color: #484f58; }
.stat-hint, .stat-flecha { margin-left: auto; flex-shrink: 0; }

/* BANNER FILTRO ACTIVO */
.filtro-activo-banner {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 0.55rem 1rem; background: rgba(56,139,253,0.06);
  border: 1px solid rgba(56,139,253,0.15); border-radius: 10px;
  font-size: 0.78rem; color: #8b949e;
}
.filtro-activo-banner strong { color: #388bfd; }
.filtro-activo-banner i { color: #388bfd; font-size: 0.75rem; }
.filtro-limpiar {
  margin-left: auto; display: flex; align-items: center; gap: 0.3rem;
  padding: 0.25rem 0.65rem; background: transparent; border: 1px solid #30363d;
  border-radius: 6px; color: #484f58; font-size: 0.72rem; font-family: 'Inter', sans-serif;
  cursor: pointer; transition: all 0.2s;
}
.filtro-limpiar:hover { border-color: #f85149; color: #f85149; }

/* TABS */
.tabs-wrapper { display: flex; gap: 0.5rem; border-bottom: 1px solid #21262d; }
.tab-btn { display: flex; align-items: center; gap: 0.4rem; padding: 0.6rem 1.1rem; background: transparent; border: none; border-bottom: 2px solid transparent; color: #484f58; font-size: 0.85rem; font-weight: 500; font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.2s; margin-bottom: -1px; }
.tab-btn:hover { color: #8b949e; }
.tab-btn.activo { color: #388bfd; border-bottom-color: #388bfd; }
.tab-badge { background: #fbbf24; color: #080c14; font-size: 0.6rem; font-weight: 800; padding: 0.1rem 0.4rem; border-radius: 99px; margin-left: 0.2rem; }

/* CARDS */
.seccion-card { background: #0d1117; border: 1px solid #21262d; border-radius: 16px; padding: 1.8rem; }
.card-cabeza { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1.2rem; border-bottom: 1px solid #161b22; flex-wrap: wrap; }
.cabeza-icono { font-size: 1.3rem; color: #388bfd; background: rgba(56,139,253,0.08); border: 1px solid rgba(56,139,253,0.15); padding: 0.6rem; border-radius: 10px; }
.card-titulo { font-size: 1rem; font-weight: 600; color: #e6edf3; margin-bottom: 0.15rem; }
.card-sub { font-size: 0.78rem; color: #484f58; }

/* BUSCADOR */
.buscador-wrap { position: relative; display: flex; align-items: center; }
.buscador-icono { position: absolute; left: 0.7rem; color: #484f58; font-size: 0.75rem; pointer-events: none; }
.buscador-inp { padding: 0.42rem 0.75rem 0.42rem 2rem; background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; font-size: 0.8rem; font-family: 'Inter', sans-serif; outline: none; width: 220px; transition: border-color 0.2s; }
.buscador-inp:focus { border-color: #388bfd; }
.buscador-inp::placeholder { color: #30363d; }

.boton-nuevo { display: flex; align-items: center; gap: 0.4rem; margin-left: auto; padding: 0.45rem 1rem; background: rgba(56,139,253,0.1); border: 1px solid rgba(56,139,253,0.25); border-radius: 8px; color: #388bfd; font-size: 0.8rem; font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.2s; }
.boton-nuevo:hover { background: rgba(56,139,253,0.18); border-color: #388bfd; }

.form-nuevo { background: #0a0f1a; border: 1px solid #21262d; border-radius: 12px; padding: 1.3rem; margin-bottom: 1.5rem; }
.form-grid-4 { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.campo label { display: block; font-size: 0.75rem; font-weight: 500; color: #8b949e; margin-bottom: 0.35rem; }
.inp { width: 100%; padding: 0.5rem 0.75rem; background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; font-size: 0.82rem; font-family: 'Inter', sans-serif; transition: border-color 0.2s; outline: none; }
.inp:focus { border-color: #388bfd; }
.inp option { background: #161b22; }
.form-acciones { display: flex; gap: 0.7rem; justify-content: flex-end; }
.boton-cancelar-form { padding: 0.5rem 1rem; background: transparent; border: 1px solid #21262d; border-radius: 8px; color: #8b949e; font-size: 0.82rem; font-family: 'Inter', sans-serif; cursor: pointer; }
.boton-guardar { display: flex; align-items: center; gap: 0.4rem; padding: 0.5rem 1.2rem; background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 8px; color: #e6edf3; font-size: 0.82rem; font-family: 'Inter', sans-serif; cursor: pointer; }
.boton-guardar:disabled { opacity: 0.4; cursor: not-allowed; }

.doctores-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
.doctor-card { background: #0a0f1a; border: 1px solid #21262d; border-radius: 12px; padding: 1.1rem; display: flex; flex-direction: column; align-items: center; gap: 0.6rem; text-align: center; transition: border-color 0.2s, transform 0.2s; }
.doctor-card:hover { border-color: #30363d; transform: translateY(-2px); }
.doctor-avatar { width: 52px; height: 52px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 700; color: #e6edf3; border: 2px solid rgba(255,255,255,0.08); }
.doctor-nombre { font-size: 0.82rem; font-weight: 600; color: #e6edf3; }
.doctor-especialidad { font-size: 0.72rem; color: #388bfd; font-weight: 500; }
.doctor-contacto { font-size: 0.68rem; color: #484f58; display: flex; align-items: center; gap: 0.3rem; justify-content: center; }

.inp-mini { padding: 0.4rem 0.75rem; background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; font-size: 0.78rem; font-family: 'Inter', sans-serif; outline: none; }
.inp-mini option { background: #161b22; }

.citas-lista { display: flex; flex-direction: column; gap: 0.7rem; }
.cita-fila { display: flex; align-items: center; gap: 1rem; padding: 0.85rem 1rem; background: #0a0f1a; border: 1px solid #21262d; border-radius: 10px; transition: border-color 0.2s; }
.cita-fila:hover { border-color: #30363d; }
.cita-avatar { width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 700; color: #e6edf3; }
.cita-info { flex: 1; min-width: 0; }
.cita-doctor { font-size: 0.83rem; font-weight: 600; color: #e6edf3; }
.cita-detalle { font-size: 0.7rem; color: #484f58; margin-top: 0.08rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.badge-estado { padding: 0.22rem 0.6rem; border-radius: 99px; font-size: 0.7rem; font-weight: 600; text-transform: capitalize; flex-shrink: 0; }
.estado-pendiente { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.25); color: #fbbf24; }
.estado-confirmada { background: rgba(63,185,80,0.1); border: 1px solid rgba(63,185,80,0.25); color: #3fb950; }
.estado-cancelada { background: rgba(248,81,73,0.1); border: 1px solid rgba(248,81,73,0.25); color: #f85149; }
.badge-citas-pac { display: flex; align-items: center; gap: 0.3rem; font-size: 0.7rem; color: #388bfd; flex-shrink: 0; }

.acciones-cita { display: flex; gap: 0.4rem; flex-shrink: 0; }
.btn-accion { width: 30px; height: 30px; border-radius: 7px; border: 1px solid #21262d; background: transparent; color: #484f58; cursor: pointer; font-size: 0.75rem; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
.btn-accion.confirmar:hover { border-color: #3fb950; color: #3fb950; background: rgba(63,185,80,0.06); }
.btn-accion.cancelar:hover { border-color: #fbbf24; color: #fbbf24; background: rgba(251,191,36,0.06); }
.btn-accion.eliminar:hover { border-color: #f85149; color: #f85149; background: rgba(248,81,73,0.06); }

.sin-citas { text-align: center; padding: 3rem 1rem; display: flex; flex-direction: column; align-items: center; gap: 0.6rem; }
.sin-citas-icono { width: 56px; height: 56px; background: rgba(56,139,253,0.06); border: 1px solid rgba(56,139,253,0.12); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; color: #388bfd; margin-bottom: 0.5rem; }
.sin-citas-titulo { font-size: 0.95rem; font-weight: 600; color: #484f58; }
.sin-citas-sub { font-size: 0.78rem; color: #30363d; }
.btn-limpiar-todo { margin-top: 0.5rem; padding: 0.4rem 1rem; background: transparent; border: 1px solid #21262d; border-radius: 8px; color: #388bfd; font-size: 0.78rem; font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.2s; }
.btn-limpiar-todo:hover { border-color: #388bfd; background: rgba(56,139,253,0.06); }
.lista-skeleton { display: flex; flex-direction: column; gap: 0.7rem; }

/* ESTADÍSTICAS */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
.dona-wrap { display: flex; align-items: center; justify-content: center; gap: 2rem; padding: 1rem 0; }
.dona-svg { width: 130px; height: 130px; flex-shrink: 0; }
.dona-leyenda { display: flex; flex-direction: column; gap: 0.8rem; }
.leyenda-item { display: flex; align-items: center; gap: 0.6rem; }
.leyenda-clicable { cursor: pointer; padding: 0.3rem 0.5rem; border-radius: 8px; transition: background 0.2s; }
.leyenda-clicable:hover { background: rgba(56,139,253,0.06); }
.leyenda-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.leyenda-label { font-size: 0.78rem; color: #8b949e; flex: 1; }
.leyenda-val { font-size: 0.85rem; font-weight: 700; color: #e6edf3; }
.barras-wrap { display: flex; flex-direction: column; gap: 0.8rem; padding: 0.5rem 0; }
.barra-fila { display: flex; align-items: center; gap: 0.8rem; }
.barra-clicable { cursor: pointer; padding: 0.3rem; border-radius: 8px; transition: background 0.2s; }
.barra-clicable:hover { background: rgba(56,139,253,0.04); }
.barra-label { font-size: 0.72rem; color: #8b949e; width: 120px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.barra-track { flex: 1; height: 8px; background: #161b22; border-radius: 99px; overflow: hidden; }
.barra-fill { height: 100%; border-radius: 99px; transition: width 1s ease; }
.barra-num { font-size: 0.75rem; font-weight: 700; color: #e6edf3; width: 20px; text-align: right; flex-shrink: 0; }

/* MODALES */
.modal-overlay { position: fixed; inset: 0; z-index: 200; background: rgba(8,12,20,0.85); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; padding: 1.5rem; }
.modal-caja { width: 100%; max-width: 400px; background: #0d1117; border: 1px solid #21262d; border-radius: 18px; padding: 2rem; box-shadow: 0 24px 80px rgba(0,0,0,0.6); }
.modal-cabeza { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.modal-icono { width: 44px; height: 44px; border-radius: 12px; flex-shrink: 0; background: rgba(56,139,253,0.1); border: 1px solid rgba(56,139,253,0.2); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #388bfd; }
.modal-icono-ok { background: rgba(63,185,80,0.1); border-color: rgba(63,185,80,0.2); color: #3fb950; }
.modal-titulo { font-size: 0.95rem; font-weight: 700; color: #e6edf3; margin-bottom: 0.2rem; }
.modal-sub { font-size: 0.75rem; color: #484f58; }
.modal-sub strong { color: #8b949e; }
.modal-cerrar { margin-left: auto; background: transparent; border: none; color: #484f58; font-size: 0.9rem; cursor: pointer; padding: 0.3rem; border-radius: 6px; transition: color 0.2s; flex-shrink: 0; }
.modal-cerrar:hover { color: #e6edf3; }
.modal-acciones { display: flex; gap: 0.7rem; margin-top: 1.3rem; }
.btn-modal-cancelar { flex: 1; padding: 0.55rem; background: transparent; border: 1px solid #21262d; border-radius: 8px; color: #8b949e; font-size: 0.82rem; font-family: 'Inter', sans-serif; cursor: pointer; }
.btn-modal-ok { flex: 1; padding: 0.55rem; background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 8px; color: #e6edf3; font-size: 0.82rem; font-weight: 600; font-family: 'Inter', sans-serif; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.4rem; transition: all 0.2s; }
.btn-modal-ok:hover:not(:disabled) { background: #1d4ed8; border-color: #388bfd; }
.btn-modal-ok:disabled { opacity: 0.4; cursor: not-allowed; }
.aviso-modal { color: #f85149; font-size: 0.75rem; margin-top: 0.6rem; display: flex; align-items: center; gap: 0.4rem; }
.modal-exito { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 0.5rem; padding: 1rem 0; }
.exito-icono { font-size: 2.5rem; color: #3fb950; margin-bottom: 0.5rem; }
.exito-titulo { font-size: 1rem; font-weight: 700; color: #e6edf3; }
.exito-sub { font-size: 0.78rem; color: #484f58; }

/* PERFIL */
.perfil-datos { display: flex; flex-direction: column; gap: 0.7rem; }
.perfil-avatar-grande { width: 64px; height: 64px; background: #1a3a6e; border: 2px solid #2d5fa8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700; color: #60a5fa; margin: 0 auto 0.5rem; }
.perfil-fila { display: flex; align-items: center; justify-content: space-between; padding: 0.55rem 0; border-bottom: 1px solid #161b22; }
.perfil-key { font-size: 0.78rem; color: #484f58; display: flex; align-items: center; gap: 0.4rem; }
.perfil-val { font-size: 0.82rem; font-weight: 500; color: #e6edf3; }

/* TRANSICIONES */
.deslizar-enter-active { transition: opacity 0.35s ease, transform 0.35s ease; }
.deslizar-enter-from { opacity: 0; transform: translateY(-12px); }
.lista-enter-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.lista-enter-from { opacity: 0; transform: translateX(-10px); }
.lista-leave-active { transition: opacity 0.2s; }
.lista-leave-to { opacity: 0; }
.modal-fade-enter-active { transition: opacity 0.25s ease, transform 0.25s ease; }
.modal-fade-enter-from { opacity: 0; transform: scale(0.96); }
.modal-fade-leave-active { transition: opacity 0.2s; }
.modal-fade-leave-to { opacity: 0; }
.menu-drop-enter-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.menu-drop-enter-from { opacity: 0; transform: translateY(-8px); }
.menu-drop-leave-active { transition: opacity 0.15s; }
.menu-drop-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .grid-stats { grid-template-columns: repeat(2, 1fr); }
  .grid-2 { grid-template-columns: 1fr; }
  .doctores-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-banner { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .hero-der { align-items: flex-start; }
  .reloj-hora { font-size: 1.5rem; }
  .navbar { padding: 0.9rem 1rem; }
  .nav-saludo { display: none; }
  .buscador-inp { width: 160px; }
}
</style>