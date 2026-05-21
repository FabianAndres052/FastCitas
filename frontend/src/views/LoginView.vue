<template>
  <div class="pagina-login">
    <div class="fondo-grid"></div>

    <div class="carrusel-wrapper">
      <div class="carrusel-track">
        <span v-for="(item, i) in carruselItems.concat(carruselItems)" :key="i" class="carrusel-item">
          <i :class="item.icono"></i> {{ item.texto }}
        </span>
      </div>
    </div>

    <div class="centro">
      <div class="logo-bloque">
        <div class="logo-svg-wrap">
          <svg viewBox="0 0 80 80" width="64" height="64" xmlns="http://www.w3.org/2000/svg">
            <polygon points="40,2 76,21 76,59 40,78 4,59 4,21" fill="none" stroke="#1a2744" stroke-width="1"/>
            <rect x="29" y="14" width="22" height="52" rx="7" fill="#1a3a6e"/>
            <rect x="14" y="29" width="52" height="22" rx="7" fill="#1a3a6e"/>
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
        <div class="logo-texto-wrap">
          <h1 class="logo-nombre">FastCitas</h1>
          <p class="logo-sub">Agendamiento médico digital</p>
        </div>
      </div>

      <div class="tarjeta">
        <p class="tarjeta-titulo">Iniciar sesión</p>

        <div class="campo">
          <label>Correo electrónico</label>
          <InputText v-model="correo" placeholder="correo@ejemplo.com" class="inp" :disabled="cargando" />
        </div>

        <div class="campo">
          <label>Contraseña</label>
          <InputText v-model="contrasena" type="password" placeholder="••••••••" class="inp" :disabled="cargando" />
        </div>

        <!-- LINK OLVIDÉ CONTRASEÑA -->
        <div class="fila-olvide">
          <span class="link-olvide" @click="mostrarModalContrasena = true">
            <i class="pi pi-lock"></i> ¿Olvidaste tu contraseña?
          </span>
        </div>

        <button class="boton-entrar" @click="iniciarSesion" :disabled="cargando">
          <span v-if="!cargando" class="boton-contenido">
            Entrar <i class="pi pi-arrow-right icono-boton"></i>
          </span>
          <span v-else class="boton-contenido">
            <i class="pi pi-spin pi-spinner"></i> Cargando...
          </span>
          <span class="boton-brillo"></span>
        </button>

        <p class="pie">
          ¿Sin cuenta? <span @click="$router.push('/registro')">Regístrate</span>
        </p>
      </div>
    </div>

    <!-- MODAL OLVIDÉ / CAMBIAR CONTRASEÑA -->
    <Transition name="modal-fade">
      <div class="modal-overlay" v-if="mostrarModalContrasena" @click.self="cerrarModal">
        <div class="modal-caja">

          <!-- PASO 1: ingresar email -->
          <div v-if="pasoModal === 1">
            <div class="modal-cabeza">
              <div class="modal-icono"><i class="pi pi-lock"></i></div>
              <div>
                <p class="modal-titulo">Restablecer contraseña</p>
                <p class="modal-sub">Ingresa tu correo registrado</p>
              </div>
            </div>
            <div class="campo">
              <label>Correo electrónico</label>
              <InputText v-model="emailRecupero" placeholder="correo@ejemplo.com" class="inp" :disabled="cargandoModal" />
            </div>
            <div class="modal-acciones">
              <button class="btn-modal-cancelar" @click="cerrarModal">Cancelar</button>
              <button class="btn-modal-ok" @click="verificarEmail" :disabled="cargandoModal">
                <span v-if="!cargandoModal"><i class="pi pi-arrow-right"></i> Continuar</span>
                <span v-else><i class="pi pi-spin pi-spinner"></i> Verificando...</span>
              </button>
            </div>
          </div>

          <!-- PASO 2: nueva contraseña -->
          <div v-if="pasoModal === 2">
            <div class="modal-cabeza">
              <div class="modal-icono modal-icono-ok"><i class="pi pi-check"></i></div>
              <div>
                <p class="modal-titulo">Nueva contraseña</p>
                <p class="modal-sub">Cuenta encontrada para <strong>{{ emailRecupero }}</strong></p>
              </div>
            </div>
            <div class="campo">
              <label>Nueva contraseña</label>
              <InputText v-model="nuevaContrasena" type="password" placeholder="Mínimo 6 caracteres" class="inp" :disabled="cargandoModal" />
            </div>
            <div class="campo">
              <label>Confirmar contraseña</label>
              <InputText v-model="confirmarContrasena" type="password" placeholder="Repite la contraseña" class="inp" :disabled="cargandoModal" />
            </div>
            <Transition name="fade">
              <p class="aviso-modal" v-if="errorContrasena">
                <i class="pi pi-exclamation-triangle"></i> {{ errorContrasena }}
              </p>
            </Transition>
            <div class="modal-acciones">
              <button class="btn-modal-cancelar" @click="pasoModal = 1">Atrás</button>
              <button class="btn-modal-ok" @click="cambiarContrasena" :disabled="cargandoModal">
                <span v-if="!cargandoModal"><i class="pi pi-check"></i> Guardar</span>
                <span v-else><i class="pi pi-spin pi-spinner"></i> Guardando...</span>
              </button>
            </div>
          </div>

          <!-- PASO 3: éxito -->
          <div v-if="pasoModal === 3" class="modal-exito">
            <div class="exito-icono"><i class="pi pi-check-circle"></i></div>
            <p class="exito-titulo">¡Contraseña actualizada!</p>
            <p class="exito-sub">Ya puedes iniciar sesión con tu nueva contraseña</p>
            <button class="btn-modal-ok" @click="cerrarModal" style="margin-top:1.2rem; width:100%">
              <i class="pi pi-arrow-right"></i> Ir al login
            </button>
          </div>

        </div>
      </div>
    </Transition>

    <Toast />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import axios from 'axios'

const enrutador = useRouter()
const notificacion = useToast()

const correo = ref('')
const contrasena = ref('')
const cargando = ref(false)

// Modal estado
const mostrarModalContrasena = ref(false)
const pasoModal = ref(1)
const emailRecupero = ref('')
const nuevaContrasena = ref('')
const confirmarContrasena = ref('')
const cargandoModal = ref(false)
const errorContrasena = ref('')

const carruselItems = ref([
  { icono: 'pi pi-heart', texto: 'Medicina General' },
  { icono: 'pi pi-star', texto: 'Pediatría' },
  { icono: 'pi pi-heart-fill', texto: 'Cardiología' },
  { icono: 'pi pi-eye', texto: 'Oftalmología' },
  { icono: 'pi pi-user', texto: 'Dermatología' },
  { icono: 'pi pi-verified', texto: 'Ginecología' },
  { icono: 'pi pi-shield', texto: 'Odontología' },
  { icono: 'pi pi-plus', texto: 'Neurología' },
])

const iniciarSesion = async () => {
  if (!correo.value || !contrasena.value) {
    notificacion.add({ severity: 'warn', summary: 'Atención', detail: 'Completa todos los campos', life: 3000 })
    return
  }
  cargando.value = true
  try {
    const respuesta = await axios.post('/auth/login', { email: correo.value, password: contrasena.value })
    localStorage.setItem('usuario', JSON.stringify(respuesta.data.usuario))
    notificacion.add({ severity: 'success', summary: '¡Bienvenido!', detail: respuesta.data.usuario.nombre, life: 2000 })
    setTimeout(() => {
      if (respuesta.data.usuario.rol === 'admin') enrutador.push('/admin')
      else enrutador.push('/inicio')
    }, 1500)
  } catch (error) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Credenciales incorrectas', life: 3000 })
  } finally {
    cargando.value = false
  }
}

const cerrarModal = () => {
  mostrarModalContrasena.value = false
  pasoModal.value = 1
  emailRecupero.value = ''
  nuevaContrasena.value = ''
  confirmarContrasena.value = ''
  errorContrasena.value = ''
}

const verificarEmail = async () => {
  if (!emailRecupero.value) {
    notificacion.add({ severity: 'warn', summary: 'Atención', detail: 'Ingresa tu correo', life: 3000 })
    return
  }
  cargandoModal.value = true
  try {
    // Verificamos que el correo exista usando el endpoint de usuarios
    const res = await axios.get('/auth/usuarios')
    const existe = res.data.find(u => u.email === emailRecupero.value)
    if (!existe) {
      notificacion.add({ severity: 'error', summary: 'No encontrado', detail: 'No existe una cuenta con ese correo', life: 3000 })
      return
    }
    pasoModal.value = 2
  } catch {
    notificacion.add({ severity: 'error', summary: 'Error', detail: 'No se pudo verificar el correo', life: 3000 })
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
    await axios.put('/auth/cambiar-password', {
      email: emailRecupero.value,
      nueva_password: nuevaContrasena.value
    })
    pasoModal.value = 3
  } catch (e) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: e.response?.data?.detail || 'No se pudo cambiar la contraseña', life: 3000 })
  } finally {
    cargandoModal.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }

.pagina-login {
  min-height: 100vh; background: #080c14;
  display: flex; flex-direction: column; align-items: center;
  position: relative; overflow: hidden;
}
.fondo-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(56,139,253,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,139,253,0.03) 1px, transparent 1px);
  background-size: 52px 52px; pointer-events: none;
}

.carrusel-wrapper { width: 100%; background: #0d1117; border-bottom: 1px solid #161b22; padding: 0.55rem 0; overflow: hidden; z-index: 1; }
.carrusel-track { display: flex; gap: 3rem; animation: deslizar 28s linear infinite; width: max-content; }
.carrusel-item { display: flex; align-items: center; gap: 0.45rem; color: #30363d; font-size: 0.75rem; font-weight: 500; letter-spacing: 0.04em; white-space: nowrap; }
.carrusel-item i { color: #1d4ed8; font-size: 0.7rem; }
@keyframes deslizar { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

.centro { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2.5rem; padding: 3rem 1.5rem; z-index: 1; width: 100%; }

.logo-bloque { display: flex; align-items: center; gap: 1rem; }
.pulso-linea { stroke-dasharray: 80; stroke-dashoffset: 80; animation: dibujarPulso 2s ease-in-out infinite; }
.pulso-delay { animation-delay: 0.4s; }
@keyframes dibujarPulso {
  0%   { stroke-dashoffset: 80; opacity: 0; }
  10%  { opacity: 1; }
  50%  { stroke-dashoffset: 0; opacity: 1; }
  80%  { stroke-dashoffset: 0; opacity: 0.3; }
  100% { stroke-dashoffset: 80; opacity: 0; }
}
.logo-nombre { font-size: 2rem; font-weight: 700; color: #e6edf3; letter-spacing: -1px; line-height: 1.1; }
.logo-sub { font-size: 0.72rem; color: #30363d; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.2rem; font-weight: 500; }

.tarjeta { width: 100%; max-width: 360px; background: #0d1117; border: 1px solid #21262d; border-radius: 16px; padding: 2rem; }
.tarjeta-titulo { font-size: 0.75rem; font-weight: 600; color: #8b949e; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.08em; }

.campo { margin-bottom: 1.1rem; }
.campo label { display: block; font-size: 0.78rem; font-weight: 500; color: #8b949e; margin-bottom: 0.45rem; }
.inp { width: 100%; }

/* LINK OLVIDÉ */
.fila-olvide { display: flex; justify-content: flex-end; margin-bottom: 1rem; margin-top: -0.4rem; }
.link-olvide {
  font-size: 0.75rem; color: #388bfd; cursor: pointer;
  display: flex; align-items: center; gap: 0.3rem; font-weight: 500;
  transition: opacity 0.2s;
}
.link-olvide:hover { opacity: 0.75; text-decoration: underline; }

.boton-entrar {
  position: relative; width: 100%; margin-top: 0.2rem; padding: 0.75rem 1.2rem;
  background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 10px;
  color: #e6edf3; font-size: 0.9rem; font-weight: 600; font-family: 'Inter', sans-serif;
  cursor: pointer; overflow: hidden; transition: background 0.25s, border-color 0.25s, transform 0.15s;
}
.boton-entrar:hover:not(:disabled) { background: #1d4ed8; border-color: #388bfd; transform: translateY(-2px); }
.boton-entrar:active:not(:disabled) { transform: translateY(0); }
.boton-entrar:disabled { opacity: 0.5; cursor: not-allowed; }
.boton-contenido { display: flex; align-items: center; justify-content: center; gap: 0.5rem; position: relative; z-index: 1; }
.boton-brillo { position: absolute; top: 0; left: -100%; width: 60%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent); transform: skewX(-20deg); transition: left 0.5s ease; pointer-events: none; }
.boton-entrar:hover .boton-brillo { left: 150%; }
.icono-boton { transition: transform 0.25s ease; }
.boton-entrar:hover .icono-boton { transform: translateX(4px); }

.pie { text-align: center; margin-top: 1.2rem; font-size: 0.78rem; color: #30363d; }
.pie span { color: #388bfd; cursor: pointer; font-weight: 600; }
.pie span:hover { text-decoration: underline; }

/* ===== MODAL ===== */
.modal-overlay {
  position: fixed; inset: 0; z-index: 100;
  background: rgba(8,12,20,0.85); backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center; padding: 1.5rem;
}
.modal-caja {
  width: 100%; max-width: 380px;
  background: #0d1117; border: 1px solid #21262d; border-radius: 18px;
  padding: 2rem; box-shadow: 0 24px 80px rgba(0,0,0,0.6);
}
.modal-cabeza { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.modal-icono {
  width: 44px; height: 44px; border-radius: 12px; flex-shrink: 0;
  background: rgba(56,139,253,0.1); border: 1px solid rgba(56,139,253,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; color: #388bfd;
}
.modal-icono-ok { background: rgba(63,185,80,0.1); border-color: rgba(63,185,80,0.2); color: #3fb950; }
.modal-titulo { font-size: 0.95rem; font-weight: 700; color: #e6edf3; margin-bottom: 0.2rem; }
.modal-sub { font-size: 0.75rem; color: #484f58; }
.modal-sub strong { color: #8b949e; }

.modal-acciones { display: flex; gap: 0.7rem; margin-top: 1.3rem; }
.btn-modal-cancelar {
  flex: 1; padding: 0.55rem; background: transparent; border: 1px solid #21262d;
  border-radius: 8px; color: #8b949e; font-size: 0.82rem; font-family: 'Inter', sans-serif;
  cursor: pointer; transition: all 0.2s;
}
.btn-modal-cancelar:hover { border-color: #30363d; color: #e6edf3; }
.btn-modal-ok {
  flex: 1; padding: 0.55rem; background: #1a3a6e; border: 1px solid #2d5fa8;
  border-radius: 8px; color: #e6edf3; font-size: 0.82rem; font-weight: 600;
  font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.2s;
  display: flex; align-items: center; justify-content: center; gap: 0.4rem;
}
.btn-modal-ok:hover:not(:disabled) { background: #1d4ed8; border-color: #388bfd; }
.btn-modal-ok:disabled { opacity: 0.4; cursor: not-allowed; }

.aviso-modal { color: #f85149; font-size: 0.75rem; margin-top: 0.6rem; display: flex; align-items: center; gap: 0.4rem; }

/* PASO 3 ÉXITO */
.modal-exito { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 0.5rem; padding: 1rem 0; }
.exito-icono { font-size: 2.5rem; color: #3fb950; margin-bottom: 0.5rem; }
.exito-titulo { font-size: 1rem; font-weight: 700; color: #e6edf3; }
.exito-sub { font-size: 0.78rem; color: #484f58; }

/* TRANSICIONES */
.modal-fade-enter-active { transition: opacity 0.25s ease, transform 0.25s ease; }
.modal-fade-enter-from { opacity: 0; transform: scale(0.96); }
.modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>