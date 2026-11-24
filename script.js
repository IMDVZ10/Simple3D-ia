const generateButton = document.getElementById("generate");
const promptInput = document.getElementById("prompt");
const durationInput = document.getElementById("duration");
const formatInput = document.getElementById("format");
const preview = document.getElementById("preview");
const status = document.getElementById("status");

generateButton.addEventListener("click", () => {
  const description = promptInput.value.trim();
  const duration = durationInput.value;
  const format = formatInput.value;

  if (!description) {
    status.textContent = "Por favor, descreva a animação desejada.";
    promptInput.focus();
    return;
  }

  status.textContent = "Preparando sua animação...";

  preview.innerHTML = `     <div>       <h3>Projeto preparado!</h3>       <p>${escapeHTML(description)}</p>       <p>Duração: ${duration} segundos</p>       <p>Formato: ${format}</p>       <p>Motor 3D: aguardando implementação.</p>     </div>   `;

  status.textContent =
    "Descrição recebida! A geração de vídeo será implementada na próxima etapa.";
});

function escapeHTML(text) {
  return text.replace(/[&<>\"']/g, (character) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "'"
    };

    return entities[character];
  });
}
