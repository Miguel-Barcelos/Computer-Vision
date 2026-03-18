from tkinter import *
from tkinter import filedialog
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


import cv2
import numpy as np

customtkinter.set_appearance_mode("System")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # customtkinter.set_appearance_mode("System")
        epiValue = ["Abafador", "Óculos", "Máscara"]

        


        # Função para abrir o diálogo de seleção de arquivo


        # def selecionar_imagem(self):
        #         # Abrir diálogo e processar a imagem
        #         filepath = filedialog.askopenfilename(
        #             filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")]
        #         )
        #         if filepath:
        #             resultado, imagem = analisar_imagem(filepath)
        #             self.atualizar_interface(resultado)


        # Configurações da janela principal
        self.title("Analisador de EPI")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(2, weight=1)

        # Sidebar com widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=100, corner_radius=10
        )
        self.sidebar_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew"
        )
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        self.comboboxEpi = customtkinter.CTkOptionMenu(
            master=self.sidebar_frame,
            values=epiValue,
            width=200,
            height=50,
        )
        self.comboboxEpi.grid(
            row=1, column=1, padx=(5, 20), pady=10, sticky="w")
        self.comboboxEpi.set("Selecione o EPI")

        self.buttonAddPhoto = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Adicionar imagem",
            width=200,
            height=50,
            border_width=2,
            corner_radius=10,
            command=lambda: self.selecionar_imagem(),
        )
        self.buttonAddPhoto.grid(
            row=2, column=0, padx=50, pady=(20, 10), columnspan=2)

        # Frame principal
        self.main_frame = customtkinter.CTkFrame(
            self, width=600, corner_radius=10
        )
        self.main_frame.grid(
            row=0, column=2, padx=(10, 10), pady=(20, 20), sticky="nsew"
        )
        self.main_frame.grid_rowconfigure(5, weight=1)

        self.name_label = customtkinter.CTkLabel(
            self.main_frame,
            text="Analisador de Equipamentos Individuais",
            font=customtkinter.CTkFont(size=30, weight="bold"),
        )
        self.name_label.grid(
            row=0,
            column=0,
            padx=50,
            pady=(20, 10),
            sticky="nsew",
            columnspan=2,
        )

        # self.textboxGcode = customtkinter.CTkTextbox(self.main_frame, width=500, height=350)
        
        self.plotframe = customtkinter.CTkFrame(self.main_frame, width=500, height=450, fg_color=("black", "lightgray"))
        # self.plotframe = customtkinter.CTkFrame(self.main_frame, width=350, height=350, fg_color=("black", "lightgray"))
        self.plotframe.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="n")

        
        

        
        

        # self.label_imagem = customtkinter.CTkLabel(self.plotframe, image=imagem, text="")
        # self.label_imagem.image = imagem
        # self.label_imagem.place(relx=0.5, rely=0.5, anchor="center")
        

        # Indicador colorido
        self.plotframe = customtkinter.CTkFrame(
            self.main_frame, width=300, height=100, fg_color=("black", "gray")
        )
        self.plotframe.grid(row=5, column=2, padx=(10), pady=(10), sticky="se")

    

        # Loop para realizar os testes em todas as imagens

    def analisar_imagem(self,filepath):

            # def pre_processamento(img):

            #     imgpre = cv2.Canny(img, 200, 1000)
            #     kernel = np.ones((5, 5))
            #     imgpre = cv2.dilate(imgpre, kernel, 2)
            #     imgpre = cv2.erode(imgpre, kernel, 2)
            #     return imgpre
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            abafador = cv2.imread("Abafador/vermelho.jpg", cv2.IMREAD_COLOR)


            
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
                # Reduz a saturação
                imagem_hsv[:, :, 1], mascara_pele // 255 * 90)

            imagem_final = cv2.cvtColor(
                imagem_hsv_reduzida, cv2.COLOR_HSV2BGR)  # Volta para BGR

            imagem = operador.copy()

            gray = cv2.cvtColor(operador, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            altura, largura, _ = imagem.shape
            mascara = np.zeros((altura, largura), dtype=np.uint8)

            for (x, y, w, h) in faces:

                # Coordenadas do segundo retângulo (preto)
                linha_sup = y + h // 4
                linha_inf = (y + h) * 3 // 4

                # Criar a máscara para o segundo retângulo
                cv2.rectangle(mascara, (int(x-(x/1.2)), linha_sup),
                              (int((x+w)*1.2), linha_inf), 255, -1)

            recorte_olhos = cv2.bitwise_and(
                imagem_final, imagem_final, mask=mascara)

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

            imgpre = cv2.Canny(img_recortada, 200, 1000)
            kernel = np.ones((5, 5))
            imgpre = cv2.dilate(imgpre, kernel, 2)
            imgpre = cv2.erode(imgpre, kernel, 2)

            # Aloca a chamada da função de tratamento da imagem à variável
            bordas = imgpre
            # bordas = self.pre_processamento(img_recortada)

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

            cv2.imshow(f"Imagem com Retângulos e Ponto", imagem)

            #     # Qualquer formato suportado pelo Pillow
            # self.img_path3 = "Abafador/003.jpg"
            # img_pil = Image.open(self.img_path3)  # Abre a imagem com Pillow
            # img_pil = img_pil.resize((350, 350))
            # self.img3 = ImageTk.PhotoImage(img_pil)
            # # Criação do Label para exibir a imagem dentro do plotframe
            # self.l_img3 = Label(self.plotframe, image=self.img3, bg="lightgray")
            # # Centralizar no frame
            # self.l_img3.place(row=1, column=0, padx=(20, 0),
            #                   pady=(20, 0), anchor="center")
            
            
             
            return resultado, imagem



    def selecionar_imagem(self):
        # Abrir diálogo e processar a imagem
        filepath = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")]
        )
        if filepath:
            resultado, imagem = self.analisar_imagem(filepath)
            self.atualizar_interface(resultado)
        
        # print(filepath)
        return filepath

    def atualizar_interface(self, resultado):
        # # Atualizar a textbox com o resultado
        # self.textboxGcode.delete("1.0", "end")  # Limpar a textbox
        # self.textboxGcode.insert("1.0", f"Resultado: {resultado}\n")

        if resultado == "LIVRE":
            cor = "green"
            texto = "ACESSO LIVRE"
        elif resultado == "BLOQUEADO":
            cor = "red"
            texto = "ACESSO NEGADO"
        else:
            cor = "white"
            texto = "RESULTADO INDEFINIDO"

    # Atualizar a cor do frame
        # self.plotframe.configure(fg_color=("black", cor))

    # Atualizar ou criar o texto no frame
        if not hasattr(self, "texto_plotframe"):  # Se o Label não existir, crie-o
            self.texto_plotframe = customtkinter.CTkLabel(
                self.plotframe, text=texto, font=customtkinter.CTkFont(
                    size=20, weight="bold")
            )
            self.texto_plotframe.pack(pady=10, padx=10)
        else:  # Se já existir, apenas atualize o texto
            self.texto_plotframe.configure(text=texto)

       
    


if __name__ == "__main__":
    app = App()
    app.mainloop()
