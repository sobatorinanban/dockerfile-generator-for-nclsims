FROM openjdk:11-jdk-bullseye

ENV TZ=Asia/Tokyo

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install -y git ant psmisc cron && rm -rf /var/lib/apt/lists/*

CMD [ "bash" ]