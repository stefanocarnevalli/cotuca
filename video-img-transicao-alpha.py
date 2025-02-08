#script - seleciona imagens, corta com base na primeira, cria um video com trasições fade alpha
# CC autor: stefanocarnevalli
# contribuições:

import cv2
import os
import numpy as np

# Diretório onde as imagens estão salvas
input_dir = 'fotos_predio_novo'

# Nome do arquivo de vídeo de saída
output_video = 'video_com_transicoes-alpha.avi'

# Obter a lista de arquivos de imagem no diretório
images = [img for img in os.listdir(input_dir) if img.endswith(".jpg")]

# Ordenar as imagens pelo nome do arquivo
images.sort()

# Verificar se há imagens no diretório
if not images:
    print("Nenhuma imagem encontrada no diretório.")
else:
    # Obter o caminho completo da primeira imagem para obter as dimensões
    first_image_path = os.path.join(input_dir, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Definir o codec e criar o objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 1  # Definindo 1 frame por segundo
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Função para criar uma transição de fade entre duas imagens
    def add_fade_transition(img1, img2, steps=2):
        for i in range(steps):
            alpha = i / float(steps)
            beta = 1.0 - alpha
            transition_frame = cv2.addWeighted(img1, beta, img2, alpha, 0)
            video.write(transition_frame)

    # Função para ajustar o tamanho da imagem mantendo proporções e cortando se necessário
    def adjust_image_size(image, target_width, target_height):
        h, w, _ = image.shape
        
        # Calcular a proporção de redimensionamento
        scale = max(target_width / w, target_height / h)
        
        # Redimensionar a imagem mantendo a proporção
        resized_image = cv2.resize(image, (int(w * scale), int(h * scale)))
        
        # Cortar a imagem para o tamanho alvo
        start_x = (resized_image.shape[1] - target_width) // 2
        start_y = (resized_image.shape[0] - target_height) // 2
        cropped_image = resized_image[start_y:start_y + target_height, start_x:start_x + target_width]
        
        return cropped_image

    # Adicionar cada imagem ao vídeo com transições
    print("Imagens utilizadas no vídeo:")
    for i in range(len(images) - 1):
        image_path = os.path.join(input_dir, images[i])
        next_image_path = os.path.join(input_dir, images[i + 1])
        
        frame = cv2.imread(image_path)
        next_frame = cv2.imread(next_image_path)
        
        # Ajustar o tamanho das imagens para ter as mesmas dimensões
        adjusted_frame = adjust_image_size(frame, width, height)
        adjusted_next_frame = adjust_image_size(next_frame, width, height)
        
        video.write(adjusted_frame)
        add_fade_transition(adjusted_frame, adjusted_next_frame)
        print(images[i])

    # Adicionar a última imagem sem transição
    last_image_path = os.path.join(input_dir, images[-1])
    last_frame = cv2.imread(last_image_path)
    adjusted_last_frame = adjust_image_size(last_frame, width, height)
    video.write(adjusted_last_frame)
    print(images[-1])

    # Liberar o objeto VideoWriter
    video.release()

    print(f"Vídeo salvo como {output_video}.")