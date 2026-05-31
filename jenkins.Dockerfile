# Jenkins LTS + Docker CLI (파이프라인에서 docker build/push 하기 위함)
FROM jenkins/jenkins:lts

USER root

# Docker CLI(static 바이너리)만 설치 — 데몬은 호스트의 docker.sock을 마운트해서 사용
ARG DOCKER_VERSION=27.5.1
RUN curl -fsSL "https://download.docker.com/linux/static/stable/aarch64/docker-${DOCKER_VERSION}.tgz" -o /tmp/docker.tgz \
    && tar -xzf /tmp/docker.tgz -C /tmp \
    && cp /tmp/docker/docker /usr/local/bin/docker \
    && chmod +x /usr/local/bin/docker \
    && rm -rf /tmp/docker /tmp/docker.tgz

# 마운트된 /var/run/docker.sock 의 소유 그룹이 root 이므로,
# jenkins 유저를 root 그룹에 추가해 socket 접근 권한 부여
RUN usermod -aG root jenkins

USER jenkins
