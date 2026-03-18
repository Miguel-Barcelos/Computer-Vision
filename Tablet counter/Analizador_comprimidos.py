
import cv2
import numpy as np

# Carregar a imagem da parte azul do comprimido, imagem de controle
remedio = cv2.imread("Banco de imagens\parte_azul.jpg", cv2.IMREAD_COLOR)

# Carregar a imagem das cartelas
imagens = ["cart_001", "cart_002", "cart_003",
           "cart_004", "cart_005", "cart_006", "cart_007", "cart_008", "cart_009", "cart_010", "cart_011", "cart_012"]

# Loop para realizar os testes em todas as cartelas
for i in imagens:

    # Aloca a cartela da vez na variável
    cartela = cv2.imread(f"Banco de imagens/{i}.jpg")

    # Calcular os valores máximos e mínimos do vermelho 
    rmax = np.max(remedio[:, :, 0])
    rmin = np.min(remedio[:, :, 0])

    # Calcular os valores máximos e mínimos do verde
    gmax = np.max(remedio[:, :, 1])
    gmin = np.min(remedio[:, :, 1])

    # Calcular os valores máximos e mínimos do azul
    bmax = np.max(remedio[:, :, 2])
    bmin = np.min(remedio[:, :, 2])

    # Obter o tamanho da imagem das cartelas
    largura, altura, _ = cartela.shape

    # Inicializar a matriz com tamanho igual ao da imagem da cartela
    img_recortada = np.zeros_like(cartela)

    # Iterar sobre os pixels do cubo permitindo manter somente os pixels que estão entre o máximo e mínio do RGB da imagem de controle
    for x in range(largura):
        for y in range(altura):
            if (cartela[x, y, 0] <= rmax and cartela[x, y, 0] >= rmin and cartela[x, y, 1] <= gmax and cartela[x, y, 1] >= gmin and cartela[x, y, 2] <= bmax and cartela[x, y, 2] >= bmin): # Se o valor do pixel da cartela estiver entre o máx e mín da imagem de controle adiciona na matriz de zeros criada, caso não, deixe vazia
                img_recortada[x, y, :] = cartela[x, y, :]

    cv2.imshow("Imagem com recorte", img_recortada)


# FUNÇÃO DE PROCESSAMENTO DA IMAGEM
    def pre_processamento(img):
        imgpre = cv2.Canny(img, 200, 800)
        cv2.imshow("Bordas", imgpre)
        kernel = np.ones((3, 3), np.uint8)
        imgpre = cv2.dilate(imgpre, kernel, 2)
        imgpre = cv2.erode(imgpre, kernel, 2)
        cv2.imshow("Bordas 2", imgpre)
        return imgpre


    bordas = pre_processamento(img_recortada) # Aloca a chamada da função de tratamento da imagem à variável 

    contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Identifica as bordas do tratamento de imagem

    num_comprimido = len(contornos) # Calcula quantos conjutos de bordas existem = Quantos comprimidos

    # IDENTIFICA A INSPEÇÃO
    if num_comprimido == 15 :
        inspecao = "APROVADO"
        cor = (67, 232, 67) #VERDE
    else:
        inspecao = "REPROVADO"
        cor = (67, 67, 232) #VERMELHO

    # LOOP PARA IDENTIICAÇÃO E DELIMITAÇÃO DOS CONTORNOS 
    for contorno in contornos:
        
        x, y, w, h = cv2.boundingRect(contorno) # Calcular o retângulo delimitador para cada contorno
        cv2.rectangle(cartela, (x, y), (x + w, y + h), cor, 2) # Desenhar o retângulo na imagem original


    imagem_contornos = cartela.copy() # Cria uma cópia da imagem original para mostragem final

    cv2.rectangle(imagem_contornos, (10, 10), (370, 40), (138, 135, 135), -1) # Cria plano de fundo para destacar a mensagem

    cv2.putText(imagem_contornos, f"{inspecao}, {num_comprimido} Comprimidos", (20, 35), cv2.FONT_HERSHEY_DUPLEX, 0.7, cor, 1) # Escreve a mensagem na imagem, referente a inspeção e quantidade de comprimidos

    cv2.imshow(f"Imagem da cartela {i}", imagem_contornos) # Exibir a imagem com os contornos e com o veredito

    # FECHAR O PROGRAMA
    cv2.waitKey(0)
    cv2.destroyAllWindows()


