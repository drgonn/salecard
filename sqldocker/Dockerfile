# 使用官方PostgreSQL基础镜像
FROM postgres:14.5

# 设置环境变量，指定数据库名称、用户名、密码和端口
ENV POSTGRES_DB iwp3
ENV POSTGRES_USER root
ENV POSTGRES_PASSWORD root
ENV POSTGRES_HOST postgres_fastweek
ENV POSTGRES_PORT 5432

# 复制自定义配置文件到容器中（可选）
# COPY custom_postgresql.conf /etc/postgresql/postgresql.conf
# 映射数据库文件出来
VOLUME /var/lib/postgresql/data /root/postgresql/data

# 暴露PostgreSQL默认端口
EXPOSE 5432
