Repo para web de desencriptacion de documentos PDF con formato de contraseña Adobe Acrobat

--Remember
    -Whenever you feel like giving up, think of all the people that would love
    to see you fail.

--Instalación en Ubuntu Test

    -mkdir -p ~/src
    -sudo apt-get -y install git build-essential libssl-dev zlib1g-dev

    -recomended 
    -sudo apt-get -y install yasm pkg-config libgmp-dev libpcap-dev libbz2-dev

    -For Nvidia
    -sudo apt-get -y install nvidia-opencl-dev

    -For Amd
    -sudo apt-get -y install ocl-icd-opencl-dev opencl-headers

    -Inici instalació Repo
    -cd ~/src
    -git clone https://github.com/openwall/john -b bleeding-jumbo john

    -Build
    -cd ~/src/john/src
    -./configure && make -s clean && make -sj4

    -Test build
    -cd ~/src/john/run
    -./john --test=0

    -Benchmark
    -./john --test
    
--Instalacion Windows

    -Ruta cd /cygdrive/c/Users/Daniel/Desktop/jhonjumbo/john-bleeding-jumbo/src

    -./configure && make -s clean && make -sj4
    -make windows-package
