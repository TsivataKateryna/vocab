import os
import argparse

def generate_toc(directories, output_file):
    toc_lines = []
    
    toc_lines.append('<!DOCTYPE html>')
    toc_lines.append('<html lang="fr">')
    toc_lines.append('<head>')
    toc_lines.append('<meta charset="UTF-8">')
    toc_lines.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    toc_lines.append('<title>Table des Matières</title>')
    toc_lines.append('</head>')
    toc_lines.append('<body>')
    toc_lines.append('<h1>Table des Matières</h1>')
    toc_lines.append('<ul>')
    
    for directory in directories:
        for root, _, files in os.walk(directory):
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * level
            toc_lines.append(f'{indent}<li>{os.path.basename(root)}</li>')
            toc_lines.append(f'{indent}<ul>')
            
            for file in sorted(files):
                if file.endswith('.html'):
                    filepath = os.path.join(root, file)
                    relative_path = os.path.relpath(filepath, start=directories[0])
                    #print(relative_path)
                    print(filepath)
                    toc_lines.append(f'{indent}    <li><a href="{filepath}">{file}</a></li>')
            
            toc_lines.append(f'{indent}</ul>')
    
    toc_lines.append('</ul>')
    toc_lines.append('</body>')
    toc_lines.append('</html>')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(toc_lines))
    
    print(f"Table des matières générée dans {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Génère une table des matières à partir de fichiers HTML dans une séquence de répertoires.')
    parser.add_argument('directories', nargs='+', help='Une séquence de répertoires à parcourir.')
    parser.add_argument('output_file', type=str, help='Le fichier HTML de sortie pour la table des matières.')
    
    args = parser.parse_args()
    
    generate_toc(args.directories, args.output_file)

if __name__ == '__main__':
    main()