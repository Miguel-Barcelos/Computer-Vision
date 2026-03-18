
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Carregar a imagem da parte vermelha do abafador
abafador = cv2.imread("Abafador/vermelho.jpg", cv2.IMREAD_COLOR)


# Carregar a imagem dos operadores
imagens = ["001", "002","003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015"]
# imagens = ["abafador_001", "abafador_002"]

# FUNÇÃO DE PROCESSAMENTO DA IMAGEM


def pre_processamento(img):
    # img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
    cv2.imshow('color',img)
    imgpre = cv2.Canny(img, 200, 1000)
    cv2.imshow("Bordas", imgpre)
    kernel = np.ones((5, 5))
    imgpre = cv2.dilate(imgpre, kernel, 2)
    imgpre = cv2.erode(imgpre, kernel, 2)
    # cv2.imshow("Bordas 2", imgpre)
    return imgpre


# Loop para realizar os testes em todas as imagens
def analisar_imagem(filepath):
    cv2.destroyAllWindows()

    # Aloca a imagem do operador da vez na variável
    operador = cv2.imread(filepath)
    operador = cv2.resize(operador, (354, 354))
    imagem_hsv = cv2.cvtColor(
        operador, cv2.COLOR_BGR2HSV)  # Converter para HSV
    lower_skin = np.array([0, 20, 70])  # Limite inferior
    upper_skin = np.array([100, 255, 255])  # Limite superior

    # Criar uma máscara para detectar a pele
    mascara_pele = cv2.inRange(imagem_hsv, lower_skin, upper_skin)

    # Aplicar a máscara na imagem HSV
    imagem_hsv_reduzida = imagem_hsv.copy()
    imagem_hsv_reduzida[:, :, 1] = cv2.subtract(
        imagem_hsv[:, :, 1], mascara_pele // 255 * 90)  # Reduz a saturação

    imagem_final = cv2.cvtColor(
        imagem_hsv_reduzida, cv2.COLOR_HSV2BGR)  # Volta para BGR
    cv2.imshow("stauração", imagem_final)

    imagem = operador.copy()

    gray = cv2.cvtColor(operador, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    altura, largura, _ = imagem.shape
    mascara = np.zeros((altura, largura), dtype=np.uint8)

    for (x, y, w, h) in faces:
        # Retângulo original (azul)
        # cv2.rectangle(imagem, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Coordenadas do segundo retângulo (preto)
        linha_sup = y + h // 4
        linha_inf = (y + h) * 3 // 4
        # cv2.rectangle(imagem, (int(x-(x/1.2)), linha_sup),(int((x+w)*1.2), linha_inf), (0, 0, 0), 2)

        # Criar a máscara para o segundo retângulo
        cv2.rectangle(mascara, (int(x-(x/1.2)), linha_sup),
                      (int((x+w)*1.2), linha_inf), 255, -1)

        # Ponto central (vermelho)
        # centro_x = x + w // 2
        # centro_y = y + h // 2
        # cv2.circle(imagem, (centro_x, centro_y), 5, (0, 0, 255), -1)

    # Exibir a imagem com retângulos e ponto
    # cv2.imshow(f"Imagem com Retângulos e Ponto", imagem)

    recorte_olhos = cv2.bitwise_and(imagem_final, imagem_final, mask=mascara)

    # Exibir o recorte
    cv2.imshow("Recorte da Imagem", recorte_olhos)

    # BUSCA POR TONS VERMELHOS
    # Calcular os valores máximos e mínimos do vermelho
    rmax = np.max(abafador[:, :, 0])
    rmin = np.min(abafador[:, :, 0])

    # Calcular os valores máximos e mínimos do verde
    gmax = np.max(abafador[:, :, 1])
    gmin = np.min(abafador[:, :, 1])

    # Calcular os valores máximos e mínimos do azul
    bmax = np.max(abafador[:, :, 2])
    bmin = np.min(abafador[:, :, 2])

    # Obter o tamanho da imagem da foto do operador
    largura, altura, _ = recorte_olhos.shape

    # Inicializar a matriz com tamanho igual ao da imagem do operador
    img_recortada = np.zeros_like(recorte_olhos)

    # Iterar sobre os pixels da imagem permitindo manter somente os pixels que estão entre o máximo e mínio do RGB da imagem de controle(cor do abafador)
    # Se o valor do pixel da cartela estiver entre o máx e mín da imagem de controle adiciona na matriz de zeros criada, caso não, deixe vazia
    for x in range(largura):
        for y in range(altura):
            if (operador[x, y, 0] <= rmax and operador[x, y, 0] >= rmin and operador[x, y, 1] <= gmax and operador[x, y, 1] >= gmin and operador[x, y, 2] <= bmax and operador[x, y, 2] >= bmin):
                img_recortada[x, y, :] = recorte_olhos[x, y, :]

    # Aloca a chamada da função de tratamento da imagem à variável
    bordas = pre_processamento(img_recortada)

    # Identifica as bordas do tratamento de imagem
    contornos, _ = cv2.findContours(
        bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Contar pixels diferentes de zero (tons de vermelho recortados)
    quantidade_pixel = cv2.countNonZero(bordas)

    if quantidade_pixel >= 200:
        cor = (0, 255, 0)  # Cor Verde
        resultado = "LIVRE"

    else:
        cor = (0, 0, 255)  # Cor Vermelha
        resultado = "BLOQUEADO"

    # LOOP PARA IDENTIICAÇÃO E DELIMITAÇÃO DOS CONTORNOS
    for contorno in contornos:
        if resultado == "LIVRE":

            # Calcular o retângulo delimitador para cada contorno
            x, y, w, h = cv2.boundingRect(contorno)
            # Desenhar o retângulo na imagem original
            cv2.rectangle(imagem, (x, y), (x + w, y + h), cor, 2)

    cv2.putText(imagem, resultado, (int(x-(x/1.2)), linha_sup),cv2.FONT_HERSHEY_COMPLEX, 0.5, cor, 1)

    # cv2.imshow("Imagem com recorte", img_recortada)
    cv2.imshow(f"Imagem com Retângulos e Ponto", imagem)

    # Esperar entrada do usuário
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


analisar_imagem("Abafador/003.jpg")
