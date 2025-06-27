let questionsData = [];  // les questions seront chargées ici

// Fonction pour charger les questions depuis un fichier JSON
async function loadQuestions() {
  try {
    const response = await fetch('questions.json');
    if (!response.ok) throw new Error("Erreur lors du chargement du fichier");
    questionsData = await response.json();
  } catch (error) {
    alert("Impossible de charger les questions : " + error);
  }
}

// Fonction pour démarrer le quiz avec N questions
function startQuiz(numWords) {
  const form = document.getElementById('quizForm');
  form.innerHTML = '';

  const shuffled = questionsData.sort(() => 0.5 - Math.random());
  const selected = shuffled.slice(0, numWords);

  selected.forEach(q => {
    const div = document.createElement('div');
    div.className = 'question';

    const label = document.createElement('label');
    label.textContent = q.question;
    div.appendChild(label);

    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'q' + q.id;
    div.appendChild(input);

    const feedback = document.createElement('span');
    feedback.id = 'feedback' + q.id;
    div.appendChild(feedback);

    const hintBtn = document.createElement('button');
    hintBtn.type = 'button';
    hintBtn.className = 'hint';
    hintBtn.textContent = "Afficher l'indice";
    hintBtn.onclick = () => showHint(q.id);
    div.appendChild(hintBtn);

    const hintSpan = document.createElement('span');
    hintSpan.id = 'hint' + q.id;
    hintSpan.style.display = 'none';
    hintSpan.className = 'hint';
    hintSpan.textContent = 'Indice : ' + q.hint;
    div.appendChild(hintSpan);

    form.appendChild(div);
  });

  const submitBtn = document.createElement('button');
  submitBtn.type = 'button';
  submitBtn.textContent = 'Soumettre';
  submitBtn.onclick = checkAnswers;
  form.appendChild(submitBtn);

  form.style.display = 'block';

  document.getElementById('result').textContent = '';
}

// Vérification des réponses
function checkAnswers() {
  let score = 0;
  const form = document.getElementById('quizForm');

  questionsData.forEach(q => {
    const input = form.querySelector(`input[name="q${q.id}"]`);
    if (!input) return;

    const feedbackElem = document.getElementById('feedback' + q.id);
    const hintElem = document.getElementById('hint' + q.id);
    const userAnswer = input.value.trim().toLowerCase();

    if (userAnswer === q.answer.toLowerCase()) {
      score++;
      feedbackElem.textContent = 'Correct !';
      feedbackElem.className = 'correct';
    } else {
      feedbackElem.textContent = 'Incorrect !';
      feedbackElem.className = 'incorrect';
    }

    hintElem.style.display = 'none';
  });

  const total = form.querySelectorAll('.question').length;
  document.getElementById('result').textContent = `Vous avez obtenu ${score} sur ${total}.`;
}

// Afficher l'indice
function showHint(id) {
  const hintElem = document.getElementById('hint' + id);
  if (hintElem) hintElem.style.display = 'inline';
}

// Gestionnaire de l'événement pour démarrer le quiz
document.getElementById('startQuizBtn').addEventListener('click', async () => {
  let num = parseInt(document.getElementById('num_words').value);
  if (isNaN(num) || num < 1) num = 1;
  if (num > questionsData.length) num = questionsData.length;

  await loadQuestions();
  startQuiz(num);
});
