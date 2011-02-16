$(
function() {
    function replace_in_attr(elem, attr, str, replacement) {
        if (elem.attr(attr)) {
            elem.attr(attr, elem.attr(attr).replace(str, replacement));
        }
        var elems = elem.children();
        for(var i = 0; i < elems.length; i++) {
            var el = $(elems[i]);
            if (el.attr(attr)) {
                el.attr(attr, el.attr(attr).replace(str, replacement));
            }
        }
    }
    $(".add_field").live("click",function () {
        holder = $(this).parent().parent();
        var i, extra_elem_type, split_id;
        var nextall = $(holder).nextAll();
        var extra_num = -1;
        for (i = 0; i < nextall.length; i++) {
            cur_el = $(nextall[i]).attr('id');
            if (cur_el.indexOf('extra') !== -1) {
                split_id = cur_el.split("_");
                extra_num = Number(split_id.pop());
            } else {
                extra_elem_type = $.makeArray($($(holder).attr('id').split("_")).slice(2)).join("_");
                break;//dance
            }
        }
        if (extra_num === -1) {
            // No extra fields added yet
            extra_elem = $(holder).clone();
            replace_in_attr(extra_elem,
                "id", extra_elem_type, "extra_" + extra_elem_type + "_1");
            replace_in_attr(extra_elem,
                "name", extra_elem_type, "extra_" + extra_elem_type + "_1");
            replace_in_attr(extra_elem,
                "for", extra_elem_type, "extra_" + extra_elem_type + "_1");
            extra_elem.children()[1].value = null;
            $(extra_elem.children()[0]).children().remove();
            extra_elem.insertAfter(holder);
        } else {
            extra_elem = $(holder).clone();
            replace_in_attr(extra_elem,
                "id", extra_elem_type, "extra_" + extra_elem_type + "_" + (extra_num+1));
            replace_in_attr(extra_elem,
                "name", extra_elem_type,"extra_" + extra_elem_type + "_" + (extra_num+1));
            replace_in_attr(extra_elem,
                "for", extra_elem_type, "extra_" + extra_elem_type + "_" + (extra_num+1));
            extra_elem.children()[1].value = null;
            $(extra_elem.children()[0]).children().remove();
            extra_elem.insertAfter($(holder).nextAll()[extra_num-1]);
        }
        return false; // Stops weird bug where clicking the label would cause click
                      // to fire twice
    });
}
);
