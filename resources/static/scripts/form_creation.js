let columnForm = document.querySelectorAll(".column_form")
let container = document.querySelector("#submit_form")
let addButton = document.querySelector("#add_form")
let totalForms = document.querySelector("#id_schemascolumn_set-TOTAL_FORMS")
let newPosition = document.querySelector("#additional_columns")

let formNum = columnForm.length - 2
addButton.addEventListener('click', addForm)

function addForm(e) {
    e.preventDefault()

    let newForm = columnForm[0].cloneNode(true)
    newForm.removeAttribute("hidden")
    let formRegex = RegExp(/_set-(\d)-/, 'g')
    let columnType = document.querySelector("#id_category_type").value
    newForm.querySelector(".text_input").setAttribute("value", document.querySelector("#id_column_name").value)
    newForm.querySelector(".order_input").setAttribute("value", document.querySelector("#id_order").value)
    newForm.querySelector(".delete_column").closest("div").setAttribute("hidden", true)
    newForm.querySelector(".min_integer").setAttribute("value", 18)
    newForm.querySelector(".max_integer").setAttribute("value", 60)
    newForm.querySelector(".sentence_type").setAttribute("value", 5)

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
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `_set-${formNum}-`)
    newForm.querySelector(".category_input").value = columnType;
    container.insertBefore(newForm, newPosition)

    totalForms.setAttribute('value', `${formNum + 1}`)


}

function deactivateElements(newForm, integers = true, sentences = true) {
    if (integers) {
        newForm.querySelectorAll(".integer_type").forEach(element => element.closest("div").setAttribute("hidden", true))
    }
    if (sentences) {
        newForm.querySelector(".sentence_type").closest("div").setAttribute("hidden", true)
    }
}

function activateElements(editForm, integers = false, sentences = false) {
    if (integers) {
        editForm.querySelectorAll(".integer_type").forEach(element => element.closest("div").removeAttribute("hidden"))
    }
    if (sentences) {
        editForm.querySelector(".sentence_type").closest("div").removeAttribute("hidden")
    }
}

function realTimeChanging(element_id) {
    let parentNode = document.getElementById("submit_form")
    let oldForm = document.querySelector(`#${element_id}`).closest("div.column_form")
    let editForm = oldForm.cloneNode(true);
    let selectValue = document.getElementById(element_id).value


    if (selectValue === "integer") {
        activateElements(editForm, true)
        deactivateElements(editForm, false)
        moveOrderField(editForm, -4)
    } else if (selectValue === "text") {
        activateElements(editForm, false, true)
        deactivateElements(editForm, true, false)
        moveOrderField(editForm, -2)
    } else {
        deactivateElements(editForm)
        moveOrderField(editForm, 0)
    }
    editForm.querySelector(".category_input").value = selectValue;
    parentNode.replaceChild(editForm, oldForm)
}

function moveOrderField(editForm, position = 0) {
    let moveCol = editForm.getElementsByClassName("moving_order")[0]
    let marginRegex = RegExp(/offset-sm-/, 'g')
    let currentMargin = ""
    moveCol.classList.forEach(element => {
        if (element.match(marginRegex)) {
            currentMargin = element
        }
    });

    moveCol.classList.replace(currentMargin, `offset-sm-${5 + position}`)
}

function setDeleted(element_id) {
    let deleteForm = document.querySelector(`#${element_id}`).closest("div.column_form")
    deleteForm.getElementsByClassName("delete_column")[0].checked = true
    deleteForm.querySelector(".text_input").setAttribute("value", "null")
    deleteForm.querySelector(".order_input").setAttribute("value", 0)
    deleteForm.setAttribute("hidden", true)
}
