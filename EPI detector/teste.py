import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Carregar a imagem da parte vermelha do abafador
abafador = cv2.imread("Abafador/abafador_verm.jpg", cv2.IMREAD_COLOR)

# Carregar a lista de imagens dos operadores
imagens = ["abafador_001", "abafador_002",
           "abafador_003", "abafador_004", "abafador_005",
           "abafador_006", "abafador_007", "abafador_008",
           "abafador_009", "abafador_010", "abafador_011",
           "abafador_012"]

# Loop para realizar os testes em todas as imagens
for i in imagens:
    # Aloca a imagem do operador da vez na variável
    operador = cv2.imread(f"Abafador/{i}.jpg")
    imagem = operador.copy()
    gray = cv2.cvtColor(operador, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

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
    largura, altura, _ = operador.shape

    # Inicializar a matriz com tamanho igual ao da imagem do operador
    img_recortada = np.zeros_like(operador)

    # Iterar sobre os pixels da imagem
    for x in range(largura):
        for y in range(altura):
            if (operador[x, y, 0] <= rmax and operador[x, y, 0] >= rmin and
                operador[x, y, 1] <= gmax and operador[x, y, 1] >= gmin and
                    operador[x, y, 2] <= bmax and operador[x, y, 2] >= bmin):
                img_recortada[x, y, :] = operador[x, y, :]

    cv2.imshow("Imagem com recorte", img_recortada)

    # FUNÇÃO DE PROCESSAMENTO DA IMAGEM
    def pre_processamento(img):
        imgpre = cv2.Canny(img, 200, 800)
        cv2.imshow("Bordas", imgpre)
        kernel = np.ones((5, 5), np.uint8)
        imgpre = cv2.dilate(imgpre, kernel, 2)
        imgpre = cv2.erode(imgpre, kernel, 2)
        cv2.imshow("Bordas 2", imgpre)
        return imgpre

    bordas = pre_processamento(img_recortada)

    contornos, _ = cv2.findContours(
        bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    num_comprimido = len(contornos)

    # IDENTIFICA A INSPEÇÃO
    if num_comprimido == 15:
        inspecao = "REPROVADO"
        cor = (67, 232, 67)  # VERDE
    else:
        inspecao = "APROVADO"
        cor = (67, 67, 232)  # VERMELHO

    for contorno in contornos:
        x, y, w, h = cv2.boundingRect(contorno)
        cv2.rectangle(operador, (x, y), (x + w, y + h), cor, 2)

    imagem_contornos = operador.copy()

    cv2.putText(imagem_contornos, f"{inspecao}",
                (20, 35), cv2.FONT_HERSHEY_DUPLEX, 0.7, cor, 1)

    cv2.imshow(f"Imagem operador {i}", imagem_contornos)

    # Mostrar ponto central das faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(imagem, (x, y), (x+w, y+h), (255, 0, 0), 2)
        centro_x = x + w // 2
        centro_y = y + h // 2
        cv2.circle(imagem, (centro_x, centro_y), 5, (0, 0, 255), -1)

    cv2.imshow(f"Imagem ponto central {i}", imagem)

    # Aguardar entrada do usuário para avançar
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

# Fechar todas as janelas no final
cv2.destroyAllWindows()
