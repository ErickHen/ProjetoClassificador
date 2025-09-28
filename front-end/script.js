async function processEmail() {
  const fileInput = document.getElementById("fileInput");
  const textArea = document.getElementById("emailText");
  const resultsBox = document.getElementById("resultsBox");
  const categoryEl = document.getElementById("category");
  const answerEl = document.getElementById("answer");

  const formData = new FormData();
  if (fileInput.files.length > 0) {
    formData.append("file", fileInput.files[0]);
  }
  formData.append("text", textArea.value);

  // ✅ limpa imediatamente após capturar os dados
  fileInput.value = "";
  textArea.value = "";

  categoryEl.innerText = "Processando...";
  answerEl.innerText = "";
  resultsBox.style.display = "block";

  try {
    const resp = await fetch("http://localhost:5000/api/process", { 
      method: "POST", 
      body: formData 
    });

    const data = await resp.json();
    if (resp.ok) {
      categoryEl.innerText = "Categoria: " + data.category;
      answerEl.innerText = "Resposta sugerida: " + data.suggested_answer;
    } else {
      categoryEl.innerText = "Erro: " + data.error;
    }
  } catch (err) {
    categoryEl.innerText = "Erro de conexão com o servidor.";
    answerEl.innerText = err.message;
  }
}
