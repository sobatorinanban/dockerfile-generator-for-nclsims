FROM ubuntu:22.04

ENV SIMULATOR_NAME ncl_icn-sfcsim

WORKDIR /simulator

RUN apt update \
    && apt install -y openjdk-17-jdk ant git cron

RUN git clone https://github.com/ncl-teu/${SIMULATOR_NAME}.git \
    && cd ${SIMULATOR_NAME} \
    && ant build

ADD sim_autoexecutor.sh /sim_autoexecutor

# test
RUN mkdir /test-sim-log

ADD crontab /var/spool/crontab/root
RUN chmod 0744 /var/spool/crontab/root/* \
    && crontab /var/spool/crontab/root

CMD ["cron" "-f"]

# EXPOSE 3000

# # Start the app using serve command
# CMD [ "serve", "-s", "build" ]