/****************************************************************************

 COPYRIGHT NOTICE
 COPYRIGHT (C) {{ product.years }} WEBTELEMETRY US
 ALL RIGHTS RESERVED

 THIS SOURCE FILE, ITS MACHINE READABLE FORM, AND ANY
 REPRESENTATION OF THE MATERIAL CONTAINED HEREIN ARE
 WEBTELEMETRY INC OWNED.

 THE REPRODUCTION OR DISASSEMBLY OF EMBODIED PROGRAMS,
 DATA, OR ALGORITHMS IS PROHIBITED.

 COPYRIGHT PROTECTION CLAIMED INCLUDES ALL FORMS AND
 MATTERS OF COPYRIGHTABLE MATERIAL AND INFORMATION
 NOW ALLOWED BY STATUTORY OR JUDICIAL LAW OR HEREIN-
 AFTER GRANTED, INCLUDING WITHOUT LIMITATION, MATERIAL
 GENERATED FROM THE SOFTWARE PROGRAMS WHICH ARE
 DISPLAYED ON THE SCREEN SUCH AS ICONS, SCREEN DISPLAY
 LOOKS, BEHAVIOR OF PRODUCT, ETC.

 PROPRIETARY INFORMATION
 THESE MATERIALS ARE PROPRIETARY AND CONFIDENTIAL AND
 MAY NOT BE REPRODUCED IN ANY FORM WITHOUT THE PRIOR
 WRITTEN PERMISSION OF WEBTELEMETRY US.
 REPRODUCTION, TRANSCRIPTION, DISSEMINATION (INCLUDING UPLOADING
 TO INFORMATION SYSTEMS SUCH AS INTERNET, ETC.) OR
 USE OF INFORMATION CONTAINED HERE OR IN ANY DOCUMENTS
 OR MANUALS FOR PURPOSES, MAINTENANCE AND/OR OPERATION
 IS PROHIBITED WITHOUT WRITTEN AUTHORIZATION FROM
 WEBTELEMETRY US.

 Author: Leo Shatokhin
 Date:    {{ ansible_date_time.date }}
 ****************************************************************************/

function validate(obj) {
    var combo = document.getElementById(obj);
    var selectProceed = 0;

    for (i = 0; i <= (combo.options.length - 1); i++) {
        if (selectProceed != (combo.options.length - 1)) {
            alert("You must move all graphs from left to right");
            return false;
            break;
        }
    }
    return true;
}

function selectAll(selectBox, selectAll) {
    // have we been passed an ID
    if (typeof selectBox == "string") {
        selectBox = document.getElementById(selectBox);
    }

    // is the select box a multiple select box?
    if (selectBox.type == "select-multiple") {
        for (var i = 0; i < selectBox.options.length; i++) {
            selectBox.options[i].selected = selectAll;
        }
    }
}

function MoveUp(combo_name) {
    var combo = document.getElementById(combo_name);
    i = combo.selectedIndex;
    if (i > 0) {
        swap(combo, i, i - 1);
        combo.options[i - 1].selected = true;
        combo.options[i].selected = false;
    }
}

function MoveDown(combo_name) {
    var combo = document.getElementById(combo_name);
    i = combo.selectedIndex;

    if (i < combo.length - 1 && i > -1) {
        swap(combo, i + 1, i);
        combo.options[i + 1].selected = true;
        combo.options[i].selected = false;
    }
}

function MoveToTop(combo_name) {
    var combo = document.getElementById(combo_name);
    i = combo.selectedIndex;

    for (; i > 0; i--) {
        swap(combo, i, i - 1);
        combo.options[i - 1].selected = true;
        combo.options[i].selected = false;
    }
}

function MoveToBottom(combo_name) {
    var combo = document.getElementById(combo_name);
    i = combo.selectedIndex;

    if (i > -1) {
        for (; i < combo.length - 1; i++) {
            swap(combo, i + 1, i);
            combo.options[i + 1].selected = true;
            combo.options[i].selected = false;
        }
    }
}

//moves options from one selection box (combo box) to another
//removes the all selected options from one combo box and adds them to the second combo box
function MoveElements(FromComboName, ToComboName) {
    var FromCombo = document.getElementById(FromComboName);
    var ToCombo = document.getElementById(ToComboName);
    var to_remove_counter = 0; //number of options that were removed (num selected options)

    //move selected options to right select box (to)
    for (var i = 0; i < FromCombo.options.length; i++) {
        if (FromCombo.options[i].selected == true) {
            var addtext = FromCombo.options[i].text;
            var addvalue = FromCombo.options[i].value;
            ToCombo.options[ToCombo.options.length] = new Option(addtext, addvalue);
            FromCombo.options[i].selected = false;
            ++to_remove_counter;
        }
        else {
            FromCombo.options[i - to_remove_counter].selected = false;
            FromCombo.options[i - to_remove_counter].text = FromCombo.options[i].text;
            FromCombo.options[i - to_remove_counter].value = FromCombo.options[i].value;
        }
    }

    //now cleanup the last remaining options
    var numToLeave = FromCombo.options.length - to_remove_counter;

    for (i = FromCombo.options.length - 1; i >= numToLeave; i--) {
        FromCombo.options[i] = null;
    }
}

//this function is used to swap between elements
function swap(combo, index1, index2) {
    var savedValue = combo.options[index1].value;
    var savedText = combo.options[index1].text;

    combo.options[index1].value = combo.options[index2].value;
    combo.options[index1].text = combo.options[index2].text;
    combo.options[index2].value = savedValue;
    combo.options[index2].text = savedText;
}

function placeInHidden(delim, selStr, hidStr) {
    var selObj = document.getElementById(selStr);
    var hideObj = document.getElementById(hidStr);
    hideObj.value = '';

    for (var i = 0; i < selObj.options.length; i++) {
        hideObj.value = hideObj.value == '' ? selObj.options[i].value : hideObj.value + delim + selObj.options[i].value;
    }
}
