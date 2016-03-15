FROM hypriot/rpi-alpine-scratch
MAINTAINER Jocelyn Fiat

RUN apk update && apk upgrade \
	&& apk add ca-certificates \
	&& apk add libstdc++ make gcc g++ linux-headers musl-dev\
	&& apk add libxtst-dev gtk+2.0-dev \
	&& apk add curl subversion bzip2  \
	&& rm -rf /var/cache/apk/* \
	&& rm -rf /var/lib/apt/lists/*

RUN export uid=1000 gid=1000 && \
    mkdir -p /home/eiffel && \
    echo "eiffel:x:${uid}:${gid}:eiffel,,,:/home/eiffel:/bin/bash" >> /etc/passwd && \
    echo "eiffel:x:${uid}:" >> /etc/group && \
    chown ${uid}:${gid} -R /home/eiffel

# Define Eiffel environment variables
ENV 	ISE_PLATFORM=linux-armv6 \
	ISE_EIFFEL=/home/eiffel/Eiffel \
	ISE_LIBRARY=$ISE_EIFFEL \
	PATH=$PATH:$ISE_EIFFEL/studio/spec/$ISE_PLATFORM/bin:$ISE_EIFFEL/tools/spec/$ISE_PLATFORM/bin:$ISE_EIFFEL/library/gobo/spec/$ISE_PLATFORM/bin


USER eiffel
ADD ./src/install_porterpackage.sh /tmp/install_porterpackage.sh
RUN /tmp/install_porterpackage.sh $ISE_PLATFORM /home/eiffel/build $ISE_EIFFEL

