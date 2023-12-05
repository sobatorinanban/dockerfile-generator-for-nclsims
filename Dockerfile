FROM ubuntu:20.04

ENV SIMULATOR_NAME ncl_icn-sfcsim
ENV LOGBACKUP_DIR /simulator-logs
ENV CONFIG_FILE nfv.properties
ENV CONFIG_TYPE random/0
ENV RUN_SH nfvrun.sh
ENV TZ=Asia/Tokyo

WORKDIR /simulator

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update \
    && apt install -y openjdk-17-jdk ant git psmisc cron

RUN git clone https://github.com/ncl-teu/${SIMULATOR_NAME}.git \
    && cd ${SIMULATOR_NAME} \
    && ant build \
    && chmod 777 ${RUN_SH}

COPY ${CONFIG_FILE} /simulator/${SIMULATOR_NAME}/${CONFIG_FILE}

COPY sim_autoexecutor.sh /simulator/sim_autoexecutor.sh
RUN chmod 777 /simulator/sim_autoexecutor.sh

# test
RUN mkdir -p ${LOGBACKUP_DIR}/${CONFIG_TYPE}

COPY crontab /etc/cron.d/crontab
# RUN echo '*/5 * * * * /bin/bash /simulator/sim_autoexecutor.sh >> /simulator/cron.log 2>&1' > /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# Start cron in the foreground
ENTRYPOINT ["cron", "-f", "-L", "15"]