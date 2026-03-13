const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.getElementById("enterprise-form");
const enterpriseIdInput = document.getElementById("enterprise-id");
const submitButton = document.getElementById("submit-button");
const cancelButton = document.getElementById("cancel-button");
const refreshButton = document.getElementById("refresh-button");
const feedbackElement = document.getElementById("feedback");
const tableBody = document.getElementById("enterprise-table-body");
const tableCount = document.getElementById("table-count");

const fields = {
    business_name: document.getElementById("business_name"),
    owner_name: document.getElementById("owner_name"),
    city: document.getElementById("city"),
    segment: document.getElementById("segment"),
    contact: document.getElementById("contact"),
    status: document.getElementById("status"),
    description: document.getElementById("description"),
};

let enterprises = [];

form.addEventListener("submit", handleFormSubmit);
cancelButton.addEventListener("click", handleCancelEdit);
refreshButton.addEventListener("click", loadEnterprises);

document.addEventListener("DOMContentLoaded", () => {
    loadEnterprises();
});

async function loadEnterprises() {
    setTableLoadingState();

    try {
        const response = await fetch(`${API_BASE_URL}/enterprises`);
        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(formatApiMessage(result.message) || "Nao foi possivel carregar os empreendimentos.");
        }

        enterprises = Array.isArray(result.data) ? result.data : [];
        renderTable();
    } catch (error) {
        enterprises = [];
        renderTable();
        showFeedback(error.message || "Nao foi possivel carregar os empreendimentos.", "error");
    }
}

async function handleFormSubmit(event) {
    event.preventDefault();

    const payload = buildPayload();
    const enterpriseId = enterpriseIdInput.value;
    const isUpdate = Boolean(enterpriseId);
    const endpoint = isUpdate
        ? `${API_BASE_URL}/enterprises/${enterpriseId}`
        : `${API_BASE_URL}/enterprises`;
    const method = isUpdate ? "PUT" : "POST";

    try {
        const response = await fetch(endpoint, {
            method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });
        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(formatApiMessage(result.message) || "Nao foi possivel salvar o empreendimento.");
        }

        resetFormState();
        showFeedback(
            isUpdate
                ? "Empreendimento atualizado com sucesso."
                : "Empreendimento cadastrado com sucesso.",
            "success",
        );
        await loadEnterprises();
    } catch (error) {
        showFeedback(error.message || "Nao foi possivel salvar o empreendimento.", "error");
    }
}

async function handleDelete(enterpriseId) {
    const confirmed = window.confirm("Deseja excluir este empreendimento?");
    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/enterprises/${enterpriseId}`, {
            method: "DELETE",
        });
        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(formatApiMessage(result.message) || "Nao foi possivel excluir o empreendimento.");
        }

        if (enterpriseIdInput.value === enterpriseId) {
            resetFormState();
        }

        showFeedback("Empreendimento excluido com sucesso.", "success");
        await loadEnterprises();
    } catch (error) {
        showFeedback(error.message || "Nao foi possivel excluir o empreendimento.", "error");
    }
}

function handleEdit(enterpriseId) {
    const enterprise = enterprises.find((item) => item.id === enterpriseId);
    if (!enterprise) {
        showFeedback("Empreendimento nao encontrado na lista atual.", "error");
        return;
    }

    enterpriseIdInput.value = enterprise.id;
    fields.business_name.value = enterprise.business_name || "";
    fields.owner_name.value = enterprise.owner_name || "";
    fields.city.value = enterprise.city || "";
    fields.segment.value = enterprise.segment || "";
    fields.contact.value = enterprise.contact || "";
    fields.status.value = enterprise.status || "";
    fields.description.value = enterprise.description || "";

    submitButton.textContent = "Atualizar empreendimento";
    cancelButton.classList.remove("hidden");
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function handleCancelEdit() {
    resetFormState();
    hideFeedback();
}

function resetFormState() {
    form.reset();
    enterpriseIdInput.value = "";
    submitButton.textContent = "Cadastrar empreendimento";
    cancelButton.classList.add("hidden");
}

function buildPayload() {
    const payload = {
        business_name: fields.business_name.value.trim(),
        owner_name: fields.owner_name.value.trim(),
        city: fields.city.value.trim(),
        segment: fields.segment.value,
        contact: fields.contact.value.trim(),
        status: fields.status.value,
    };

    const description = fields.description.value.trim();
    if (description) {
        payload.description = description;
    }

    return payload;
}

function renderTable() {
    tableCount.textContent = `${enterprises.length} ${enterprises.length === 1 ? "item" : "itens"}`;

    if (!enterprises.length) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="8" class="empty-state">Nenhum empreendimento encontrado.</td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = enterprises
        .map((enterprise) => {
            const description = enterprise.description || "-";

            return `
                <tr>
                    <td>${escapeHtml(enterprise.business_name)}</td>
                    <td>${escapeHtml(enterprise.owner_name)}</td>
                    <td>${escapeHtml(enterprise.city)}</td>
                    <td>${escapeHtml(enterprise.segment)}</td>
                    <td>${escapeHtml(enterprise.contact)}</td>
                    <td>${escapeHtml(enterprise.status)}</td>
                    <td>${escapeHtml(description)}</td>
                    <td>
                        <div class="actions-cell">
                            <button type="button" data-action="edit" data-id="${enterprise.id}">Editar</button>
                            <button type="button" class="danger-button" data-action="delete" data-id="${enterprise.id}">Excluir</button>
                        </div>
                    </td>
                </tr>
            `;
        })
        .join("");

    bindTableActions();
}

function bindTableActions() {
    const actionButtons = tableBody.querySelectorAll("button[data-action]");

    actionButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const { action, id } = button.dataset;

            if (action === "edit") {
                handleEdit(id);
                return;
            }

            if (action === "delete") {
                handleDelete(id);
            }
        });
    });
}

function setTableLoadingState() {
    tableBody.innerHTML = `
        <tr>
            <td colspan="8" class="empty-state">Carregando empreendimentos...</td>
        </tr>
    `;
}

function showFeedback(message, type) {
    feedbackElement.textContent = message;
    feedbackElement.className = `feedback ${type}`;
}

function hideFeedback() {
    feedbackElement.textContent = "";
    feedbackElement.className = "feedback hidden";
}

function formatApiMessage(message) {
    const messages = {
        "Enterprise not found": "Empreendimento nao encontrado.",
        "Invalid enterprise id": "Identificador de empreendimento invalido.",
        "Field cannot be empty": "Preencha os campos obrigatorios.",
        "Segment cannot be empty": "Selecione um segmento.",
        "Status cannot be empty": "Selecione um status.",
        "Invalid segment": "Selecione um segmento valido.",
        "Invalid status": "Selecione um status valido.",
        "At least one field must be provided": "Informe pelo menos um campo para atualizar.",
    };

    return messages[message] || message;
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}
