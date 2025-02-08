import cv2
import os

# Diretório onde as imagens estão salvas
input_dir = 'fotos_predio_novo'

# Nome do arquivo de vídeo de saída
output_video = 'video-cotuca-novo.avi'

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
    video = cv2.VideoWriter(output_video, fourcc, 1.0, (width, height))

    # Adicionar cada imagem ao vídeo
    for image in images:
        image_path = os.path.join(input_dir, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    # Liberar o objeto VideoWriter
    video.release()

    print(f"Vídeo salvo como {output_video}.")