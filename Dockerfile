ARG IMAGE=store/intersystems/iris-community:2020.1.0.215.0
ARG IMAGE=store/intersystems/iris-community:2020.2.0.204.0
ARG IMAGE=store/intersystems/iris-community
FROM $IMAGE

COPY --chown=irisowner ./src/ /app

USER root

# Install and Configure Apache+PHP+php_iris
RUN apt update \
 && apt -y install python3 python3-pip mysql-client \
 && pip3 install /app/nativeAPI/irisnative-1.0.0-cp34-abi3-linux_x86_64.whl \
 && pip3 install PyMySQL flask wtforms

#### Set up the irisowner account and load application
USER irisowner

COPY --chown=irisowner Installer.cls .
COPY  --chown=irisowner irissession.sh /
RUN chmod +x /irissession.sh

# Configure this demo IRIS instance
SHELL ["/irissession.sh"]

# Set up anything you may need in Objectscript
RUN \
  do $SYSTEM.OBJ.Load("Installer.cls", "ck") \
  set sc = ##class(App.Installer).setup() 

ENV PATH="/usr/irissys/bin/:${PATH}"

# bringing the standard shell back
SHELL ["/bin/bash", "-c"]

USER root
RUN echo "cd /app" > /startFlack.sh && echo "python3 app.py > /log.txt" >> /startFlack.sh && chmod +x /startFlack.sh
CMD [ "-a", "/startFlack.sh" ]
