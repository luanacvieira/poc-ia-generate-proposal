async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const response = await fetch("http://localhost:8000/upload/", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  document.getElementById("extractedText").value = data.text;
}

async function analyzeText() {
  const text = document.getElementById("extractedText").value;
  const prompt = document.getElementById("promptText").value;

  const formData = new FormData();
  formData.append("text", text);
  formData.append("prompt", prompt);

  const response = await fetch("http://localhost:8000/analyze/", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  document.getElementById("resultText").value = data.result;
}

async function loadHistory() {
  const response = await fetch("http://localhost:8000/history/");
  const history = await response.json();
  const historyDiv = document.getElementById("historyDiv");
  if (!historyDiv) return;
  if (history.length === 0) {
    historyDiv.innerHTML = "<em>Nenhum histórico encontrado.</em>";
    return;
  }
  let html = '<table><tr><th>Arquivo</th><th>Data/Hora</th><th>Prévia do texto</th></tr>';
  history.reverse().forEach(item => {
    html += `<tr><td>${item.filename}</td><td>${new Date(item.timestamp).toLocaleString()}</td><td>${item.text_preview || ''}</td></tr>`;
  });
  html += '</table>';
  historyDiv.innerHTML = html;
}
