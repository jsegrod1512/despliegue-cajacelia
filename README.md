# ansible-cajacelia
Repositorio con el playbook de ansible para el Proyecto de Cajacelia, despliegue de Webserver, Servidor de BBDD y Servidor LDAP

La estructura del repositorio es la siguiente:
ansible-cajacelia/
├── .gitignore
├── README.md
├── inventory/
│   ├── production.ini         # Inventario de producción (hosts virtuales)
│   └── staging.ini            # Inventario de staging/tests
├── playbooks/
│   ├── webserver.yml          # Playbook para configurar Apache/Nginx + PHP
│   ├── database.yml           # Playbook para instalar y configurar MySQL
│   └── ldap.yml               # Playbook para desplegar OpenLDAP
├── roles/
│   ├── webserver/             # Estructura de role Webserver
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── vhost.conf.j2
│   │   └── vars/
│   │       └── main.yml
│   ├── database/              # Role MySQL
│   │   ├── tasks/
│   │   ├── handlers/
│   │   ├── templates/
│   │   └── vars/
│   └── ldap/                  # Role OpenLDAP
│       ├── tasks/
│       ├── handlers/
│       ├── templates/
│       └── vars/
├── group_vars/
│   ├── all.yml                # Variables globales (versión PHP, credenciales)
│   └── webservers.yml         # Variables específicas de webservers
├── host_vars/
│   └── server1.yml            # Variables para un host concreto si hace falta
└── site.yml                   # Playbook principal (incluye roles y despliega todo)

# 1. 
Ejecutaremos un playbook con:
``` bash
   ansible-playbook -i inventory/production.ini site.yml
```