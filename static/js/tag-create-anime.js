const RESULT_TABLE_TEMPLATE = document.getElementById('template-result-table').content;
const RESULT_ROW_TEMPLATE = document.getElementById('template-result-row').content;

function addAnime(event) {
    event.preventDefault();
    const id = event.target.querySelector('input[name="id"]').value;

    // Fetch the anime data from kitsu.io.
    fetch(`https://kitsu.io/api/edge/anime/${id}`)
        .then((response) => response.json())
        .then((json) => { handleAddAnimeResponse(json); })
}

function handleAddAnimeResponse(json) {
}

function search(event) {
    event.preventDefault();

    // Clear current results.
    const tableDiv = document.getElementById('result-table');
    tableDiv.innerHTML = '';

    // Construct query parameters.
    const query = document.getElementById('query').value;
    const params = new URLSearchParams();
    params.append('filter[text]', query);

    // Fetch the data from kitsu.io.
    fetch(`https://kitsu.io/api/edge/anime?${params.toString()}`)
        .then((response) => response.json())
        .then((json) => { handleSearchResponse(json); });
}

function handleSearchResponse(json) {
    const tableDiv = document.getElementById('result-table');

    // No results were found.
    if (json.data.length === 0) {
        tableDiv.innerHTML = 'No results found!';
        return;
    }

    // Display results.
    const table = document.importNode(RESULT_TABLE_TEMPLATE, true);
    tableDiv.appendChild(table);
    const tableBodyDiv = tableDiv.querySelector('tbody');

    for (const data of json.data) {
        const tableRow = document.importNode(RESULT_ROW_TEMPLATE, true);
        tableRow.querySelector('.result-title').textContent = data.attributes.canonicalTitle;
        tableRow.querySelector('.result-id').textContent = data.id;

        // Create the "add" form. Submitting this form triggers the "addAnime()" function.
        const addForm = tableRow.querySelector('.add-form');
        addForm.onsubmit = addAnime;
        addForm.querySelector('input[name="id"]').value = data.id;

        // Add the row to the table body.
        tableBodyDiv.appendChild(tableRow);
    }
}

const searchForm = document.getElementById('search-form');
searchForm.onsubmit = search;
