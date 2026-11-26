(function () {
    let filmAuthorCount = 0;

    function showFilmCsvErrors(messages) {
        const container = document.getElementById("film_csv_errors");
        if (!container) return;

        container.innerHTML = "";
        const title = document.createElement("strong");
        title.textContent = "CSV validation error:";
        container.appendChild(title);

        const list = document.createElement("ul");
        list.className = "mb-0 mt-1";
        messages.forEach((msg) => {
            const li = document.createElement("li");
            li.textContent = String(msg);
            list.appendChild(li);
        });
        container.appendChild(list);
        container.style.display = "block";
    }

    function clearFilmCsvErrors() {
        const container = document.getElementById("film_csv_errors");
        if (!container) return;
        container.innerHTML = "";
        container.style.display = "none";
    }

    function showFilmUploadError(message) {
        const errorBox = document.getElementById("film_upload_error");
        if (!errorBox) return;
        errorBox.textContent = typeof message === "string" ? message : JSON.stringify(message);
        errorBox.style.display = "block";
    }

    function clearFilmUploadError() {
        const errorBox = document.getElementById("film_upload_error");
        if (!errorBox) return;
        errorBox.textContent = "";
        errorBox.style.display = "none";
    }

    function renderCsvMetricsSummary(filename, metrics) {
        const summary = document.getElementById("film_csv_summary");
        const filenameLabel = document.getElementById("film_csv_filename_label");
        const metricsGrid = document.getElementById("film_csv_metrics_preview");
        if (!summary || !filenameLabel || !metricsGrid) return;

        filenameLabel.textContent = filename;
        metricsGrid.innerHTML = "";

        if (metrics) {
            const yearRange =
                metrics.min_year !== null && metrics.max_year !== null
                    ? `${metrics.min_year} - ${metrics.max_year}`
                    : "N/A";
            const avgRating =
                metrics.avg_rating !== null && metrics.avg_rating !== undefined
                    ? `${Number(metrics.avg_rating).toFixed(2)} / 10`
                    : "N/A";

            const entries = [
                ["Movies", String(metrics.total_movies ?? 0)],
                ["Years", yearRange],
                ["Primary genre", metrics.primary_genre || "N/A"],
                ["Avg rating", avgRating],
            ];
            entries.forEach(([label, value]) => {
                const col = document.createElement("div");
                col.className = "col-6";
                const strong = document.createElement("strong");
                strong.textContent = `${label}: `;
                col.appendChild(strong);
                col.appendChild(document.createTextNode(value));
                metricsGrid.appendChild(col);
            });
        }

        summary.style.display = "block";
    }

    function resetFilmCsvSelection() {
        const csvInput = document.getElementById("csv_filename");
        const summary = document.getElementById("film_csv_summary");
        const uploadBlock = document.getElementById("film_upload_dataset");
        const agree = document.getElementById("film_agree_checkbox");
        const uploadBtn = document.getElementById("film_upload_button");

        if (csvInput) csvInput.value = "";
        if (summary) summary.style.display = "none";
        if (uploadBlock) uploadBlock.style.display = "none";
        if (agree) agree.checked = false;
        if (uploadBtn) uploadBtn.disabled = true;
    }

    function addFilmAuthorBlock(idx) {
        const wrapper = document.createElement("div");
        wrapper.className = "author row";
        wrapper.style.cssText =
            "border:2px dotted #ccc;border-radius:10px;padding:10px;margin:10px 0;background-color:white";

        const fields = [
            [`authors-${idx}-name`, "Name *"],
            [`authors-${idx}-affiliation`, "Affiliation"],
            [`authors-${idx}-orcid`, "ORCID"],
        ];

        fields.forEach(([name, labelText]) => {
            const col = document.createElement("div");
            col.className = "col-lg-6 col-12 mb-3";

            const label = document.createElement("label");
            label.className = "form-label";
            label.textContent = labelText;

            const input = document.createElement("input");
            input.name = name;
            input.className = "form-control";

            col.appendChild(label);
            col.appendChild(input);
            wrapper.appendChild(col);
        });

        const btnCol = document.createElement("div");
        btnCol.className = "col-12 mb-2";
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "btn btn-danger btn-sm";
        removeBtn.textContent = "Remove author";
        removeBtn.addEventListener("click", () => wrapper.remove());
        btnCol.appendChild(removeBtn);
        wrapper.appendChild(btnCol);

        return wrapper;
    }

    function initFilmDropzone() {
        const dropzoneEl = document.getElementById("filmDropzone");
        if (!dropzoneEl || typeof Dropzone === "undefined") return;

        Dropzone.options.filmDropzone = {
            url: "/filmdataset/file/upload",
            paramName: "file",
            maxFiles: 1,
            maxFilesize: 20,
            acceptedFiles: ".csv",
            init: function () {
                const dz = this;

                this.on("addedfile", function (file) {
                    clearFilmCsvErrors();
                    const ext = file.name.split(".").pop().toLowerCase();
                    if (ext !== "csv") {
                        this.removeFile(file);
                        showFilmCsvErrors([`Invalid file extension: ${file.name}. Please upload a .csv file.`]);
                        resetFilmCsvSelection();
                        return;
                    }
                    while (dz.files.length > 1) {
                        dz.removeFile(dz.files[0]);
                    }
                });

                this.on("success", function (_file, response) {
                    clearFilmCsvErrors();
                    const csvInput = document.getElementById("csv_filename");
                    if (csvInput) csvInput.value = response.filename || "";
                    renderCsvMetricsSummary(response.filename || "", response.metrics || null);

                    const uploadBlock = document.getElementById("film_upload_dataset");
                    if (uploadBlock) uploadBlock.style.display = "block";
                    if (typeof feather !== "undefined") feather.replace();
                });

                this.on("error", function (file, response) {
                    let parsed = response;
                    if (typeof response === "string") {
                        try {
                            parsed = JSON.parse(response);
                        } catch (_e) {
                            parsed = response;
                        }
                    }

                    let messages = [];
                    if (parsed && Array.isArray(parsed.errors) && parsed.errors.length > 0) {
                        messages = parsed.errors;
                    } else if (parsed && parsed.message) {
                        messages = [parsed.message];
                    } else if (typeof parsed === "string" && parsed.trim()) {
                        messages = [parsed];
                    } else {
                        messages = [`Could not validate CSV file: ${file.name}`];
                    }
                    showFilmCsvErrors(messages);
                    resetFilmCsvSelection();
                    this.removeFile(file);
                });

                const deleteBtn = document.getElementById("film_delete_csv_btn");
                if (deleteBtn) {
                    deleteBtn.addEventListener("click", function () {
                        const csvInput = document.getElementById("csv_filename");
                        const filename = csvInput ? csvInput.value : "";
                        dz.removeAllFiles(true);
                        resetFilmCsvSelection();
                        clearFilmCsvErrors();

                        if (!filename) return;
                        fetch("/filmdataset/file/delete", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ file: filename }),
                        }).catch((err) => console.error("Error deleting temp CSV:", err));
                    });
                }
            },
        };
    }

    function initFilmUploadForm() {
        const uploadBtn = document.getElementById("film_upload_button");
        if (!uploadBtn) return;

        const agreeCheckbox = document.getElementById("film_agree_checkbox");
        if (agreeCheckbox) {
            agreeCheckbox.addEventListener("change", function () {
                uploadBtn.disabled = !agreeCheckbox.checked;
            });
        }

        const addAuthorBtn = document.getElementById("film_add_author");
        if (addAuthorBtn) {
            addAuthorBtn.addEventListener("click", function () {
                const container = document.getElementById("film_authors");
                if (container) {
                    container.appendChild(addFilmAuthorBlock(filmAuthorCount++));
                }
            });
        }

        uploadBtn.addEventListener("click", function () {
            clearFilmUploadError();

            const titleInput = document.getElementById("film_title");
            const descInput = document.getElementById("film_desc");
            const csvInput = document.getElementById("csv_filename");
            const loading = document.getElementById("film_loading");

            const titleVal = titleInput ? titleInput.value.trim() : "";
            const descVal = descInput ? descInput.value.trim() : "";
            const csvVal = csvInput ? csvInput.value.trim() : "";

            if (titleVal.length < 3) {
                showFilmUploadError("Title must have at least 3 characters.");
                return;
            }
            if (descVal.length < 3) {
                showFilmUploadError("Description must have at least 3 characters.");
                return;
            }
            if (!csvVal) {
                showFilmUploadError("Please upload a valid CSV file before submitting.");
                return;
            }

            const formData = new FormData();
            const formContainer = document.getElementById("film_basic_info_form");
            if (formContainer) {
                formContainer.querySelectorAll("input, select, textarea").forEach((el) => {
                    if (el.name && !el.disabled) {
                        formData.append(el.name, el.value);
                    }
                });
            }
            formData.set("csv_filename", csvVal);

            uploadBtn.style.display = "none";
            if (loading) loading.style.display = "block";

            fetch("/filmdataset/upload", {
                method: "POST",
                body: formData,
            })
                .then((response) =>
                    response.json().then((data) => ({
                        ok: response.ok,
                        data,
                    }))
                )
                .then(({ ok, data }) => {
                    if (ok) {
                        window.location.href = data.dataset_url || "/dataset/list";
                    } else {
                        if (loading) loading.style.display = "none";
                        uploadBtn.style.display = "inline-block";
                        showFilmUploadError(data.message || "Failed to upload film dataset.");
                    }
                })
                .catch((err) => {
                    if (loading) loading.style.display = "none";
                    uploadBtn.style.display = "inline-block";
                    showFilmUploadError(`Network error: ${err.message}`);
                });
        });
    }

    function initFilmPreviewTable() {
        const section = document.getElementById("film-preview-section");
        if (!section) return;

        const previewUrl = section.dataset.previewUrl;
        const thead = document.getElementById("film-preview-thead");
        const tbody = document.getElementById("film-preview-tbody");
        const tableWrapper = document.getElementById("film-preview-table-wrapper");
        const loadingEl = document.getElementById("film-preview-loading");
        const emptyEl = document.getElementById("film-preview-empty");
        const errorEl = document.getElementById("film-preview-error");
        const countEl = document.getElementById("film-preview-count");
        const pageInfoEl = document.getElementById("film-preview-page-info");
        const prevBtn = document.getElementById("film-preview-prev");
        const nextBtn = document.getElementById("film-preview-next");
        const perPageSelect = document.getElementById("film-preview-per-page");

        let currentPage = 1;
        let currentPerPage = perPageSelect ? parseInt(perPageSelect.value, 10) || 10 : 10;

        function loadPage(page) {
            if (loadingEl) loadingEl.style.display = "block";
            if (errorEl) errorEl.style.display = "none";

            fetch(`${previewUrl}?page=${page}&per_page=${currentPerPage}`)
                .then((resp) => {
                    if (!resp.ok) {
                        throw new Error(`HTTP ${resp.status}`);
                    }
                    return resp.json();
                })
                .then((payload) => {
                    if (loadingEl) loadingEl.style.display = "none";
                    const headers = payload.headers || [];
                    const rows = payload.rows || [];
                    const total = payload.total || 0;
                    const respPage = payload.page || 1;
                    const respPerPage = payload.per_page || currentPerPage;
                    const totalPages = Math.max(1, Math.ceil(total / respPerPage));
                    currentPage = respPage;

                    if (thead) {
                        thead.innerHTML = "";
                        const trHead = document.createElement("tr");
                        headers.forEach((h) => {
                            const th = document.createElement("th");
                            th.scope = "col";
                            th.textContent = h;
                            trHead.appendChild(th);
                        });
                        thead.appendChild(trHead);
                    }

                    if (tbody) {
                        tbody.innerHTML = "";
                        rows.forEach((row) => {
                            const tr = document.createElement("tr");
                            headers.forEach((h) => {
                                const td = document.createElement("td");
                                td.textContent = row[h] !== undefined && row[h] !== null ? String(row[h]) : "";
                                tr.appendChild(td);
                            });
                            tbody.appendChild(tr);
                        });
                    }

                    if (total === 0) {
                        if (tableWrapper) tableWrapper.style.display = "none";
                        if (emptyEl) emptyEl.style.display = "block";
                        if (countEl) countEl.textContent = "0 movies";
                    } else {
                        if (emptyEl) emptyEl.style.display = "none";
                        if (tableWrapper) tableWrapper.style.display = "block";
                        const startIdx = (respPage - 1) * respPerPage + 1;
                        const endIdx = Math.min(total, startIdx + rows.length - 1);
                        if (countEl) countEl.textContent = `Showing ${startIdx}-${endIdx} of ${total} movies`;
                    }

                    if (pageInfoEl) pageInfoEl.textContent = `Page ${respPage} of ${totalPages}`;
                    if (prevBtn) prevBtn.disabled = respPage <= 1;
                    if (nextBtn) nextBtn.disabled = respPage >= totalPages;
                })
                .catch((err) => {
                    if (loadingEl) loadingEl.style.display = "none";
                    if (tableWrapper) tableWrapper.style.display = "none";
                    if (errorEl) {
                        errorEl.textContent = `Unable to load movie preview (${err.message}).`;
                        errorEl.style.display = "block";
                    }
                });
        }

        if (prevBtn) {
            prevBtn.addEventListener("click", function () {
                if (currentPage > 1) loadPage(currentPage - 1);
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener("click", function () {
                loadPage(currentPage + 1);
            });
        }
        if (perPageSelect) {
            perPageSelect.addEventListener("change", function () {
                currentPerPage = parseInt(perPageSelect.value, 10) || 10;
                loadPage(1);
            });
        }

        loadPage(1);
    }

    initFilmDropzone();
    document.addEventListener("DOMContentLoaded", function () {
        initFilmUploadForm();
        initFilmPreviewTable();
    });
})();
