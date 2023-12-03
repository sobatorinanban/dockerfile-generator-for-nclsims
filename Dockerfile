FROM ubuntu:20.04

ENV SIMULATOR_NAME ncl_icn-sfcsim
ENV TZ=Asia/Tokyo

WORKDIR /simulator

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update \
    && apt install -y openjdk-17-jdk ant git psmisc cron

RUN git clone https://github.com/ncl-teu/${SIMULATOR_NAME}.git \
    && cd ${SIMULATOR_NAME} \
    && ant build \
    && chmod 777 automain.sh

COPY sim_autoexecutor.sh /simulator/sim_autoexecutor.sh
RUN chmod 777 /simulator/sim_autoexecutor.sh

# test
RUN mkdir /test-sim-log

COPY crontab /etc/cron.d/crontab
# RUN echo '*/5 * * * * /bin/bash /simulator/sim_autoexecutor.sh >> /simulator/cron.log 2>&1' > /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# Start cron in the foreground
ENTRYPOINT ["cron", "-f", "-L", "15"]