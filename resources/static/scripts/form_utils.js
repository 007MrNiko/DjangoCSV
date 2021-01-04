function realTimeChanging(element_id) {
    // At column category changing activating and deactivating fields
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
    // Hiding delete checkbox when "editing view" outputting all forms
    editForm.querySelector("input[type=checkbox]").parentElement.setAttribute("hidden", true)
    parentNode.replaceChild(editForm, oldForm)
}

function deactivateElements(newForm, integers = true, sentences = true) {
    // Turning off column fields
    if (integers) {
        newForm.querySelectorAll(".integer_type").forEach(element => element.closest("div").setAttribute("hidden", true))
    }
    if (sentences) {
        newForm.querySelector(".sentence_type").closest("div").setAttribute("hidden", true)
    }
}

function activateElements(editForm, integers = false, sentences = false) {
    // Turning on column fields
    if (integers) {
        editForm.querySelectorAll(".integer_type").forEach(element => element.closest("div").removeAttribute("hidden"))
    }
    if (sentences) {
        editForm.querySelector(".sentence_type").closest("div").removeAttribute("hidden")
    }
}

function moveOrderField(editForm, position = 0) {
    // Changing order field position in Bootstrap grid system
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
