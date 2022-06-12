import os

def save_to_file(output_path, filename, content):
  os.makedirs(output_path, exist_ok=True)
  with open(f'{output_path}/{filename}', 'w') as f:
    f.write(content)
