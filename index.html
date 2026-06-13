const API_URL = window.location.protocol.startsWith("http") ? window.location.origin : "http://127.0.0.1:5000";

const studentCode = document.querySelector("#studentCode");
const highlightedCode = document.querySelector("#highlightedCode");
const similarityScore = document.querySelector("#similarityScore");
const matchCount = document.querySelector("#matchCount");
const referenceCount = document.querySelector("#referenceCount");
const matchesList = document.querySelector("#matchesList");
const referenceList = document.querySelector("#referenceList");
const referenceForm = document.querySelector("#referenceForm");
const chunkSize = document.querySelector("#chunkSize");

const sampleSubmission = `def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9], 7))`;

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}

function renderHighlightedCode(segments) {
  if (!segments || segments.length === 0) {
    highlightedCode.innerHTML = '<span class="placeholder">No submitted code to highlight.</span>';
    return;
  }

  highlightedCode.innerHTML = segments
    .map((segment) => `<span class="${segment.copied ? "copied" : "original"}">${escapeHtml(segment.text)}</span>`)
    .join("");
}

function renderMatches(matches) {
  if (!matches || matches.length === 0) {
    matchesList.className = "matches-list empty-state";
    matchesList.textContent = "No copied fragments found.";
    return;
  }

  matchesList.className = "matches-list";
  matchesList.innerHTML = matches.slice(0, 25).map((match) => `
    <div class="match-item">
      <div class="item-heading">
        <strong>${escapeHtml(match.reference_filename)}</strong>
        <span class="badge">${escapeHtml(match.reference_language)}</span>
      </div>
      <small>Student chars ${match.submitted_start}-${match.submitted_end}, reference chars ${match.reference_start}-${match.reference_end}</small>
      <pre>${escapeHtml(match.snippet)}</pre>
    </div>
  `).join("");
}

async function loadReferences() {
  const references = await request("/api/references");
  referenceCount.textContent = references.length;
  referenceList.innerHTML = references.map((reference) => `
    <div class="reference-item">
      <div class="item-heading">
        <div>
          <strong>${escapeHtml(reference.filename)}</strong>
          <span class="badge">${escapeHtml(reference.language)}</span>
        </div>
        <button class="delete-button" data-id="${reference.id}" type="button">Delete</button>
      </div>
      <small>${reference.characters} characters</small>
      <pre>${escapeHtml(reference.code)}</pre>
    </div>
  `).join("");
}

async function runCheck() {
  try {
    const result = await request("/api/check", {
      method: "POST",
      body: JSON.stringify({ student_code: studentCode.value, chunk_size: Number(chunkSize.value) }),
    });

    similarityScore.textContent = `${result.similarity_percentage}%`;
    matchCount.textContent = result.matches_found;
    referenceCount.textContent = result.references_checked;
    renderHighlightedCode(result.highlighted_segments);
    renderMatches(result.matches);
  } catch (error) {
    alert(error.message);
  }
}

document.querySelector("#checkBtn").addEventListener("click", runCheck);
document.querySelector("#sampleBtn").addEventListener("click", () => {
  studentCode.value = sampleSubmission;
  runCheck();
});

referenceForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const filename = document.querySelector("#filename").value || "reference.txt";
  const language = document.querySelector("#language").value;
  const code = document.querySelector("#referenceCode").value;

  try {
    await request("/api/references", {
      method: "POST",
      body: JSON.stringify({ filename, language, code }),
    });
    referenceForm.reset();
    await loadReferences();
  } catch (error) {
    alert(error.message);
  }
});

referenceList.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-id]");
  if (!button) return;
  await request(`/api/references/${button.dataset.id}`, { method: "DELETE" });
  await loadReferences();
});

loadReferences().catch((error) => {
  referenceList.textContent = `Could not load references: ${error.message}`;
});
