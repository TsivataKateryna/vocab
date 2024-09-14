import random
import re
import argparse
import html

# Liste des mots trop faciles que l'on ne veut pas masquer
easy_words = ["is", "I", "a", "if", "the", "in", "on", "at", "of", "and","m",".","'","?","!",":",'to','you','You',',','not','To','A','s','d']

def read_expressions(input_file):
    """Read expressions from the input file."""
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    expressions = [line.split(' # ') for line in lines]
    return expressions


def split_sentence(sentence):
    """Split a sentence into words, keeping the punctuation as separate tokens."""
    #return re.findall(r"\w+|[.,!?;]", sentence)
    return re.findall(r"\w+(?:'\w+)?|[.,!?;]", sentence)

def generate_quiz_html(expressions, output_file):
    """Generate HTML for the quiz."""
    html_lines = []

    html_lines.append('<!DOCTYPE html>')
    html_lines.append('<html lang="fr">')
    html_lines.append('<head>')
    html_lines.append('<meta charset="UTF-8">')
    html_lines.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_lines.append('<title>Quiz de Traduction</title>')
    html_lines.append('<style>')
    html_lines.append('body { font-family: Arial, sans-serif; margin: 20px; }')
    html_lines.append('h1 { font-size: 24px; }')
    html_lines.append('p { font-size: 18px; }')
    html_lines.append('input[type="text"] { font-size: 16px; padding: 5px; }')
    html_lines.append('button { font-size: 16px; padding: 5px 10px; margin-left: 5px; }')
    html_lines.append('</style>')
    html_lines.append('</head>')
    html_lines.append('<body>')
    html_lines.append('<h1>Quiz de Traduction</h1>')
    html_lines.append('<form id="quizForm">')

    correct_words = []

    for i, (french, english) in enumerate(expressions):
        words = split_sentence(english)
        #print(words)
        
        # Filtrer les mots interdits (trop faciles)
        possible_words = [word for word in words if word not in easy_words]

        #print("possible_words",possible_words)
        
        # Sélectionner un mot à masquer parmi les mots valides
        if possible_words:
            missing_word = random.choice(possible_words)
        else:
            missing_word = random.choice(words)

        #print("missing word:",missing_word)
        
        correct_words.append(missing_word)
        
        # Remplacer le mot manquant par une ligne
        words = ['____' if word == missing_word else word for word in words]
        missing_word_shuffled = ''.join(random.sample(missing_word, len(missing_word)))
        #escaped_missing_word_shuffled = html.escape(missing_word_shuffled)
        escaped_missing_word_shuffled = missing_word_shuffled.replace("'", "\\'")

        #print(missing_word)

        html_lines.append('<br>')
        html_lines.append(f'<p>{french}</p>')
        html_lines.append(f'<p>{" ".join(words)}</p>')
        html_lines.append(f'<input type="text" id="answer_{i}" name="answer_{i}" />')
        html_lines.append(f'<button type="button" onclick="showHint({i}, \'{escaped_missing_word_shuffled}\')">Aide</button>')
        html_lines.append(f'<button type="button" onclick="showAnswer({i}, \'{missing_word}\')">Reponse</button>')
        # Display the hint without escaping (for readability)
        html_lines.append(f'<p id="hint_{i}" style="display:none;">Indice: {missing_word_shuffled}</p>')
        html_lines.append(f'<p id="hint2_{i}" style="display:none;">Reponse: {missing_word}</p>')
        print("==>",missing_word)
        print("==>",missing_word_shuffled)
        html_lines.append(f'<p id="result_{i}"></p>')

    html_lines.append('</form>')
    html_lines.append('<p><button type="button" onclick="correctAnswers()">Corrige</button></p>')
    html_lines.append('<p id="score"></p>')

    html_lines.append('<script>')
    html_lines.append('function correctAnswers() {')
    html_lines.append('    let score = 0;')
    html_lines.append(f'    const correctWords = {correct_words};')
    html_lines.append('    const totalQuestions = correctWords.length;')
    
    for i in range(len(expressions)):
        html_lines.append(f'    const userAnswer_{i} = document.getElementById("answer_{i}").value.trim();')
        html_lines.append(f'    const correctWord_{i} = correctWords[{i}];')
        html_lines.append(f'    const resultElement_{i} = document.getElementById("result_{i}");')
        html_lines.append(f'    if (userAnswer_{i}.toLowerCase() === correctWord_{i}.toLowerCase()) {{')
        html_lines.append(f'        resultElement_{i}.textContent = "Correct!";')
        html_lines.append(f'        resultElement_{i}.style.color = "green";')
        html_lines.append(f'        score += 1;')
        html_lines.append('    } else {')
        html_lines.append(f'        resultElement_{i}.textContent = "Incorrect, la bonne réponse était: " + correctWord_{i};')
        html_lines.append(f'        resultElement_{i}.style.color = "red";')
        html_lines.append('    }')
    
    html_lines.append('    document.getElementById("score").textContent = "Votre score: " + score + " / " + totalQuestions;')
    html_lines.append('}')

    html_lines.append('function showHint(index, hint) {')
    html_lines.append('    const hintElement = document.getElementById("hint_" + index);')
    html_lines.append('    hintElement.style.display = "block";')
    html_lines.append('}')

    html_lines.append('function showAnswer(index, answer) {')
    html_lines.append('    const answerElement = document.getElementById("hint2_" + index);')
    html_lines.append('    answerElement.style.display = "block";')
    html_lines.append('}')
    
    html_lines.append('</script>')
    html_lines.append('</body>')
    html_lines.append('</html>')

    with open(output_file, 'w') as file:
        file.write('\n'.join(html_lines))
    
    print(f"Quiz généré dans {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Génère un quiz HTML à partir d\'expressions en français et leur traduction en anglais.')
    parser.add_argument('input_file', type=str, help='Fichier texte contenant les expressions et traductions.')
    parser.add_argument('output_file', type=str, help='Fichier HTML de sortie pour le quiz.')

    args = parser.parse_args()

    expressions = read_expressions(args.input_file)
    generate_quiz_html(expressions, args.output_file)

if __name__ == '__main__':
    main()