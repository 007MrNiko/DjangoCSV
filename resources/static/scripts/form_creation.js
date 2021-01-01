let columnForm= document.querySelectorAll(".column_form")
let container = document.querySelector("#submit_form")
let addButton = document.querySelector("#add_form")
let totalForms = document.querySelector("#id_schemascolumn_set-TOTAL_FORMS")
let newPosition = document.querySelector("#additional_columns")

let formNum = columnForm.length-2
addButton.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()

    let newForm = columnForm[0].cloneNode(true)
    newForm.removeAttribute("hidden")
    let formRegex = RegExp(/_set-(\d)-/,'g')
    let columnType = document.querySelector("#id_category_type").value
    newForm.querySelector(".text_input").setAttribute("value", document.querySelector("#id_column_name").value)
    newForm.querySelector(".order_input").setAttribute("value", document.querySelector("#id_order").value)

    if (columnType === "integer"){
        deactivateElements(newForm, false)
    }
    else if (columnType === "text"){
        deactivateElements(newForm, true, false)
    }
    else {
        deactivateElements(newForm)
    }

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `_set-${formNum}-`)
    newForm.querySelector(".category_input").value = columnType;
    container.insertBefore(newForm, newPosition)

    totalForms.setAttribute('value', `${formNum+1}`)


}

function deactivateElements(newForm, integers = true, sentences = true){
    if (integers){
        newForm.querySelectorAll(".integer_type").forEach(element => element.closest("div").setAttribute("hidden", true))
    }
    if (sentences){
        newForm.querySelector(".sentence_type").closest("div").setAttribute("hidden", true)
    }
}

function activateElements(editForm, integers = false, sentences = false){
    if (integers){
        editForm.querySelectorAll(".integer_type").forEach(element => element.closest("div").removeAttribute("hidden"))
    }
    if (sentences){
        editForm.querySelector(".sentence_type").closest("div").removeAttribute("hidden")
    }
}

function realTimeChanging(element_id){
    let parentNode = document.getElementById("submit_form")
    let oldForm = document.querySelector(`#${element_id}`).closest("div.column_form")
    let editForm = oldForm.cloneNode(true);
    let selectValue = document.getElementById(element_id).value



    if (selectValue === "integer"){
        activateElements(editForm, true)
        deactivateElements(editForm, false)
    }
    else if (selectValue === "text"){
        activateElements(editForm, false, true)
        deactivateElements(editForm, true, false)
    }
    else {
        deactivateElements(editForm)
    }
    editForm.querySelector(".category_input").value = selectValue;
    parentNode.replaceChild(editForm, oldForm)
}
