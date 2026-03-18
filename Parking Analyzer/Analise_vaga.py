import cv2
from cv2 import VideoCapture

# DELIMITAÇÃO DE LOCAL DE CADA JANELA
vaga1 = [75, 1, 130, 53]
vaga2 = [75, 61, 130, 53]
vaga3 = [75, 121, 130, 53]
vaga4 = [75, 181, 130, 53]
vaga5 = [75, 241, 130, 53]
vaga6 = [75, 301, 130, 53]
vaga7 = [75, 361, 130, 53]

vaga8 = [205, 1, 130, 53]
vaga9 = [205, 61, 130, 53]
vaga10 = [205, 121, 130, 53]
vaga11 = [205, 181, 130, 53]
vaga12 = [205, 241, 130, 53]
vaga13 = [205, 301, 130, 53]
vaga14 = [205, 361, 130, 53]

# CRIA UMA LISTA COM AS VAGAS
vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8, vaga9, vaga10, vaga11, vaga12, vaga13, vaga14]


# Abre o vídeo e aloca na variável
video = cv2.VideoCapture('parking_crop_loop.mp4')

# Abre a iamgem do gabarito e aloca na variável
mascara = cv2.imread("mask_crop.png")


# FUNÇÃO PARA TRATAMENTO EXTRAINDO AS BORDAS
def tratamento(video):
    vd_pb = cv2.cvtColor(video, cv2.COLOR_RGB2GRAY)
    # cv2.imshow("Video Preto e branco", vd_pb)
    vd_blur = cv2.blur(vd_pb, (3, 3))
    # cv2.imshow("video blur",vd_blur)
    vd_borda = cv2.Canny(vd_blur, 90, 140)
    # cv2.imshow("Video bordas", vd_borda)
    return vd_borda


# LOOP PARA LEITURA DE FRAMES
while True:
    ret, frame = video.read()  # Lê o próximo frame

    # Verifica se o frame foi lido corretamente
    if not ret:
        print("Erro: Não foi possível ler o próximo frame.")
        break

    largura, altura, _ = frame.shape  # Obtem dimensões do video

    # Redimensiona o gabarito para o mesmo tamanho do video
    mascara = cv2.resize(mascara, (altura, largura))

    # Aloca o tratamento do video numa variável
    img_tratada = tratamento(frame)

    cont = 0  # Inicia um contator para detecção de vagas livres

    # LOOP PARA TRATAMENTO DAS VAGAS COM AS JANELAS
    for x, y, w, h in vagas:

        # Especifica uma determinada janela das vagas
        recorte = img_tratada[y:y+h, x:x+w]

        # Contagem dos pixels dentro da janela especificada
        quantidade_pixel = cv2.countNonZero(recorte)

        # LÓGICA PARA ANALISAR A PRESENÇA DE UM VEÍCULO, VAGA LIVRE APROXIMADAMENTE 450 PIXELS
        if quantidade_pixel <= 450:
            cont += 1
            cor = (0, 255, 0)  # Cor Verde
            resultado = "LIVRE"

        else:
            cor = (0, 0, 255)  # Cor Vermelha
            resultado = "OCUPADO"

        # Cria um retângulo em volta das vagas
        cv2.rectangle(frame, (x, y), (x+w, y+h), cor, 2)
        # Escreve o resultado da vaga
        cv2.putText(frame, resultado, (x+5, y+h-5),
                    cv2.FONT_HERSHEY_COMPLEX, 0.25, cor, 1)

    # Escreve a quantidade total de vagas livres
    cv2.putText(frame, (f"Vaga Livre: {cont}"), (5, 440),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (20, 20, 20), 1)

    cv2.imshow("Video estacionamento", frame)  # Exibe o video

    if cv2.waitKey(25) & 0xFF == ord('e'):  # Saída do vídeo apertando a tecla "e"
        break


# Libera os recursos
video.release(0)
cv2.destroyAllWindows()
