import cv2
import numpy as np



# Carregar a imagem
imagem = cv2.imread("Abafador/003.jpg")

# Converter para o espaço de cores HSV
imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
lower_skin = np.array([0, 20, 70])# Limite inferior (ajustar conforme necessário)
upper_skin = np.array([25, 255, 255])# Limite superior (ajustar conforme necessário)

mascara_pele = cv2.inRange(imagem_hsv, lower_skin, upper_skin)# Criar uma máscara para detectar a pele

# Aplicar a máscara na imagem HSV
imagem_hsv_reduzida = imagem_hsv.copy()
imagem_hsv_reduzida[:, :, 1] = cv2.subtract(
    imagem_hsv[:, :, 1], mascara_pele // 255 * 80)  # Reduz a saturação

imagem_final = cv2.cvtColor(imagem_hsv_reduzida, cv2.COLOR_HSV2BGR)# Converter de volta para BGR

# Mostrar os resultados
cv2.imshow("Original", imagem)
cv2.imshow("Saturação Reduzida", imagem_final)

# Salvar a imagem (opcional)
# cv2.imwrite("imagem_saturacao_reduzida.jpg", imagem_final)

cv2.waitKey(0)
cv2.destroyAllWindows()
