import random

def shuffle_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

def generate_html_quiz(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Prepare the HTML content
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Language Quiz</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            max-width: 800px;
            margin: auto;
            background-color: #f9f9f9;
        }}
        h1 {{
            text-align: center;
        }}
        .question {{
            margin-bottom: 20px;
        }}
        .question label {{
            display: block;
            margin-bottom: 5px;
        }}
        .question input {{
            display: block;
            margin-bottom: 5px;
        }}
        .correct {{
            color: green;
            font-weight: bold;
        }}
        .incorrect {{
            color: red;
            font-weight: bold;
        }}
        .hint {{
            color: blue;
            cursor: pointer;
        }}
        button {{
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        .result {{
            text-align: center;
            font-size: 1.2em;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>Language Quiz</h1>
    <label for="num_words">Nombre de mots dans le quiz (max {0}):</label>
    <input type="number" id="num_words" name="num_words" value="10" min="1" max="{0}">
    <button type="button" onclick="startQuiz()">Commencer le quiz</button>
    <form id="quizForm" style="display:none;">
'''.format(len(lines))

    # Initialize answer dictionary for JavaScript
    js_answers = "var answers = {"
    
    # Process each line and add to HTML
    for i, line in enumerate(lines):
        try:
            question, answer = line.strip().split(':')
        except ValueError:
            print(line)
        shuffled_hint = shuffle_word(answer.strip())  # Shuffle the letters of the correct answer
        html_content += f'''
        <div class="question">
            <label>Quel est le mot néerlandais pour "{question.strip()}" ?</label>
            <input type="text" name="q{i+1}">
            <span id="feedback{i+1}"></span>
            <button type="button" class="hint" onclick="showHint({i+1})">Afficher l'indice</button>
            <span id="hint{i+1}" style="display:none;" class="hint">Indice : {shuffled_hint}</span>
        </div>
'''
        js_answers += f'\nq{i+1}: "{answer.strip()}",'

    # Finalize HTML and JS content
    js_answers = js_answers.rstrip(',') + "\n};"

    html_content += '''
        <button type="button" onclick="checkAnswers()">Soumettre</button>
    </form>
    <div id="result" class="result"></div>

    <script>
        ''' + js_answers + '''

        var score = 0;
        var total = ''' + str(len(lines)) + ''';  // Nombre total de questions

        function startQuiz() {
            // Get the number of words specified by the user
            var numWords = document.getElementById("num_words").value;
            numWords = Math.min(numWords, ''' + str(len(lines)) + ''');
            numWords = Math.max(numWords, 1);

            // Select a random subset of questions
            var form = document.getElementById("quizForm");
            form.style.display = "block";
            var questions = document.querySelectorAll(".question");
            var selectedQuestions = [];
            while (selectedQuestions.length < numWords) {
                var randomIndex = Math.floor(Math.random() * total);
                if (!selectedQuestions.includes(randomIndex)) {
                    selectedQuestions.push(randomIndex);
                }
            }

            // Show only the selected questions
            for (var i = 0; i < total; i++) {
                if (selectedQuestions.includes(i)) {
                    questions[i].style.display = "block";
                } else {
                    questions[i].style.display = "none";
                }
            }
        }

        function checkAnswers() {
            score = 0;

            // Get form inputs
            var form = document.forms["quizForm"];
            var displayedQuestions = document.querySelectorAll(".question");
            var numQuestionsDisplayed = 0;

            // Check each visible answer
            for (var i = 0; i < displayedQuestions.length; i++) {
                if (displayedQuestions[i].style.display !== "none") {
                    numQuestionsDisplayed++;
                    var userAnswer = form["q" + (i + 1)].value.trim();
                    var feedbackElem = document.getElementById("feedback" + (i + 1));
                    var hintElem = document.getElementById("hint" + (i + 1));

                    if (userAnswer.toLowerCase() === answers["q" + (i + 1)].toLowerCase()) {
                        score++;
                        feedbackElem.textContent = "Correct !";
                        feedbackElem.className = "correct";
                    } else {
                        feedbackElem.textContent = "Incorrect !";
                        feedbackElem.className = "incorrect";
                    }

                    // Hide hint after checking
                    hintElem.style.display = "none";
                }
            }

            // Display result
            var result = document.getElementById("result");
            result.innerHTML = "Vous avez obtenu " + score + " sur " + numQuestionsDisplayed + ".";
        }

        function showHint(questionNumber) {
            var hintElem = document.getElementById("hint" + questionNumber);
            hintElem.style.display = "inline";

            // Deduct 0.5 points for using the hint
            score -= 0.5;
        }
    </script>
</body>
</html>
'''

    # Write the HTML content to the output file
    with open(output_file, 'w') as output_file:
        output_file.write(html_content)
    print(f"Quiz HTML generated: {output_file.name}")

# Generate the quiz HTML
generate_html_quiz('quiz.txt', 'index.html')