import { generateMultipleExercises } from './ollama.js';

function hideWordInSentence(sentence, word) {
  const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`\\b${escaped}\\b`, 'gi');
  return sentence.replace(regex, '___');
}

function shuffleWord(word) {
  const letters = word.split('');
  for (let i = letters.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [letters[i], letters[j]] = [letters[j], letters[i]];
  }
  return letters.join('');
}

function createExerciseElement(exercise, index) {
  const [word, translation, french, english] = exercise;
  const container = document.createElement('div');
  container.className = 'exercise-block';
  container.innerHTML = `
    <p><strong>${index + 1}.</strong> ${french}</p>
    <p>${hideWordInSentence(english, translation)}</p>
    <input type="text" data-answer="${translation.toLowerCase()}" data-word="${word}" />
    <span class="result"></span>
    <br><br>
  `;
  return container;
}

function checkAllAnswers() {
  const inputs = document.querySelectorAll('input[type="text"]');
  let correctCount = 0;

  inputs.forEach(input => {
    const userAnswer = input.value.trim().toLowerCase();
    const correctAnswer = input.dataset.answer;
    const resultSpan = input.nextElementSibling;

    if (userAnswer === correctAnswer) {
      resultSpan.textContent = '✔';
      resultSpan.style.color = 'green';
      correctCount++;
    } else {
      const scrambled = shuffleWord(correctAnswer);
      const wordHint = input.dataset.word;
      resultSpan.textContent = `✖ Hint: ${wordHint} → ${scrambled}`;
      resultSpan.style.color = 'red';
    }
  });

  const summary = document.getElementById('summary');
  summary.textContent = `Résultat : ${correctCount} / ${inputs.length} corrects.`;
}

(async function init() {
  const exercises = await generateMultipleExercises(10);
  const container = document.getElementById('exercise-container');

  exercises.forEach((ex, idx) => {
    container.appendChild(createExerciseElement(ex, idx));
  });

  const button = document.createElement('button');
  button.textContent = 'Valider';
  button.addEventListener('click', checkAllAnswers);
  container.appendChild(button);

  const summary = document.createElement('p');
  summary.id = 'summary';
  container.appendChild(summary);
})();
