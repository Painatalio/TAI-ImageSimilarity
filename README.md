# README

### Dependências e instalação

Para instalar a biblioteca OpenCV:

```
apt install libopencv-dev
export OpenCV_DIR=/usr/share/OpenCV
```

Se a live preview da câmera não funcionar corretamente, correr os seguintes comandos:

```
apt install appmenu-gtk-module-common appmenu-gtk2-module appmenu-gtk3-module
```

Para que o cv2 funcionar corretamente em python3, executar o seguinte comando:

```
pip3 install opencv-python --user
```

### Correr o programa para as classificações

Para correr as classificações usando NCD e NCCD apenas é necessário:
```bash
python3 src/classifier/classifier.py
```

### Parâmetros de classificação

De forma a podermos classificar as imagens de acordo com diferentes pré-processamentos, foram criados 2 dicionários dentro do ficheiro ```classifier.py```, em que conseguimos facilmente controlar quais os algoritmos de compressão utilizados e qual o pré-processamento  a aplicar.

```python
preprocessing = [
{"prep" : "original"},
{"prep" : "resize", "ratio": 0.5},
{"prep" : "resize", "ratio": 0.25},
{"prep" : "resize", "ratio": 0.1},
{"prep" : "quantization", "n_bits" : 4},
{"prep" : "quantization", "n_bits" : 6},
]

classifiers = [
{"classifier": "ncd", "compressor" : "gzip" },
{"classifier": "ncd", "compressor" : "bzip2" },
{"classifier": "ncd", "compressor" : "lzma" },
{"classifier": "ncd", "compressor" : "png" },
{"classifier": "ncd", "compressor" : "jpeg" },
{"classifier": "nccd", "ctx" : "ctx1" },
{"classifier": "nccd", "ctx" : "ctx2" }
]
```

Caso se pretenda utilizar apenas um algoritmo de compressão, devem-se comentar as restantes entradas do dicionário ```classifiers```.

### Reultados
Os resultados deste estudo podem ser encontrados em ```results/results.csv```. Neste ficheiro encontra-se o erro obtido para a classificação das imagens do dataset, com recurso a diversos algoritmos de compressão e a diferentes mecanismos de pré-processamento.

### Correr o programa de reconhecimento facial
O programa para o reconhecimento facial tem 2 funções: tirar fotografias e realizar o reconhecimento facial.
Para tirar fotografias, o seguinte comando deve ser exectuado, dentro da pasta ```src/camera/```:
```bash
python3 cameraRecog.py 0
```

Para realizar o reconhecimento facial:
```bash
python3 cameraRecog.py 1 ../../images/webcam_images gzip 1.01
```

### Relatório

Dentro do diretório  **report** pode ser encontrada a versão final do mesmo, em ```pdf```.



