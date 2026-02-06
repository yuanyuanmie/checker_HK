# 1. 使用 Miniconda 官方镜像
FROM continuumio/miniconda3

# 2. 暴露端口
EXPOSE 8030

# 3. 保持 Python 不产生 .pyc 文件 & 无缓冲日志
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 设置工作目录
WORKDIR /app

# 5. 复制 Conda 环境文件
COPY environment.yml .

# 6. 创建 Conda 环境
RUN conda env create -f environment.yml

# 7. 将 Conda 环境的 bin 目录加入 PATH
# 假设 environment.yml 中 name: your_env_name
ENV PATH="/opt/conda/envs/agent_checker_hk/bin:$PATH"

# 8. 复制项目代码
COPY . /app

# 9. 创建非 root 用户并授权
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# 10. 启动命令 (Gunicorn + Uvicorn Worker)
CMD ["gunicorn", "--bind", "0.0.0.0:8030", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
