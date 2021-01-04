// Getting all needed data from Schema creation form
let columnForm = document.querySelectorAll(".column_form")
let container = document.querySelector("#submit_form")
let addButton = document.querySelector("#add_form")
let totalForms = document.querySelector("#id_schemascolumn_set-TOTAL_FORMS")
let newPosition = document.querySelector("#additional_columns")

// Setting amount of current forms (2 because one is already generated as pattern and hidden down the page + array count)
let formNum = columnForm.length - 2
// Removing pattern form unit from total_count
totalForms.setAttribute('value', `${columnForm.length - 1}`)
addButton.addEventListener('click', addForm)

function addForm(e) {
    // Add column to list, using parameters
    e.preventDefault()

    // Copying hidden column from page
    let newForm = columnForm[columnForm.length - 1].cloneNode(true)
    // Make it visible
    newForm.removeAttribute("hidden")
    // Creating RegEx to change all ids for +1
    let formRegex = RegExp(/_set-(\d)-/, 'g')
    // Getting and setting new column parameter
    let columnType = document.querySelector("#id_category_type").value
    newForm.querySelector(".text_input").setAttribute("value", document.querySelector("#id_column_name").value)
    newForm.querySelector(".order_input").setAttribute("value", document.querySelector("#id_order").value)
    newForm.querySelector(".delete_column").closest("div").setAttribute("hidden", true)
    newForm.querySelector(".min_integer").setAttribute("value", 18)
    newForm.querySelector(".max_integer").setAttribute("value", 60)
    newForm.querySelector(".sentence_type").setAttribute("value", 5)

    // Switching needed field for column (accordingly to category)
    if (columnType === "integer") {
        deactivateElements(newForm, false)
        moveOrderField(newForm, -4)
    } else if (columnType === "text") {
        deactivateElements(newForm, true, false)
        moveOrderField(newForm, -2)
    } else {
        deactivateElements(newForm)
        moveOrderField(newForm, 0)
    }

    formNum++
    // Applying RegEx to new column
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `_set-${formNum}-`)
    newForm.querySelector(".category_input").value = columnType;
    // Adding column to page
    container.insertBefore(newForm, newPosition)

    // Setting amount of columns for Django formset
    totalForms.setAttribute('value', `${formNum + 1}`)


}

function setDeleted(element_id) {
    // Deleting form (setting its hidden delete field to checked)
    let deleteForm = document.querySelector(`#${element_id}`).closest("div.column_form")
    deleteForm.getElementsByClassName("delete_column")[0].checked = true
    deleteForm.querySelector(".text_input").setAttribute("value", "null")
    deleteForm.querySelector(".order_input").setAttribute("value", 0)
    deleteForm.setAttribute("hidden", true)
}
