#Usage : docker run -i -t -e "DISPLAY=192.168.1.4:0" jocelyn/eiffel-dev:iron-dev

FROM eiffel/devenv:trunk
MAINTAINER Jocelyn Fiat
LABEL description="Dev environment for IRON project."
EXPOSE 80 8080

USER root
#EiffelWeb framework
RUN apt-get install -y apache2 libapache2-mod-fcgid libfcgi-dev
RUN a2enmod rewrite
#RUN a2enmod suexec
#RUN a2enmod include
RUN a2enmod fcgid
RUN service apache2 restart

RUN apt-get install -y vim tmux

USER eiffel
ENV HOME /home/eiffel
COPY home/eiffel/trunk/Src/tools/iron/scripts/ /home/eiffel/trunk/Src/tools/iron/scripts/
WORKDIR /home/eiffel/trunk/Src/tools/iron/scripts/
USER root
RUN /bin/chown eiffel -R /home/eiffel/trunk/Src/tools/iron/scripts/

USER eiffel
RUN /bin/chmod u+x /home/eiffel/trunk/Src/tools/iron/scripts/*.sh
WORKDIR /home/eiffel/trunk/Src/tools/iron/scripts/
RUN ./prepare.sh

#RUN geant prepare

USER eiffel
#CMD xterm
