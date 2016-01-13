FROM eiffel/develop:dev
MAINTAINER Jocelyn Fiat

USER eiffel
EXPOSE 80 9090 9999

USER root
RUN apt-get install -y vim tmux

RUN apt-get install -y apache2 libapache2-mod-fcgid libfcgi-dev
RUN a2enmod rewrite
RUN a2enmod suexec
RUN a2enmod include
RUN a2enmod fcgid
RUN service apache2 restart

USER eiffel
RUN svn update $EIFFEL_SRC
RUN mkdir ~/projects
WORKDIR ~/projects
RUN git clone https://github.com/EiffelWebFramework/ROC.git ~/projects/ROC
ENV ROCDIR $HOME/projects/ROC
WORKDIR $ROCDIR/examples/demo
#RUN ec -config demo-safe.ecf -target demo_standalone_scoop -finalize -c_compile
#RUN cp EIFGENs/demo_standalone_scoop/F_code/demo demo

#RUN ec -config demo-safe.ecf -target demo_libfcgi -finalize -c_compile
#RUN cp EIFGENs/demo_libfcgi/F_code/demo demo.fcgi

RUN git remote add javier https://github.com/jvelilla/ROC.git
RUN git remote update
RUN git config user.email "git@example.com" 
RUN git checkout -b roc_register javier/roc_register

#ENTRYPOINT ["$ROCDIR/examples/demo/

RUN ec -config demo-safe.ecf -target demo_standalone_scoop -freeze -c_compile

COPY ./files /home/eiffel

#ENTRYPOINT ["estudio"]
#CMD ["-config", "/home/eiffel/projects/ROC/examples/demo/demo-safe.ecf", "-target", "demo_standalone_scoop"]

ENTRYPOINT ["/bin/bash", "/home/eiffel/docker_entrypoint.sh"]
CMD ["demo"]

