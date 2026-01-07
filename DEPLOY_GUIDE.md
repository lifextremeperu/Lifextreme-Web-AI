# 🚀 GUÍA DE USO - Script de Deploy Rápido

## ¿Qué Hace Este Script?

El archivo `deploy.ps1` automatiza todo el proceso de subir cambios a GitHub y Netlify con un solo comando.

---

## 📋 Uso del Script

### **Método 1: Con Mensaje Personalizado**

```powershell
.\deploy.ps1 "Descripción de tus cambios"
```

**Ejemplos:**
```powershell
.\deploy.ps1 "Actualizar diseño del Portal Partners"
.\deploy.ps1 "Agregar nueva sección de tours"
.\deploy.ps1 "Corregir bug en el sistema de reservas"
```

### **Método 2: Desde la Terminal de VS Code**

1. Abre la terminal en VS Code (Ctrl + `)
2. Navega a la carpeta del proyecto
3. Ejecuta:
```powershell
.\deploy.ps1 "tu mensaje aquí"
```

---

## 🔄 Lo Que Hace Automáticamente

Cuando ejecutas el script, realiza estos pasos:

```
1. ✅ Muestra los archivos modificados (git status)
2. ✅ Te pide confirmación
3. ✅ Agrega todos los cambios (git add .)
4. ✅ Crea el commit (git commit -m "mensaje")
5. ✅ Sube a GitHub (git push origin main)
6. ✅ Netlify detecta el cambio automáticamente
7. ✅ Tu sitio se actualiza en 30-60 segundos
```

---

## 🎯 Flujo de Trabajo Recomendado

### **Antes de Usar el Script:**

1. **Haz tus cambios** en los archivos del proyecto
2. **Prueba localmente** en http://localhost:3000
3. **Verifica que todo funcione** correctamente

### **Usar el Script:**

```powershell
# En la terminal, ejecuta:
.\deploy.ps1 "feat: Agregar nueva funcionalidad X"
```

### **Después del Deploy:**

1. **Espera 30-60 segundos**
2. **Visita tu sitio**: https://lifextreme-v29-pro.netlify.app
3. **Verifica los cambios** en producción

---

## 📝 Convenciones de Mensajes de Commit

Usa estos prefijos para organizar mejor tus commits:

| Prefijo | Uso | Ejemplo |
|---------|-----|---------|
| `feat:` | Nueva funcionalidad | `feat: Agregar sistema de pagos` |
| `fix:` | Corrección de bugs | `fix: Corregir error en login` |
| `docs:` | Documentación | `docs: Actualizar README` |
| `style:` | Cambios de diseño | `style: Mejorar botón Partners` |
| `refactor:` | Refactorización | `refactor: Optimizar código JS` |
| `test:` | Tests | `test: Agregar tests unitarios` |
| `chore:` | Mantenimiento | `chore: Actualizar dependencias` |

**Ejemplos completos:**
```powershell
.\deploy.ps1 "feat: Integrar Google Analytics"
.\deploy.ps1 "fix: Resolver problema de scroll en móvil"
.\deploy.ps1 "style: Actualizar colores del dashboard"
```

---

## ⚠️ Solución de Problemas

### **Error: "No se puede ejecutar scripts"**

Si ves este error:
```
.\deploy.ps1 : No se puede cargar el archivo porque la ejecución de scripts está deshabilitada
```

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Error: "git no reconocido"**

Asegúrate de tener Git instalado:
```powershell
git --version
```

Si no está instalado, descárgalo de: https://git-scm.com/download/win

### **Error: "Permission denied"**

Verifica que estás autenticado en GitHub:
```powershell
git config user.name
git config user.email
```

---

## 🎓 Comandos Git Manuales (Alternativa)

Si prefieres no usar el script, puedes hacer el deploy manualmente:

```powershell
# 1. Ver cambios
git status

# 2. Agregar archivos
git add .

# 3. Hacer commit
git commit -m "tu mensaje aquí"

# 4. Subir a GitHub
git push origin main
```

---

## 📊 Verificar el Deploy

### **En GitHub:**
1. Ve a: https://github.com/lifextremeperu/Lifextreme-Web-AI
2. Verás tu commit más reciente
3. El mensaje que pusiste aparecerá ahí

### **En Netlify:**
1. Ve a: https://app.netlify.com
2. Selecciona tu sitio "lifextreme-v29-pro"
3. Verás el deploy en progreso
4. Cuando diga "Published", tu sitio está actualizado

### **En tu Sitio Web:**
1. Abre: https://lifextreme-v29-pro.netlify.app
2. Refresca la página (Ctrl + F5)
3. Verifica tus cambios

---

## 🚀 Atajos de Teclado Útiles

| Atajo | Acción |
|-------|--------|
| `Ctrl + ` ` | Abrir/cerrar terminal en VS Code |
| `Ctrl + Shift + P` | Paleta de comandos |
| `Ctrl + S` | Guardar archivo |
| `Ctrl + F5` | Refrescar navegador (hard refresh) |

---

## 💡 Tips Pro

1. **Commits frecuentes**: Haz commits pequeños y frecuentes
2. **Mensajes descriptivos**: Usa mensajes claros y específicos
3. **Prueba local primero**: Siempre prueba antes de hacer deploy
4. **Revisa el sitio**: Verifica que todo funcione después del deploy

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de Netlify
2. Verifica el historial de commits en GitHub
3. Consulta la documentación de Git

---

**Última actualización:** 06 Enero 2026  
**Proyecto:** Lifextreme Web AI  
**Autor:** Lifextreme Tech Team
