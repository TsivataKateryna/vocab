import random

def shuffle_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

def generate_html_quiz(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Prepare HTML content
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Language Quiz</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            max-width: 800px;
            margin: auto;
            background-color: #f9f9f9;
        }
        h1 {
            text-align: center;
        }
        .question {
            margin-bottom: 20px;
        }
        .question label {
            display: block;
            margin-bottom: 5px;
        }
        .question input {
            display: block;
            margin-bottom: 5px;
        }
        .correct {
            color: green;
            font-weight: bold;
        }
        .incorrect {
            color: red;
            font-weight: bold;
        }
        .hint {
            color: blue;
            cursor: pointer;
        }
        button {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            text-align: center;
            font-size: 1.2em;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Language Quiz</h1>
    <form id="quizForm">
'''

    # Initialize answer dictionary for JavaScript
    js_answers = "var answers = {"
    js_shuffled_hints = "var shuffled_hints = {"
    
    # Process each line and add to HTML
    for i, line in enumerate(lines):
        question, answer = line.strip().split(':')
        shuffled_hint = shuffle_word(answer.strip())  # Shuffle the letters of the correct answer
        html_content += f'''
        <div class="question">
            <label>What is the Dutch word for "{question.strip()}"?</label>
            <input type="text" name="q{i+1}">
            <span id="feedback{i+1}"></span>
            <button type="button" class="hint" onclick="showHint({i+1})">Show Hint</button>
            <span id="hint{i+1}" style="display:none;" class="hint">Hint: {shuffled_hint}</span>
        </div>
'''
        js_answers += f'\nq{i+1}: "{answer.strip()}",'
        js_shuffled_hints += f'\nq{i+1}: "{shuffled_hint}",'

    # Finalize the HTML and JS content
    js_answers = js_answers.rstrip(',') + "\n};"
    js_shuffled_hints = js_shuffled_hints.rstrip(',') + "\n};"

    html_content += '''
        <button type="button" onclick="checkAnswers()">Submit</button>
    </form>
    <div id="result" class="result"></div>

    <script>
        ''' + js_answers + '''
        ''' + js_shuffled_hints + '''

        var score = 0;
        var total = ''' + str(len(lines)) + ''';  // Total number of questions

        function checkAnswers() {
            score = 0;

            // Get the form inputs
            var form = document.forms["quizForm"];

            // Check each answer
            for (var i = 1; i <= total; i++) {
                var userAnswer = form["q" + i].value.trim();
                var feedbackElem = document.getElementById("feedback" + i);
                var hintElem = document.getElementById("hint" + i);

                if (userAnswer.toLowerCase() === answers["q" + i].toLowerCase()) {
                    score++;
                    feedbackElem.textContent = "Correct!";
                    feedbackElem.className = "correct";
                } else {
                    feedbackElem.textContent = "Incorrect!";
                    feedbackElem.className = "incorrect";
                }

                // Hide hint after checking
                hintElem.style.display = "none";
            }

            // Display the result
            var result = document.getElementById("result");
            result.innerHTML = "You scored " + score + " out of " + total + ".";
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