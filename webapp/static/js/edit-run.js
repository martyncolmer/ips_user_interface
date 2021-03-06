/*
    Created by Jack Allcock 21/06/2018
    This javascript file handles the edit PV's modal
*/

$(document).ready(function(e){

    // Create dictionary of all the table cell rows
    var tableRows = [];
            $("#form_table > tbody  > tr").each(function() {
                var row = {
                  "name" : $(this).find(".table--cell")[0],
                  "reason" : $(this).find(".table--cell")[1],
                  "content" : $(this).find(".table--cell")[2],
                };
                tableRows.push(row);
            });

    // Get length of dictionary so it can be iterated over
    rowsLength = tableRows.length

    // Take the contents of the table and put it into the hidden field
    fillInputFieldForPosting(rowsLength);

    // Get the modal so that we can hide/un-hide and attach the ID
    var modal = $(".modal");

    // On the click of the Modal Close button, hide the modal and refresh the page.
    $(".close").click(function(event){
        // Fade out 500ms
        modal.fadeOut(500);
    });

    // When the edit button is clicked, get the ID from the button attribute
    // Show the modal and change the input fields value to the ID
    $(".pv-edit-button").click(function(event){

        // Fade in 500ms
        modal.fadeIn(500);

        variableId = this.id;

        // Length of the rows in the table
        rowsLength = tableRows.length
        // Array we will append rows to
        data = [];

        /** First we need to go through the table data and find the row we need.
            Then we can set the modal inputs with data from that table row and update the actual table data when the
            okay button is clicked
        **/

        // Iterate over dictionary of table rows
        for (i=0; i < rowsLength; i++) {
            // Get dictionary out of array by index
            row = tableRows[i];
            // Get the PV Name text
            name = row['name'].innerHTML;

            // If the dictionary is the one we need add the data to the array
            if (name === variableId) {
                data.push(row['name']);
                data.push(row['reason']);
                data.push(row['content']);
            }
        }

        // Set the inputs values to that in the data array
        $("#id_input").val(data[0].innerHTML);
        $("#reason_input").val(data[1].innerHTML);
        $("#content_input").val(data[2].innerText);

        // Edit table data when the okay button is pressed
        $("#modal_okay_button").click(function(event){
            // Get values entered into the inputs by the user
            reasonInput = $('#reason_input').val();
            contentInput = $('#content_input').val();

            // Get the data from data array
            reason = data[1];
            content = data[2];

            // Update the table data to that in the array
            reason.innerHTML = reasonInput;
            content.innerHTML = contentInput;

            // Take the contents of the table and put it into the hidden field
            fillInputFieldForPosting(rowsLength);


        // Fade out 500ms
        modal.fadeOut(500);
        });

        // Make sure the page doesn't refresh/change when this button is clicked
        return false;
    });

function fillInputFieldForPosting(rowsLength) {
        // Fill hidden input with all table data as a comma separated string
        data = [];
        for (i=0; i < rowsLength; i++) {
            // Get row from dictionary
            row = tableRows[i];

            // Get the data from row
            name = row['name'].innerHTML;
            reason = row['reason'].innerHTML;
            content = row['content'].innerHTML;

            // Create a dictionary entry to put in the input
            var row = {
                  name : name,
                  "reason" : reason,
                  "content" : content,
                };

            // Add to the data array
            data.push(row);
        }

        // Iterate over data array and add the data as a comma separated list in the input
        dataLength = data.length;
        dataToSend = "";
        // Put the data array into the input
        for (i=0; i < dataLength; i++) {
            row = data[i]
            dataToSend += row['name'] + '^';
            dataToSend += row['reason']+ '^';
            dataToSend += row['content']+ '^';
        }
        $(".hidden-edit-input-content").val(dataToSend);

    }
});