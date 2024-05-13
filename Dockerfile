FROM sidoo.registry.sdi.es/sidooker-base:17.0

USER root

WORKDIR /opt/odoo
COPY . .

# Copia custom_addons y repos.yaml
RUN chown -R odoo:odoo /opt/odoo/src/addons/oca
RUN chown -R odoo:odoo /opt/odoo/src/custom_addons

# Dependencias
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Descargar repositorios e instala dependencias

WORKDIR /opt/odoo/src/addons/oca
RUN gitaggregate -c /opt/odoo/src/addons/oca/repos.yaml

# Compile the code.
RUN python3 -m compileall -q /opt/odoo/src/addons/oca
RUN python3 -m compileall -q /opt/odoo/src/custom_addons


# Delete the .git directories to reduce the size of the image.
RUN find /opt/odoo/src/addons/oca -name '.git*' -type d -exec rm -rf {}/* \;

WORKDIR /opt/odoo
ENTRYPOINT ["/bin/sh", "-c", "/opt/odoo/bin/entrypoint"]
