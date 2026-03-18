
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Carregar a imagem da parte vermelha do abafador
abafador = cv2.imread("Abafador/abafador_verm.jpg", cv2.IMREAD_COLOR)


# Carregar a imagem dos operadores
imagens = ["001", "002",
           "003", "004", "005", "006", "007", "008", "009", "010", "011", "012","013","014","015"]
# imagens = ["abafador_001", "abafador_002"]

# FUNÇÃO DE PROCESSAMENTO DA IMAGEM
def pre_processamento(img):
    # img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
    # cv2.imshow('color',img)
    imgpre = cv2.Canny(img, 200, 800)
    cv2.imshow("Bordas", imgpre)
    kernel = np.ones((5, 5), np.uint8)
    imgpre = cv2.dilate(imgpre, kernel, 2)
    imgpre = cv2.erode(imgpre, kernel, 2)
    cv2.imshow("Bordas 2", imgpre)
    return imgpre




# Loop para realizar os testes em todas as imagens
for i in imagens:
    cv2.destroyAllWindows()

    # Aloca a imagem do operador da vez na variável
    operador = cv2.imread(f"Abafador/{i}.jpg")ee
    
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

    # Iterar sobre os pixels da imagem permitindo manter somente os pixels que estão entre o máximo e mínio do RGB da imagem de controle(cor do abafador)
    # Se o valor do pixel da cartela estiver entre o máx e mín da imagem de controle adiciona na matriz de zeros criada, caso não, deixe vazia
    for x in range(largura):
        for y in range(altura):
            if (operador[x, y, 0] <= rmax and operador[x, y, 0] >= rmin and operador[x, y, 1] <= gmax and operador[x, y, 1] >= gmin and operador[x, y, 2] <= bmax and operador[x, y, 2] >= bmin):
                img_recortada[x, y, :] = operador[x, y, :]

    cv2.imshow("Imagem com recorte", img_recortada)

    

    
    # Aloca a chamada da função de tratamento da imagem à variável
    bordas = pre_processamento(img_recortada)

    # Identifica as bordas do tratamento de imagem
    contornos, _ = cv2.findContours(
        bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    print(type(bordas))
    cv2.imshow("bordas", bordas)
    # img_cinza = cv2.cvtColor(bordas, cv2.COLOR_BGR2GRAY)

    # # Contar pixels diferentes de zero (tons de vermelho recortados)
    quantidade_pixel = cv2.countNonZero(bordas)

    print(f"Número de pixels em tons de vermelho: {quantidade_pixel}")
    

    if quantidade_pixel >= 600:
        # cont += 1
        cor = (0, 255, 0)  # Cor Verde
        resultado = "LIVRE"

    else:
        cor = (0, 0, 255)  # Cor Vermelha
        resultado = "OCUPADO"


    # LOOP PARA IDENTIICAÇÃO E DELIMITAÇÃO DOS CONTORNOS
    for contorno in contornos:

        # Calcular o retângulo delimitador para cada contorno
        x, y, w, h = cv2.boundingRect(contorno)
        # Desenhar o retângulo na imagem original
        cv2.rectangle(operador, (x, y), (x + w, y + h), cor, 2)
    
    cv2.putText(img_recortada, resultado, (x+5, y+h-5),
                    cv2.FONT_HERSHEY_COMPLEX, 0.25, cor, 1)

    # Cria uma cópia da imagem original para mostragem final
    imagem_contornos = operador.copy()

    # Escreve a mensagem na imagem, referente a inspeção e quantidade de pixels
    cv2.putText(imagem_contornos, (f"Vaga Livre: {resultado}"), (5, 440),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)

    # Exibir a imagem com os contornos e com o veredito
    cv2.imshow(f"Imagem operador {i}", imagem_contornos)

    altura, largura, _ = imagem.shape

    # Criar uma máscara inicial preenchida com zeros
    mascara = np.zeros((altura, largura), dtype=np.uint8)

    for (x, y, w, h) in faces:
        # Retângulo original (azul)
        cv2.rectangle(imagem, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Coordenadas do segundo retângulo (preto)
        linha_sup = y + h // 5
        linha_inf = (y + h) * 4 // 5
        cv2.rectangle(imagem, (int(x-(x/1.2)), linha_sup), (int((x+w)*1.2), linha_inf), (0, 0, 0), 2)


        # Criar a máscara para o segundo retângulo
        cv2.rectangle(mascara, (int(x-(x/1.2)), linha_sup),
                      (int((x+w)*1.2), linha_inf), 255, -1)

        # Ponto central (vermelho)
        centro_x = x + w // 2
        centro_y = y + h // 2
        cv2.circle(imagem, (centro_x, centro_y), 5, (0, 0, 255), -1)

    # Exibir a imagem com retângulos e ponto
    cv2.imshow(f"Imagem com Retângulos e Ponto", imagem)

    recorte = cv2.bitwise_and(imagem, imagem, mask=mascara)

    # Exibir o recorte
    cv2.imshow("Recorte da Imagem", recorte)

    # Esperar entrada do usuário
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


