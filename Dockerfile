FROM ncl-javaimg:latest

ARG SIMULATOR_NAME
ARG CONFIG_TYPE
ARG CONFIG_FILE
ARG RUN_SH

WORKDIR /simulator

COPY /sims/${SIMULATOR_NAME}/${RUN_SH} /simulator/${RUN_SH}

RUN chmod 777 ${RUN_SH}

RUN sed -i -e "s|./classes|/app/${SIMULATOR_NAME}/classes|g" -e "s|lib/|/app/${SIMULATOR_NAME}/lib/|g" ${RUN_SH}

COPY /sims/${SIMULATOR_NAME}/is /simulator/is

COPY /${CONFIG_TYPE}/${CONFIG_FILE} /simulator/${CONFIG_FILE}

COPY /${CONFIG_TYPE}/sim_autoexecutor.sh /simulator/sim_autoexecutor.sh
RUN chmod 777 /simulator/sim_autoexecutor.sh

COPY /${CONFIG_TYPE}/crontab /etc/cron.d/crontab
# RUN echo '*/5 * * * * /bin/bash /simulator/sim_autoexecutor.sh >> /simulator/cron.log 2>&1' > /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# Start cron in the foreground
ENTRYPOINT ["cron", "-f", "-L", "15"]