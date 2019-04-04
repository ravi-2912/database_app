function assignEventToFieldBtn(name) {
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
        let elems = $(`div[id^="${name}"]`).children()
        console.log(elems)
        let prev_elem = elems.last();
        let elem_count = elems.length
        html = `<div class="form-row mt-2" id="pipelines-${elem_count}">
                    <div class="col-md-3">
                        <input class="form-control" id="pipelines-${elem_count}-short_name" name="pipelines-${elem_count}-short_name" required type="text" >
                    </div>
                    <div class="col-md-9">
                        <input class="form-control" id="pipelines-${elem_count}-name" name="pipelines-${elem_count}-name" type="text">
                    </div>
                </div>`;
        prev_elem.after(html);
    });
    $(`#rem-${name}-btn`).click(function(e) {
        e.preventDefault();
        let elems = $('div[id^="pipelines"]')
        let last_elem = elems.last();
        let elem_count = elems.length - 1;
        if (elem_count > 1) {
            last_elem.remove();
        }
    });
}