FROM python:3.7
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN echo "LANG=en_US.UTF-8" > /etc/locale.conf
RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen en_US.UTF-8
RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y update
RUN pip install setuptools
RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y
RUN pip install --upgrade pip
RUN apt-get -y update
RUN pip install opencv-python==4.5.1.48
RUN apt-get install -y ca-certificates
RUN apt install -y openslide-tools
RUN pip install openslide-python
RUN pip install pandas
RUN pip install matplotlib
RUN pip install h5py
RUN pip install torchvision
RUN pip install torchsummary
RUN apt-get -y update
RUN git clone "https://github.com/oval-group/smooth-topk.git" /usr/local/src/st
RUN python /usr/local/src/st/setup.py install
RUN git clone "https://github.com/Pacific89/CLAM.git" /usr/local/src/clam
RUN git clone "https://github.com/Pacific89/docker" /usr/local/wrapper
RUN ["mkdir", "/usr/local/config"]
RUN ["cp", "/usr/local/wrapper/clam/clam_command_config.json", "/usr/local/config"]
# RUN pip install jupyter
# RUN ["cp", "/usr/local/src/clam/clam_command_config.json", "/usr/local/config"]
# CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
ENTRYPOINT [ "python", "/usr/local/wrapper/clam/start_create_patches.py" ]
# ENTRYPOINT [ "bin/bash" ]