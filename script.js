const generateButton = document.getElementById("generate");
const promptInput = document.getElementById("prompt");
const durationInput = document.getElementById("duration");
const formatInput = document.getElementById("format");
const preview = document.getElementById("preview");
const status = document.getElementById("status");
const exportButton = document.getElementById("export");
let downloadUrl = null;

generateButton.addEventListener("click", async () => {
  const description = promptInput.value.trim();
  const duration = durationInput.value;
  const format = formatInput.value;

  if (!description) {
    status.textContent = "Por favor, descreva a animação desejada.";
    preview.innerHTML = "<p>Sua animação aparecerá aqui.</p>";
    exportButton.hidden = true;
    downloadUrl = null;
    promptInput.focus();
    return;
  }

  status.textContent = "Preparando sua animação...";
  preview.innerHTML = "<p>Processando e verificando o Blender...</p>";
  exportButton.hidden = true;
  downloadUrl = null;
  generateButton.disabled = true;

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        description,
        duration,
        format
      })
    });
    const result = await response.json();

    if (!response.ok) {
      preview.innerHTML = `<p>${escapeHTML(result.error || "Não foi possível gerar a animação.")}</p>`;
      status.textContent = "Geração não realizada.";
      return;
    }

    downloadUrl = result.downloadUrl;
    preview.innerHTML = `
      <video controls autoplay muted playsinline>
        <source src="${escapeHTML(downloadUrl)}" type="video/mp4">
      </video>
    `;
    status.textContent = "Animação renderizada com sucesso.";
    exportButton.hidden = false;
  } catch (error) {
    preview.innerHTML = "<p>Não foi possível conectar ao servidor local.</p>";
    status.textContent = "Execute a aplicação com o comando documentado no README.";
  } finally {
    generateButton.disabled = false;
  }
});

exportButton.addEventListener("click", () => {
  if (!downloadUrl) return;
  const link = document.createElement("a");
  link.href = downloadUrl;
  link.download = "simple3d-ai.mp4";
  document.body.appendChild(link);
  link.click();
  link.remove();
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
