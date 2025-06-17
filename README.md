# despliegue-cajacelia
Repositorio que automatiza el aprovisionamiento de la infraestructura con Vagrant (Webserver, BBDD, LDAP, CI-CD, Cliente) y el despliegue de servicios de CajaCelia usando Ansible y Vagrant.

---

## 📁 Estructura del repositorio

```
└── jsegrod1512-despliegue-cajacelia/
    ├── README.md
    ├── site.yml
    ├── Vagrantfile
    ├── group_vars/
    │   ├── clients.yml
    │   ├── database.yml
    │   ├── jenkins.yml
    │   ├── ldap.yml
    │   └── webapp.yml
    ├── inventory/
    │   ├── inventory
    │   └── vagrant_dynamic.py
    ├── playbooks/
    │   ├── backup.yml
    │   ├── clear.yml
    │   ├── clients_ldap.yml
    │   ├── database.yml
    │   ├── deploy_database.yml
    │   ├── deploy_jenkins.yml
    │   ├── install_jenkins.yml
    │   ├── install_ldap.yml
    │   ├── jenkins_plugins.yml
    │   ├── manage_users_ldap.yml
    │   ├── role_setup.yml
    │   └── webapp.yml
    ├── templates/
    │   ├── 000-default.conf
    │   ├── app_schema.sql.j2
    │   ├── config-pfsense.cajacelia.es.xml.example
    │   ├── config.py.j2
    │   └── webapp.service.j2
    └── users/
        └── users.yml
```

---

## 🚀 Requisitos previos

* **Vagrant** Versión 2.4.6
* **VirtualBox** Versión 7.0 +

---

## 🔧 Despliegue con Vagrant y Ansible

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/jsegrod1512/despliegue-cajacelia.git
   cd despliegue-cajacelia
   ```

2. **Levantar VMs**

   ```bash
   vagrant up
   ```

   * Crea y configura máquinas virtuales.
   * Por defecto las maquinas se aprovisionan automáticamente cuando se crean.

3. **Reaprovisionar (para aplicar cambios del Vagrantfile o de los playbooks de Ansible)**

   ```bash
   vagrant up --provision
   ```

   o

   ```bash
   vagrant provision
   ```

---

## 🛠️ Configuración avanzada

* **Modificar `site.yml`**: Personaliza qué roles se ejecutan y en qué orden.
* **Playbooks manuales**: Si tenemos que lanzar playbooks desde la máquina CI-CD:

  ```bash
  cd /vagrant/
  ansible-playbook -i inventory/ site.yml
  ```

---

## 📜 Archivos

* **Vagrantfile**: Define las 5 VMs junto a su red, nombre de host y demás opciones, como la de ejecutar Ansible desde el servidor CI-CD.

* **site.yml**: Playbook principal que se ejecuta automáticamente al hacer `vagrant up`. Importa los siguientes playbooks en orden:

  | Playbook                | Propósito                                                                       |
  | ----------------------- | ------------------------------------------------------------------------------- |
  | install\_ldap.yml       | Instala OpenLDAP y aplica la estructura base                                    |
  | manage\_users\_ldap.yml | Despliega los usuarios en LDAP                                                  |
  | clients\_ldap.yml       | Configura los clientes para autenticarse con LDAP                               |
  | database.yml            | Instala y configura MySQL                                                       |
  | deploy\_database.yml    | Despliega la base de datos: usuario, esquemas y tablas                          |
  | webapp.yml              | Configura la aplicación web (flask-ldap-app) en el servidor web                 |
  | role\_setup.yml         | Configuración específica según el rol (Administrador / Desarrollador / Cliente) |
  | install\_jenkins.yml    | Instalación básica de Jenkins                                                   |
  | clear.yml               | Limpia caché y optimiza espacio                                                 |

  > **Importante**: Los playbooks de backups y Jenkins avanzados (jenkins\_plugins.yml, deploy\_jenkins.yml, backup.yml) no se incluyen en `site.yml` y deben ejecutarse manualmente tras configurar admin:contraseña :
  >
  > * **backup.yml**          : Crea respaldos en el servidor CI/CD
  > * **jenkins\_plugins.yml** : Instala plugins de Jenkins después de establecer el usuario admin
  > * **deploy\_jenkins.yml**  : Despliega una pipeline básica en Jenkins

* **group\_vars/**:\*\*: Variables de los distintos servidores (`ldap.yml`, `jenkins.yml`, `webapp.yml`, `database.yml`, `clients.yml`).

* **inventory/**:

  * `inventory`           : Hosts estáticos.
  * `vagrant_dynamic.py`  : Inventario dinámico para detectar a los clientes que reciben IP por DHCP.

* **templates/**: Plantillas Jinja2 para complementar los playbooks.

* **users/users.yml**: Definimos los usuarios y grupos que se almacenarán en el servidor LDAP.