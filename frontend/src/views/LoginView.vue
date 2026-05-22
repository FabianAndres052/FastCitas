<template>
  <div v-if="cargandoLogin" class="skeleton-page" style="display:flex;justify-content:center;align-items:center;height:100vh;">
    <Skeleton height="20rem" width="100%" />
  </div>
  <div v-else class="pagina-login">

    <!-- CARRUSEL -->
    <div class="carrusel-wrapper">
      <div class="carrusel-track">
        <span v-for="(item, i) in carruselItems.concat(carruselItems)" :key="i" class="carrusel-item">
          <i :class="item.icono"></i> {{ item.texto }}
        </span>
      </div>
    </div>

    <div class="contenedor-principal">
      <!-- IZQUIERDA: PROBLEMÁTICA -->
      <div class="lado-izquierdo">
        <div class="logo-bloque">
          <svg viewBox="0 0 80 80" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
            <polygon points="40,2 76,21 76,59 40,78 4,59 4,21" fill="none" stroke="#1a2744" stroke-width="1"/>
            <rect x="29" y="14" width="22" height="52" rx="7" fill="#1a3a6e"/>
            <rect x="14" y="29" width="52" height="22" rx="7" fill="#1a3a6e"/>
            <rect x="31" y="16" width="18" height="48" rx="6" fill="#388bfd"/>
            <rect x="16" y="31" width="48" height="18" rx="6" fill="#388bfd"/>
            <rect x="31" y="31" width="18" height="18" rx="4" fill="#60a5fa"/>
            <polyline class="pulso-linea" points="4,40 14,40 20,26 28,54 32,40" fill="none" stroke="#388bfd" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline class="pulso-linea pulso-delay" points="48,40 52,26 60,54 66,40 76,40" fill="none" stroke="#388bfd" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div>
            <h1 class="logo-nombre">FastCitas</h1>
            <p class="logo-sub">Agendamiento médico digital</p>
          </div>
        </div>

        <div class="eslogan-bloque">
          <h2>¿Cansado de madrugar<br/>para un turno?</h2>
          <p>En Colombia, miles de pacientes hacen fila desde las 4AM en centros de salud pública. Los turnos se acaban en minutos. <strong>FastCitas lo cambia todo.</strong></p>
        </div>

        <div class="comparacion">
          <div class="col-mal">
            <p class="col-titulo"><i class="pi pi-times-circle"></i> Sin FastCitas</p>
            <ul>
              <li>Fila desde las 4AM</li>
              <li>Turnos agotados en 10 min</li>
              <li>Sin historial médico</li>
              <li>Papel y bolígrafo</li>
            </ul>
          </div>
          <div class="col-bien">
            <p class="col-titulo"><i class="pi pi-check-circle"></i> Con FastCitas</p>
            <ul>
              <li>Agenda en 30 segundos</li>
              <li>Disponible 24/7</li>
              <li>Historial digital</li>
              <li>Notificaciones al instante</li>
            </ul>
          </div>
        </div>

        <div class="stats-row">
          <div class="stat-item">
            <span class="stat-n">+2.400</span>
            <span class="stat-l">Pacientes</span>
          </div>
          <div class="stat-item">
            <span class="stat-n">8</span>
            <span class="stat-l">Especialidades</span>
          </div>
          <div class="stat-item">
            <span class="stat-n">0</span>
            <span class="stat-l">Horas en fila</span>
          </div>
        </div>
      </div>

      <!-- DERECHA: FORMULARIO -->
      <div class="lado-derecho">
        <div class="tarjeta">
          <p class="tarjeta-titulo">Iniciar sesión</p>

          <div class="campo">
            <label>Correo electrónico</label>
            <InputText v-model="correo" placeholder="correo@ejemplo.com" class="inp" :disabled="cargandoLogin" />
          </div>

          <div class="campo">
            <label>Contraseña</label>
            <InputText v-model="contrasena" type="password" placeholder="••••••••" class="inp" :disabled="cargandoLogin" />
          </div>

          <!-- TÉRMINOS -->
          <div class="terminos-check-login">
            <input type="checkbox" id="acepto-login" v-model="aceptaTerminos" :disabled="cargandoLogin" />
            <label for="acepto-login">
              He leído y acepto los <span class="link-terminos" @click.stop.prevent="mostrarTerminos = true">términos y condiciones</span>
            </label>
          </div>

          <div class="fila-olvide">
            <span class="link-olvide" @click="mostrarModalContrasena = true">
              <i class="pi pi-lock"></i> ¿Olvidaste tu contraseña?
            </span>
          </div>

          <button class="boton-entrar" @click="iniciarSesion" :disabled="cargandoLogin || !aceptaTerminos">
            <span v-if="!cargandoLogin" class="boton-contenido">
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
    </div>

    <!-- MODAL TÉRMINOS -->
    <Transition name="modal-fade">
      <div class="modal-overlay" v-if="mostrarTerminos" @click.self="mostrarTerminos = false">
        <div class="modal-caja">
          <div class="modal-cabeza">
            <div class="modal-icono"><i class="pi pi-shield"></i></div>
            <div style="flex:1">
              <p class="modal-titulo">Términos y Condiciones</p>
              <p class="modal-sub">FastCitas · Colombia</p>
            </div>
            <button class="modal-cerrar" @click="mostrarTerminos = false"><i class="pi pi-times"></i></button>
          </div>
          <div class="texto-terminos">
            <p><strong>1. Uso del sistema:</strong> FastCitas es una plataforma de agendamiento médico. El uso indebido resultará en suspensión de la cuenta.</p>
            <p><strong>2. Datos personales:</strong> Los datos ingresados se usan únicamente para gestionar sus citas y no serán compartidos con terceros.</p>
            <p><strong>3. Responsabilidad:</strong> El usuario es responsable de asistir a las citas. Cancelaciones con mínimo 2 horas de anticipación.</p>
            <p><strong>4. Veracidad:</strong> El usuario garantiza que la información es verídica.</p>
            <p><strong>5. Privacidad:</strong> FastCitas cumple con la Ley 1581 de 2012 de protección de datos de Colombia.</p>
          </div>
          <div class="modal-acciones">
            <button class="btn-modal-cancelar" @click="mostrarTerminos = false">Cerrar</button>
            <button class="btn-modal-ok" @click="aceptarTerminosModal">
              <i class="pi pi-check"></i> Aceptar
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- MODAL OLVIDÉ CONTRASEÑA -->
    <Transition name="modal-fade">
      <div class="modal-overlay" v-if="mostrarModalContrasena" @click.self="cerrarModal">
        <div class="modal-caja">
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

          <div v-if="pasoModal === 2">
            <div class="modal-cabeza">
              <div class="modal-icono modal-icono-ok"><i class="pi pi-check"></i></div>
              <div>
                <p class="modal-titulo">Nueva contraseña</p>
                <p class="modal-sub">Cuenta encontrada · <strong>{{ emailRecupero }}</strong></p>
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

          <div v-if="pasoModal === 3" class="modal-exito">
            <div class="exito-icono"><i class="pi pi-check-circle"></i></div>
            <p class="exito-titulo">¡Contraseña actualizada!</p>
            <p class="exito-sub">Ya puedes iniciar sesión</p>
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
import { useToast } from 'primevue/usetoast';
import Skeleton from 'primevue/skeleton';
import axios from 'axios';

const enrutador = useRouter()
const notificacion = useToast()

const correo = ref('')
const contrasena = ref('')
const cargandoLogin = ref(false)
const aceptaTerminos = ref(false)
const mostrarTerminos = ref(false)
const intentoLogin = ref(false)
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

const aceptarTerminosModal = () => {
  aceptaTerminos.value = true
  mostrarTerminos.value = false
  notificacion.add({ severity: 'success', summary: 'Términos aceptados', detail: 'Ya puedes iniciar sesión', life: 2000 })
}

const iniciarSesion = async () => {
  intentoLogin.value = true
  if (!aceptaTerminos.value) return
  if (!correo.value || !contrasena.value) {
    notificacion.add({ severity: 'warn', summary: 'Atención', detail: 'Completa todos los campos', life: 3000 })
    return
  }
  cargandoLogin.value = true
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
    cargandoLogin.value = false
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
    await axios.get('/auth/verificar-email', { params: { email: emailRecupero.value } })
    pasoModal.value = 2
  } catch (error) {
    const mensaje = error.response?.data?.detail || 'No se pudo verificar el correo'
    notificacion.add({ severity: 'error', summary: 'No encontrado', detail: mensaje, life: 3000 })
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
    await axios.put('/auth/cambiar-password', { email: emailRecupero.value, nueva_password: nuevaContrasena.value })
    pasoModal.value = 3
  } catch (e) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: e.response?.data?.detail || 'No se pudo cambiar la contraseña', life: 3000 })
  } finally {
    cargandoModal.value = false
  }
}
</script>

<style scoped>
.pagina-login {
  min-height: 100vh; background: #080c14;
  display: flex; flex-direction: column;
  position: relative; overflow: hidden;
}

.fondo-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(56,139,253,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,139,253,0.03) 1px, transparent 1px);
  background-size: 52px 52px; pointer-events: none;
}

/* CARRUSEL */
.carrusel-wrapper { width: 100%; background: #0d1117; border-bottom: 1px solid #21262d; padding: 0.6rem 0; overflow: hidden; z-index: 1; }
.carrusel-track { display: flex; gap: 3rem; animation: deslizar 28s linear infinite; width: max-content; }
.carrusel-item { display: flex; align-items: center; gap: 0.5rem; color: #8b949e; font-size: 0.78rem; font-weight: 500; white-space: nowrap; }
.carrusel-item i { color: #388bfd; }
@keyframes deslizar { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

/* LAYOUT */
.contenedor-principal { flex: 1; display: flex; }

/* IZQUIERDA */
.lado-izquierdo {
  flex: 1.1; padding: 3.5rem 3rem;
  display: flex; flex-direction: column; gap: 2.5rem;
  justify-content: center; border-right: 1px solid #21262d;
  background: linear-gradient(160deg, #0d1117 60%, #0f1923 100%);
}

.logo-bloque { display: flex; align-items: center; gap: 1rem; }
.pulso-linea { stroke-dasharray: 80; stroke-dashoffset: 80; animation: dibujarPulso 2s ease-in-out infinite; }
.pulso-delay { animation-delay: 0.4s; }
@keyframes dibujarPulso { 0% { stroke-dashoffset: 80; opacity: 0; } 10% { opacity: 1; } 50% { stroke-dashoffset: 0; opacity: 1; } 80% { stroke-dashoffset: 0; opacity: 0.3; } 100% { stroke-dashoffset: 80; opacity: 0; } }
.logo-nombre { font-size: 2rem; font-weight: 700; color: #e6edf3; letter-spacing: -1px; }
.logo-sub { font-size: 0.7rem; color: #484f58; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.2rem; }

.eslogan-bloque { }
.eslogan-bloque h2 { font-size: 1.6rem; font-weight: 700; color: #e6edf3; line-height: 1.3; margin-bottom: 0.8rem; }
.eslogan-bloque p { font-size: 0.88rem; color: #8b949e; line-height: 1.6; }
.eslogan-bloque strong { color: #60a5fa; }

/* COMPARACIÓN */
.comparacion { display: flex; gap: 1rem; }
.col-mal, .col-bien {
  flex: 1; padding: 1.2rem; border-radius: 12px;
}
.col-mal { background: rgba(248,81,73,0.05); border: 1px solid rgba(248,81,73,0.15); }
.col-bien { background: rgba(63,185,80,0.05); border: 1px solid rgba(63,185,80,0.15); }
.col-titulo { font-size: 0.78rem; font-weight: 700; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.4rem; }
.col-mal .col-titulo { color: #f85149; }
.col-bien .col-titulo { color: #3fb950; }
.col-mal ul, .col-bien ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.5rem; }
.col-mal li, .col-bien li { font-size: 0.78rem; color: #8b949e; padding-left: 0.5rem; border-left: 2px solid; }
.col-mal li { border-color: rgba(248,81,73,0.3); }
.col-bien li { border-color: rgba(63,185,80,0.3); }

/* STATS */
.stats-row { display: flex; gap: 1rem; }
.stat-item { flex: 1; background: #0d1117; border: 1px solid #21262d; border-radius: 10px; padding: 1rem; text-align: center; transition: border-color 0.2s, transform 0.2s; }
.stat-item:hover { border-color: rgba(56,139,253,0.3); transform: translateY(-3px); }
.stat-n { display: block; font-size: 1.5rem; font-weight: 700; color: #388bfd; }
.stat-l { display: block; font-size: 0.7rem; color: #484f58; margin-top: 0.2rem; }

/* DERECHA */
.lado-derecho { flex: 0.9; display: flex; align-items: center; justify-content: center; padding: 3rem 2.5rem; background: #080c14; }

.tarjeta { width: 100%; max-width: 380px; }
.tarjeta-titulo { font-size: 0.72rem; font-weight: 600; color: #484f58; margin-bottom: 1.8rem; text-transform: uppercase; letter-spacing: 0.1em; }

.campo { margin-bottom: 1.1rem; }
.campo label { display: block; font-size: 0.78rem; font-weight: 500; color: #8b949e; margin-bottom: 0.45rem; }
.inp { width: 100%; }

/* TÉRMINOS */
.terminos-check-login {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  margin-bottom: 1.1rem;
  font-size: 0.78rem;
  color: #8b949e;
}
.terminos-check-login input[type="checkbox"] {
  width: 14px;
  height: 14px;
  accent-color: #388bfd;
  cursor: pointer;
  flex-shrink: 0;
}
.terminos-check-login label {
  cursor: pointer;
  user-select: none;
}
.link-terminos {
  color: #388bfd;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}
.link-terminos:hover {
  color: #60a5fa;
}

.fila-olvide { display: flex; justify-content: flex-end; margin-bottom: 1rem; }
.link-olvide { font-size: 0.75rem; color: #388bfd; cursor: pointer; display: flex; align-items: center; gap: 0.3rem; font-weight: 500; }
.link-olvide:hover { opacity: 0.75; text-decoration: underline; }

.boton-entrar {
  position: relative; width: 100%; padding: 0.75rem 1.2rem;
  background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 10px;
  color: #e6edf3; font-size: 0.9rem; font-weight: 600; font-family: 'Inter', sans-serif;
  cursor: pointer; overflow: hidden; transition: background 0.25s, border-color 0.25s, transform 0.15s;
}
.boton-entrar:hover:not(:disabled) { background: #1d4ed8; border-color: #388bfd; transform: translateY(-2px); }
.boton-entrar:disabled { opacity: 0.5; cursor: not-allowed; }
.boton-contenido { display: flex; align-items: center; justify-content: center; gap: 0.5rem; position: relative; z-index: 1; }
.boton-brillo { position: absolute; top: 0; left: -100%; width: 60%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent); transform: skewX(-20deg); transition: left 0.5s ease; pointer-events: none; }
.boton-entrar:hover .boton-brillo { left: 150%; }
.icono-boton { transition: transform 0.25s ease; }
.boton-entrar:hover .icono-boton { transform: translateX(4px); }

.pie { text-align: center; margin-top: 1.2rem; font-size: 0.78rem; color: #484f58; }
.pie span { color: #388bfd; cursor: pointer; font-weight: 600; }
.pie span:hover { text-decoration: underline; }

/* MODALES */
.modal-overlay { position: fixed; inset: 0; z-index: 200; background: rgba(8,12,20,0.88); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; padding: 1.5rem; }
.modal-caja { width: 100%; max-width: 400px; background: #0d1117; border: 1px solid #21262d; border-radius: 18px; padding: 2rem; box-shadow: 0 24px 80px rgba(0,0,0,0.6); }
.modal-cabeza { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.modal-icono { width: 44px; height: 44px; border-radius: 12px; flex-shrink: 0; background: rgba(56,139,253,0.1); border: 1px solid rgba(56,139,253,0.2); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #388bfd; }
.modal-icono-ok { background: rgba(63,185,80,0.1); border-color: rgba(63,185,80,0.2); color: #3fb950; }
.modal-titulo { font-size: 0.95rem; font-weight: 700; color: #e6edf3; margin-bottom: 0.2rem; }
.modal-sub { font-size: 0.75rem; color: #484f58; }
.modal-sub strong { color: #8b949e; }
.modal-cerrar { margin-left: auto; background: transparent; border: none; color: #484f58; font-size: 0.9rem; cursor: pointer; padding: 0.3rem; border-radius: 6px; }
.modal-cerrar:hover { color: #e6edf3; }
.texto-terminos { max-height: 260px; overflow-y: auto; display: flex; flex-direction: column; gap: 0.8rem; margin-bottom: 1.5rem; }
.texto-terminos p { font-size: 0.82rem; color: #8b949e; line-height: 1.6; }
.texto-terminos strong { color: #e6edf3; }
.modal-acciones { display: flex; gap: 0.7rem; margin-top: 1.3rem; }
.btn-modal-cancelar { flex: 1; padding: 0.55rem; background: transparent; border: 1px solid #21262d; border-radius: 8px; color: #8b949e; font-size: 0.82rem; font-family: 'Inter', sans-serif; cursor: pointer; }
.btn-modal-ok { flex: 1; padding: 0.55rem; background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 8px; color: #e6edf3; font-size: 0.82rem; font-weight: 600; font-family: 'Inter', sans-serif; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.4rem; }
.btn-modal-ok:hover:not(:disabled) { background: #1d4ed8; border-color: #388bfd; }
.btn-modal-ok:disabled { opacity: 0.4; cursor: not-allowed; }
.aviso-modal { color: #f85149; font-size: 0.75rem; margin-top: 0.6rem; display: flex; align-items: center; gap: 0.4rem; }
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

@media (max-width: 768px) {
  .contenedor-principal { flex-direction: column; }
  .lado-izquierdo { padding: 2rem 1.5rem; border-right: none; border-bottom: 1px solid #21262d; }
  .comparacion { flex-direction: column; }
  .stats-row { flex-wrap: wrap; }
}
</style>