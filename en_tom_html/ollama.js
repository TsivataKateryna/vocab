import { queryLlama } from './api.js';

let wordsList = [];

export async function loadWords() {
  try {
    const response = await fetch('../database/words.txt');

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const text = await response.text();
    wordsList = text
      .trim()
      .split('\n')
      .map(line => {
        const [left, right] = line.split('#');
        const word = left
          ? left.split(',')[0].trim().replace(',', '').replace('(', '').replace(')', '')
          : '';
        const translation = right ? right.trim() : '';
        return { word, translation };
      })
      .filter(({ word }) => word.length > 0);
  } catch (e) {
    console.error('Error loading words:', e);
    wordsList = [];
  }
}

function getRandomWord(excludeSet = new Set()) {
  const availableWords = wordsList.filter(({ word }) => !excludeSet.has(word));
  if (availableWords.length === 0) throw new Error('No more unique words available.');
  const idx = Math.floor(Math.random() * availableWords.length);
  return availableWords[idx];
}

export async function generateLanguageExercise(excludeSet = new Set()) {
  if (wordsList.length === 0) {
    await loadWords();
  }

  const { word, translation } = getRandomWord(excludeSet);

  const prompt = `You are a language teaching assistant.

Generate a unique exercise using the word "${word}" in a short and simple French sentence AND its English translation.

Output exactly one JSON object with these keys:
- f (string): a short French sentence containing the word "${word}".
- e (string): English translation of the french sentence.

Rules:
- f must be in French and contain the word "${word}".
- e must be in English and correspond exactly to the French sentence.
- Return ONLY the JSON object, no extra text, no explanations.
`;

  let raw = await queryLlama(prompt);
  console.log('Raw response:', raw);

  const start = raw.indexOf('{');
  const end = raw.lastIndexOf('}');
  if (start === -1 || end === -1) {
    throw new Error('No JSON found in model response');
  }

  let exercise;
  try {
    const jsonString = raw.substring(start, end + 1);
    exercise = JSON.parse(jsonString);
  } catch (e) {
    console.error('Failed to parse JSON:', raw);
    throw e;
  }

  return [word, translation, exercise.f, exercise.e];
}

export async function generateMultipleExercises(n) {
  const results = [];
  const usedWords = new Set();

  for (let i = 0; i < n; i++) {
    let attempts = 0;
    while (attempts < 10) {
      try {
        const ex = await generateLanguageExercise(usedWords);
        const word = ex[0];
        if (!usedWords.has(word)) {
          usedWords.add(word);
          results.push(ex);
          break;
        } else {
          attempts++;
        }
      } catch (e) {
        console.warn(`Exercise ${i + 1} failed:`, e.message);
        break;
      }
    }
    if (attempts === 10) {
      console.warn(`Could not generate unique exercise for index ${i + 1}`);
      continue;
    }
  }

  return results;
}
