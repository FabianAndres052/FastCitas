<template>
  <div class="pagina-registro">
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
        <svg viewBox="0 0 80 80" width="56" height="56" xmlns="http://www.w3.org/2000/svg">
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
        <div>
          <h1 class="logo-nombre">FastCitas</h1>
          <p class="logo-sub">Crea tu cuenta</p>
        </div>
      </div>

      <div class="tarjeta">
        <p class="tarjeta-titulo">Registro</p>

        <!-- SELECTOR DE ROL VISUAL -->
        <div class="rol-selector">
          <button
            class="rol-btn"
            :class="{ activo: rol === 'paciente' }"
            @click="rol = 'paciente'"
            type="button"
          >
            <i class="pi pi-user"></i>
            <span class="rol-label">Paciente</span>
            <span class="rol-desc">Agenda citas médicas</span>
          </button>
          <button
            class="rol-btn"
            :class="{ activo: rol === 'doctor' }"
            @click="rol = 'doctor'"
            type="button"
          >
            <i class="pi pi-heart"></i>
            <span class="rol-label">Doctor</span>
            <span class="rol-desc">Ofrece consultas</span>
          </button>
        </div>

        <div class="fila-campos">
          <div class="campo">
            <label>Nombre completo</label>
            <InputText v-model="nombre" placeholder="Tu nombre" class="inp" :disabled="cargando" />
          </div>
          <div class="campo">
            <label>Correo electrónico</label>
            <InputText v-model="correo" placeholder="correo@ejemplo.com" class="inp" :disabled="cargando" />
          </div>
        </div>

        <div class="fila-campos">
          <div class="campo">
            <label>Contraseña</label>
            <InputText v-model="contrasena" type="password" placeholder="••••••••" class="inp" :disabled="cargando" />
          </div>
          <div class="campo">
            <label>Teléfono</label>
            <InputText v-model="telefono" placeholder="3001234567" class="inp" :disabled="cargando" />
          </div>
        </div>

        <!-- CAMPO ESPECIALIDAD — solo si es doctor -->
        <Transition name="deslizar">
          <div class="campo campo-full" v-if="rol === 'doctor'">
            <label>
              <i class="pi pi-briefcase" style="color:#388bfd; margin-right:0.3rem"></i>
              Especialidad médica
            </label>
            <select v-model="especialidad" class="selector" :disabled="cargando">
              <option value="">Selecciona tu especialidad...</option>
              <option v-for="e in especialidades" :key="e">{{ e }}</option>
            </select>
            <p class="campo-hint">Tu perfil aparecerá en el listado de médicos disponibles</p>
          </div>
        </Transition>

        <div class="bloque-terminos">
          <div class="terminos-cabeza" @click="expandirTerminos = !expandirTerminos">
            <div class="terminos-titulo">
              <i class="pi pi-shield"></i>
              <span>Términos y condiciones</span>
            </div>
            <i :class="['pi', expandirTerminos ? 'pi-chevron-up' : 'pi-chevron-down', 'icono-chevron']"></i>
          </div>

          <Transition name="expandir">
            <div class="terminos-cuerpo" v-show="expandirTerminos">
              <div class="termino-item" v-for="(t, i) in terminos" :key="i">
                <span class="termino-num">{{ i + 1 }}</span>
                <div>
                  <p class="termino-titulo-item">{{ t.titulo }}</p>
                  <p class="termino-desc">{{ t.desc }}</p>
                </div>
              </div>
            </div>
          </Transition>

          <div class="terminos-check">
            <input type="checkbox" id="acepto" v-model="aceptaTerminos" :disabled="cargando" />
            <label for="acepto">He leído y acepto los términos y condiciones</label>
          </div>

          <Transition name="fade">
            <p class="aviso" v-if="intentoRegistro && !aceptaTerminos">
              <i class="pi pi-exclamation-triangle"></i> Debes aceptar los términos para continuar
            </p>
          </Transition>
        </div>

        <button class="boton-registrar" @click="registrar" :disabled="cargando || !aceptaTerminos">
          <span v-if="!cargando" class="boton-contenido">
            Crear cuenta <i class="pi pi-user-plus icono-boton"></i>
          </span>
          <span v-else class="boton-contenido">
            <i class="pi pi-spin pi-spinner"></i> Registrando...
          </span>
          <span class="boton-brillo"></span>
        </button>

        <p class="pie">
          ¿Ya tienes cuenta? <span @click="$router.push('/login')">Inicia sesión</span>
        </p>
      </div>
    </div>

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

const nombre = ref('')
const correo = ref('')
const contrasena = ref('')
const telefono = ref('')
const rol = ref('paciente')
const especialidad = ref('')
const cargando = ref(false)
const aceptaTerminos = ref(false)
const expandirTerminos = ref(false)
const intentoRegistro = ref(false)

const especialidades = [
  'Medicina General', 'Pediatría', 'Cardiología', 'Dermatología',
  'Neurología', 'Ginecología', 'Oftalmología', 'Odontología',
  'Ortopedia', 'Psiquiatría', 'Endocrinología', 'Traumatología',
]

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

const terminos = ref([
  { titulo: 'Uso del sistema', desc: 'FastCitas es una plataforma de agendamiento médico. El uso indebido resultará en suspensión de la cuenta.' },
  { titulo: 'Datos personales', desc: 'Los datos ingresados se usan únicamente para gestionar sus citas y no serán compartidos con terceros.' },
  { titulo: 'Responsabilidad', desc: 'El usuario es responsable de asistir a las citas agendadas. Cancelaciones con mínimo 2 horas de anticipación.' },
  { titulo: 'Veracidad', desc: 'El usuario garantiza que la información ingresada es verídica. Información falsa puede resultar en cancelación.' },
  { titulo: 'Privacidad', desc: 'FastCitas cumple con la Ley 1581 de 2012 de protección de datos personales de Colombia.' },
])

const registrar = async () => {
  intentoRegistro.value = true
  if (!aceptaTerminos.value) return

  if (!nombre.value || !correo.value || !contrasena.value || !telefono.value) {
    notificacion.add({ severity: 'warn', summary: 'Atención', detail: 'Completa todos los campos', life: 3000 })
    return
  }

  if (rol.value === 'doctor' && !especialidad.value) {
    notificacion.add({ severity: 'warn', summary: 'Atención', detail: 'Selecciona tu especialidad médica', life: 3000 })
    return
  }

  cargando.value = true
  try {
    await axios.post('/auth/register', {
      nombre: nombre.value,
      email: correo.value,
      password: contrasena.value,
      telefono: telefono.value,
      rol: rol.value,
      especialidad: rol.value === 'doctor' ? especialidad.value : '',
    })
    notificacion.add({
      severity: 'success',
      summary: '¡Cuenta creada!',
      detail: rol.value === 'doctor'
        ? `Dr. ${nombre.value} ya aparece en el listado de médicos`
        : 'Ya puedes iniciar sesión',
      life: 3000
    })
    setTimeout(() => enrutador.push('/login'), 2000)
  } catch (error) {
    notificacion.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al registrar', life: 3000 })
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }

.pagina-registro {
  min-height: 100vh;
  background: #080c14;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.fondo-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(56,139,253,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,139,253,0.03) 1px, transparent 1px);
  background-size: 52px 52px;
  pointer-events: none;
}

.carrusel-wrapper { width: 100%; background: #0d1117; border-bottom: 1px solid #161b22; padding: 0.55rem 0; overflow: hidden; z-index: 1; }
.carrusel-track { display: flex; gap: 3rem; animation: deslizar 28s linear infinite; width: max-content; }
.carrusel-item { display: flex; align-items: center; gap: 0.45rem; color: #30363d; font-size: 0.75rem; font-weight: 500; white-space: nowrap; }
.carrusel-item i { color: #1d4ed8; font-size: 0.7rem; }
@keyframes deslizar { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

.centro {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 2rem; padding: 2.5rem 1.5rem; z-index: 1; width: 100%;
}

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
.logo-nombre { font-size: 1.8rem; font-weight: 700; color: #e6edf3; letter-spacing: -1px; line-height: 1.1; }
.logo-sub { font-size: 0.72rem; color: #30363d; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.2rem; font-weight: 500; }

.tarjeta { width: 100%; max-width: 540px; background: #0d1117; border: 1px solid #21262d; border-radius: 16px; padding: 2rem; }
.tarjeta-titulo { font-size: 0.75rem; font-weight: 600; color: #8b949e; margin-bottom: 1.2rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* SELECTOR DE ROL */
.rol-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; margin-bottom: 1.3rem; }
.rol-btn {
  display: flex; flex-direction: column; align-items: center; gap: 0.3rem;
  padding: 0.9rem 0.7rem; background: #0a0f1a; border: 1px solid #21262d;
  border-radius: 12px; cursor: pointer; transition: all 0.2s; text-align: center;
}
.rol-btn i { font-size: 1.2rem; color: #484f58; transition: color 0.2s; }
.rol-btn:hover { border-color: #30363d; }
.rol-btn.activo { border-color: #388bfd; background: rgba(56,139,253,0.06); }
.rol-btn.activo i { color: #388bfd; }
.rol-label { font-size: 0.85rem; font-weight: 600; color: #8b949e; transition: color 0.2s; }
.rol-btn.activo .rol-label { color: #e6edf3; }
.rol-desc { font-size: 0.7rem; color: #30363d; }

.fila-campos { display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; margin-bottom: 0.9rem; }
.campo label { display: block; font-size: 0.78rem; font-weight: 500; color: #8b949e; margin-bottom: 0.45rem; }
.inp { width: 100%; }

/* CAMPO ESPECIALIDAD */
.campo-full { margin-bottom: 0.9rem; }
.campo-hint { font-size: 0.7rem; color: #388bfd; margin-top: 0.4rem; display: flex; align-items: center; gap: 0.3rem; }

.selector {
  width: 100%; padding: 0.55rem 0.8rem;
  background: #161b22; border: 1px solid #30363d; border-radius: 8px;
  color: #e6edf3; font-size: 0.85rem; font-family: 'Inter', sans-serif;
  cursor: pointer; transition: border-color 0.2s;
}
.selector:hover { border-color: #388bfd; }
.selector:focus { outline: none; border-color: #388bfd; }
.selector option { background: #161b22; }

.bloque-terminos { background: #0a0f1a; border: 1px solid #21262d; border-radius: 12px; padding: 1rem; margin-bottom: 1.2rem; }
.terminos-cabeza { display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none; padding-bottom: 0.5rem; }
.terminos-titulo { display: flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; font-weight: 600; color: #8b949e; }
.terminos-titulo i { color: #388bfd; }
.icono-chevron { color: #484f58; font-size: 0.75rem; transition: transform 0.2s; }

.terminos-cuerpo { padding-top: 0.8rem; display: flex; flex-direction: column; gap: 0.7rem; max-height: 200px; overflow-y: auto; margin-bottom: 0.8rem; padding-right: 0.3rem; }
.termino-item { display: flex; gap: 0.75rem; align-items: flex-start; }
.termino-num { flex-shrink: 0; width: 20px; height: 20px; background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.65rem; font-weight: 700; color: #60a5fa; margin-top: 1px; }
.termino-titulo-item { font-size: 0.78rem; font-weight: 600; color: #cdd9e5; margin-bottom: 0.15rem; }
.termino-desc { font-size: 0.75rem; color: #484f58; line-height: 1.55; }

.terminos-check { display: flex; align-items: center; gap: 0.55rem; padding-top: 0.6rem; border-top: 1px solid #161b22; font-size: 0.78rem; color: #8b949e; }
.terminos-check input[type="checkbox"] { width: 14px; height: 14px; accent-color: #388bfd; cursor: pointer; flex-shrink: 0; }
.terminos-check label { cursor: pointer; }
.aviso { color: #f85149; font-size: 0.75rem; margin-top: 0.5rem; display: flex; align-items: center; gap: 0.4rem; }

.boton-registrar {
  position: relative; width: 100%; margin-top: 0.3rem; padding: 0.75rem 1.2rem;
  background: #1a3a6e; border: 1px solid #2d5fa8; border-radius: 10px;
  color: #e6edf3; font-size: 0.9rem; font-weight: 600; font-family: 'Inter', sans-serif;
  cursor: pointer; overflow: hidden; transition: background 0.25s, border-color 0.25s, transform 0.15s;
}
.boton-registrar:hover:not(:disabled) { background: #1d4ed8; border-color: #388bfd; transform: translateY(-2px); }
.boton-registrar:active:not(:disabled) { transform: translateY(0); }
.boton-registrar:disabled { opacity: 0.3; cursor: not-allowed; filter: grayscale(0.4); }
.boton-contenido { display: flex; align-items: center; justify-content: center; gap: 0.5rem; position: relative; z-index: 1; }
.boton-brillo { position: absolute; top: 0; left: -100%; width: 60%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent); transform: skewX(-20deg); transition: left 0.5s ease; pointer-events: none; }
.boton-registrar:hover .boton-brillo { left: 150%; }
.icono-boton { transition: transform 0.25s ease; }
.boton-registrar:hover .icono-boton { transform: translateX(4px); }

.pie { text-align: center; margin-top: 1.2rem; font-size: 0.78rem; color: #30363d; }
.pie span { color: #388bfd; cursor: pointer; font-weight: 600; }
.pie span:hover { text-decoration: underline; }

.deslizar-enter-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.deslizar-enter-from { opacity: 0; transform: translateY(-10px); }
.deslizar-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.deslizar-leave-to { opacity: 0; transform: translateY(-8px); }
.expandir-enter-active, .expandir-leave-active { transition: opacity 0.25s; }
.expandir-enter-from, .expandir-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 540px) {
  .fila-campos { grid-template-columns: 1fr; }
  .rol-selector { grid-template-columns: 1fr 1fr; }
}
</style>