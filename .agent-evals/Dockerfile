# x86-64 Linux toolchain for mkl_fft evaluation tasks (MKL is x86 only). Used through [environment].exec in
# repoevals.local.toml when the agent runs on a laptop with a different architecture.
FROM --platform=linux/amd64 python:3.12
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/requirements.txt
ENV LD_LIBRARY_PATH=/usr/local/lib
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt \
 && P=$(python -c "import sys; print(sys.prefix)") \
 && ln -sf "$(ls $P/lib/libmkl_rt.so.* | head -1)" "$P/lib/libmkl_rt.so" \
 && chmod -R a+rwX /usr/local/lib/python3.12/site-packages /usr/local/bin
