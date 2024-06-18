import os
from tqdm import tqdm
from PIL import Image, ImageOps

# Definir directorios de origen y destino
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, '.')
output_dir = os.path.join(base_dir, 'processed_data')
categories = ['Covid', 'Normal', 'Pneumonia']
target_size = (256, 256)

# Crear directorios de salida
for category in categories:
    os.makedirs(os.path.join(output_dir, category), exist_ok=True)

def preprocess_and_save_images(source_dir, category, target_size):
    dest_path = os.path.join(output_dir, category)
    
    if not os.path.exists(source_dir):
        print(f"El directorio {source_dir} no existe. Saltando.")
        return
    
    for img_name in tqdm(os.listdir(source_dir)):
        try:
            img_path = os.path.join(source_dir, img_name)
            img = Image.open(img_path).convert('RGB')
            
            # Redimensionar y recortar la imagen manteniendo la relación de aspecto
            img = ImageOps.fit(img, target_size)
            
            img.save(os.path.join(dest_path, img_name))
        except Exception as e:
            print(f"Error procesando {img_path}: {e}")

def process_dataset(dataset_dir, target_size):
    for category in tqdm(categories, desc=f"Procesando {dataset_dir}"):
        # Procesar imágenes de train si existen
        train_dir = os.path.join(dataset_dir, 'train', category)
        if os.path.exists(train_dir):
            preprocess_and_save_images(train_dir, category, target_size)
        else:
            print(f"El directorio {train_dir} no existe. Saltando.")

        # Procesar imágenes de test si existen
        test_dir = os.path.join(dataset_dir, 'test', category)
        if os.path.exists(test_dir):
            preprocess_and_save_images(test_dir, category, target_size)
        else:
            print(f"El directorio {test_dir} no existe. Saltando.")

# Procesar todos los datasets
for dataset in ['dataset1', 'dataset2', 'dataset3']:
    dataset_dir = os.path.join(data_dir, dataset)
    process_dataset(dataset_dir, target_size)

print("Preprocesamiento completado.")
