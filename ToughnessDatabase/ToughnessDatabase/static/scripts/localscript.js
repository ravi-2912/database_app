function addEventToFieldBtn(name) {
    $(`#add-${name}-btn`).click(function (e) {
        e.preventDefault();
        let elems = $(`[id^=${name}-]`)
        let last_elem = elems.last();
        let elem_count = elems.length;
        let new_elem_id = `${name}-${elem_count}`
        let new_elem = last_elem.parent().clone();
        new_elem.children().attr('id', new_elem_id);
        new_elem.children().attr('name', new_elem_id);
        if (last_elem.is('select')) {
            let opt_count = last_elem.children().length - 1;
            if ((elem_count + 1) > opt_count ) {
                return;
            }
        }
        new_elem.insertAfter(last_elem.parent())
    });

    $(`#rem-${name}-btn`).click(function (e) {
        e.preventDefault();
        let elems = $(`[id^=${name}-]`)
        let last_elem = elems.last();
        let elem_count = elems.length;
        if (elem_count > 1) {
            last_elem.parent().remove();
        }
    });

}

function addEventToFieldBtnMulti(name) {
    $(`#add-${name}-btn`).click(function(e) {
        e.preventDefault();
        let elems = $(`div.form-row[id^="${name}"]`)
        let prev_elem = elems.last();
        let new_elem = prev_elem.clone();
        let new_elem_children = new_elem.children();
        let newId = text => text.replace(/(\d+)+/g, function(match, number) {
            return parseInt(number)+1;
        });
        new_elem.attr('id', newId(new_elem.attr('id')));

        new_elem_children.each((i, el)=>{
            let child = $(el).children();
            child.attr('id', newId(child.attr('id')));
            child.attr('name', newId(child.attr('name')));
        })
        prev_elem.after(new_elem);
    });

    $(`#rem-${name}-btn`).click(function(e) {
        e.preventDefault();
        let elems = $(`div.form-row[id^="${name}"]`)
        let last_elem = elems.last();
        let elem_count = elems.length - 1;
        if (elem_count > 0) {
            last_elem.remove();
        }
    });
}