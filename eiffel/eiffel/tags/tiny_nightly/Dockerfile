FROM alpine
MAINTAINER Jocelyn Fiat

RUN apk update && apk upgrade \
	&& apk add ca-certificates \
	&& apk add libstdc++ make gcc g++ linux-headers musl-dev\
	&& apk add libxtst-dev gtk+2.0-dev \
	&& apk add curl subversion bzip2  \
	&& rm -rf /var/cache/apk/*

RUN export uid=1000 gid=1000 && \
    mkdir -p /home/eiffel && \
    echo "eiffel:x:${uid}:${gid}:eiffel,,,:/home/eiffel:/bin/bash" >> /etc/passwd && \
    echo "eiffel:x:${uid}:" >> /etc/group && \
    chown ${uid}:${gid} -R /home/eiffel

# Define Eiffel environment variables
ENV ISE_PLATFORM linux-x86-64
ENV ISE_EIFFEL /usr/local/Eiffel
ENV ISE_LIBRARY $ISE_EIFFEL
ENV HOME /home/eiffel

USER eiffel
RUN mkdir -p /home/eiffel/build && curl -L https://ftp.eiffel.com/pub/beta/nightly/PorterPackage_NIGHTLY.tar | tar x -C /home/eiffel/build
ADD ./fix_runtime.sh /home/eiffel/build/PorterPackage/fix_runtime.sh
RUN cd /home/eiffel/build/PorterPackage && /bin/sh ./fix_runtime.sh
RUN cd /home/eiffel/build/PorterPackage && ./compile_exes $ISE_PLATFORM
ENV PATH $PATH:$ISE_EIFFEL/studio/spec/$ISE_PLATFORM/bin:$ISE_EIFFEL/tools/spec/$ISE_PLATFORM/bin:$ISE_EIFFEL/library/gobo/spec/$ISE_PLATFORM/bin

USER root
RUN mv /home/eiffel/build/PorterPackage/Eiffel_*.* $ISE_EIFFEL && rm -rf /home/eiffel/build

USER eiffel
