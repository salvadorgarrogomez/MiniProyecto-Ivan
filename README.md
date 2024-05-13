# agro

## Estructura

- src
  - addons, aquí van repositorios de terceros con addons
  - custom_addons, modulos a medida
- .gitlab-ci.yml, pipeline para ci/cd , por el momento crea imagen docker
- compose, prepara el contenedor de odoo con otro de postgres
- Dockerfile, aquí se monta el contenedor del cliente con sus modulos a medida
- requirements.txt, dependencias de python

## Crear imagen

docker build -t sidoo.registry.sdi.es/agro:17.0 .

Solo hace falta crear la imagen:

- Si el proyecto es nuevo y todavía no existe en el registry
- Si se ha modificado el Dockerfile, requirements.txt o se quiere actualizar oca

## Ejecutar para desarrollo

docker compose up

Por defecto crea un nueva base de datos y arranca odoo.

En el compose.yml se indica que src/custom_addons se monta en volumen local.

Podemos lanzar el contenedor sin lanzar odoo para que podamos lanzar odoo de forma manual, esto lo hacemos descomentando la línea:

- ENTRYPOINT_HOOK=NO_EXEC

Si queremos lanzar odoo de forma manual, una vez arrancado el contenedor, lo primero nos conectamos al contenedor con:

docker exec -it agro_odoo_1 /bin/bash

Luego:

/opt/odoo/src/odoo/odoo-bin -c /opt/odoo/conf/odoo.conf

Se puede actualizar ejecutando directamente

/opt/odoo/src/odoo/odoo-bin -c /opt/odoo/conf/odoo.conf -d nombre_de_base_datos -u modulo_a_actualizar

o

click-odoo-update -d nombre_de_base_datos

Esto actualiza directamente los módulos que se hayan modificado.

### Hacer debug

Se puede lanzar docker compose con la opción de ENTRYPOINT_HOOK=NO_EXEC, luego en vscode ejecutar DevContainers: Attach to Running Container.

Con esto estaremos dentro del contenedor y se podrá lanzar odoo desde vscode.

## Gestion de código custom_addons y addons de OCA

Docker compose está configurado para que custom_addons se monte en un volumen local, de esta forma podemos modificar el código sin necesidad de rehacer la imagen.

En el docker compose está comentada la línea de addons de OCA, si se descomenta se montará en un volumen local, en este caso habrá que descargar los addons de OCA para tenerlos disponibles. Esto se hace con:

gitaggregate -c repos.yaml
# MiniProyecto-Ivan
# MiniProyecto-Ivan
